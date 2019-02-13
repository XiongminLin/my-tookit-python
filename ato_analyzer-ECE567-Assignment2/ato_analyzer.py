#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
ato_analyzer.py: read file and store each line into an array 

example: 
$ python --version
Python 3.6.5 :: Anaconda, Inc.
$ python ato_analyzer.py
----> Method 1: Tracking login velocity, threshold 10 m/s
True  Positive: 171, False Negative: 151
False Positive: 8, True Negative: 48
----> Method 2: Tracking number of consecutive login failures, threshold 3
True  Positive: 280, False Negative: 42
False Positive: 0, True Negative: 56
----> Method 2: Tracking number of consecutive login failures, threshold 4
True  Positive: 280, False Negative: 42
False Positive: 0, True Negative: 56
----> Method 2: Tracking number of consecutive login failures, threshold 5
True  Positive: 280, False Negative: 42
False Positive: 0, True Negative: 56
----> Method 3: IP blacklisting
True  Positive: 299, False Negative: 23
False Positive: 12, True Negative: 44
----> M4: Combine and apply all 3 methods at the same time
True  Positive: 317, False Negative: 5
False Positive: 20, True Negative: 36
"""
#
# modification history:
# --------------------
# 2019/2/12, by Lin Xiongmin, Create
#

from math import sin, cos, sqrt, atan2, radians, fabs
import datetime
import time

# seperate each item with TAB
TRAINING_FILE_PATH = "syslog.txt"

# the item position in each entry
# - starts from 0
P_TS = 5   # time stamp
P_RT = 6   # result
P_IP = 19  # IP address
P_CO = 24  # country
P_CI = 25  # Ciry
P_LO = 27  # longitude
P_LA = 28  # latitude

# Velocity threshold in "meter per second"
VELOCITY_THRESHOLD = 10

# Consecutive login failures
FAILURES_THRESHOLD = 3


def main():
	entries = readLog(TRAINING_FILE_PATH)

	runMethod1(entries)
	runMethod2(entries)
	runMethod3(entries)
	runMethod4(entries)


# M1: Tracking login velocity
def runMethod1(entries):
	base = getBaseResult(entries)
	print("----> Method 1: Tracking login velocity, threshold {} m/s".format(VELOCITY_THRESHOLD))
	result = method1TrackVel(entries)
	printConfusionMatrix(base, result)


# M2: Tracking number of consecutive login failures compared against threshold
def runMethod2(entries):
	base = getBaseResult(entries)
	FAILURES_THRESHOLD = 3
	for i in range(3):

		print("----> Method 2: Tracking number of consecutive login failures, threshold {}".format(FAILURES_THRESHOLD))
		result = method2TrackFailure(entries)
		printConfusionMatrix(base, result)
		FAILURES_THRESHOLD += 1


# M3 IP blacklisting
def runMethod3(entries):
	base = getBaseResult(entries)
	print("----> Method 3: IP blacklisting")
	result = method3IPBlock(entries)
	printConfusionMatrix(base, result)


# M4: Combine and apply all 3 methods at the same time on the dataset
def runMethod4(entries):
	base = getBaseResult(entries)
	print("----> M4: Combine and apply all 3 methods at the same time")

	result_1 = method1TrackVel(entries)
	result_2 = method2TrackFailure(entries)
	result_3 = method3IPBlock(entries)

	result = []

	for i in range(len(result_1)):
		result.append(result_1[i] or result_2[i] or result_3[i])

	printConfusionMatrix(base, result)


def getBaseResult(entries):
	result = []
	for entry in entries:
		if (entry[P_RT] == "SUCCESS") or (entry[P_RT] == "ALLOW"):
			result.append(False)
		else:
			result.append(True)

	return result

# M1: Tracking login velocity
def method1TrackVel(entries):
	predict = [] # true: attack, false: not an attack
	lastLoginDic = {}
	for index in range(len(entries)):
		entry = entries[index]

		if index == 0:
			predict.append(False)
		
		else:
			predict.append(isVelTooLarge(entries[index-1], entry))

	return predict


# M2: Tracking number of consecutive login failures compared against threshold
def method2TrackFailure(entries):
	predict = [] # true: attack, false: not an attack
	failuresSoFar = 0
	for index in range(len(entries)):
		entry = entries[index]
		result = entry[P_RT]

		# legal attempt list
		if result != "FAILURE":
			failuresSoFar = 0
			predict.append(False)
		
		else:
			failuresSoFar += 1
			predict.append(isTooManyFailures(failuresSoFar))

	return predict


# M3 IP blacklisting
def method3IPBlock(entries):
	# legal IP list
	WhiteIPs = getWhiteIPs(entries)
	predict = [] # true: attack, false: not an attack
	for index in range(len(entries)):
		entry = entries[index]
		IP = entry[P_IP]
		
		if isIPInBlackList(IP, WhiteIPs):
			predict.append(True)
		else:
			predict.append(False)

	return predict


def isVelTooLarge(entry1, entry2):
	v = getLoginVelocity(entry1, entry2)
	#print(v)
	return v > VELOCITY_THRESHOLD

def isTooManyFailures(failuresSoFar):
	return failuresSoFar >= FAILURES_THRESHOLD

def isIPInBlackList(IP, WhiteIPs):
	return not IP in WhiteIPs

# read item list from file
# - notice: one item, one line
def readLog(fileName):
    itemList = []
    file = open(fileName)
    skip = True
    while 1:
        line = file.readline()
        if not line:
            break

        # skip head line
        if skip:
        	skip = False
        	continue
        
        if line != '\n':
            itemList.append(line.strip('\n').split('\t'))
    return itemList

# get white ip list
def getWhiteIPs(entries):
	IPs = set()
	for entry in entries:
		if ((entry[P_RT] == "SUCCESS") or (entry[P_RT] == "ALLOW")) and entry[P_IP] != "":
			IP = entry[P_IP]
			IPs.add(IP)

	return IPs

# check if entry is legal or not
# - SUCCESS or ALLOW or IP in white list
def isLegalAttempt(entry):
	IP = entry[P_IP]
	result = entry[P_RT]

	return (result == "SUCCESS") or (result == "ALLOW") or (IP in WhiteIPs)


# the login velocity (distance between 2 consecutive logins divided by time difference) 
def getLoginVelocity(entry1, entry2):
	d = getDistanceInMeter(entry1, entry2)
	t = getTimeDiffInSecond(entry1, entry2)

	#print(d)
	#print(t)

	if t == 0:
		v = VELOCITY_THRESHOLD + 1
	else:
		v = d * 1.0 / t

	return fabs(v)


# get distance between two points based on latitude/longitude
def getDistanceInMeter(entry1, entry2):
	# approximate radius of earth in meter
	R = 6373.0 * 1000

	if (entry1[P_LA] == "") or (entry1[P_LO] == "") or (entry2[P_LA] == "") or (entry2[P_LO] == ""):
		return 0

	lat1 = radians(float(entry1[P_LA]))
	lon1 = radians(float(entry1[P_LO]))
	lat2 = radians(float(entry2[P_LA]))
	lon2 = radians(float(entry2[P_LO]))

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c

	return distance

# time diff between two entry, in seconds
def getTimeDiffInSecond(entry1, entry2):
	ts1 = getTimeStamp(entry1[P_TS])
	ts2 = getTimeStamp(entry2[P_TS])
	return ts2 - ts1


# get time stamp from a given date time str
# - exmaple: 2018-12-06T03:19:22.494Z
def getTimeStamp(date_time_str):
	dt = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')

	utc_delta = datetime.datetime.utcnow()-datetime.datetime.now()
	utc_time = dt - utc_delta

	timestamp = float(time.mktime(utc_time.timetuple()) + utc_time.microsecond/1000000.0)

	return timestamp


def printConfusionMatrix(base, predict):
	TP = 0
	FP = 0
	FN = 0
	TN = 0

	for i in range(len(base)):
		if base[i] and predict[i]:
			TP = TP + 1
		elif (not base[i]) and predict[i]:
			FP = FP + 1
		elif base[i] and (not predict[i]):
			FN = FN + 1
		else:
			TN = TN + 1

	print("True Positive: {}, False Negative: {}".format(TP, FN))
	print("False Positive: {}, True Negative: {}".format(FP, TN))

if __name__ == "__main__":
    main()