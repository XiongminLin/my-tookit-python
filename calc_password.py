#!/usr/bin/python
# coding:UTF-8
"""
calc_password.py: calc_password
 
//example:
$ python calc_password.py 
==>All valid bank accounts: 1.000e+08
---------------------------------
P (Password space): 5.461e+23
H (Only special characters): 1.720e+18
E (Only digit number and special character; Digit number ≥1; Special character ≥0): 3.919e+19
F (Only lower case letter and special character; Lower case letter ≥1; Special character ≥0): 1.808e+21
G (Only upper case letter and special character; Upper case letter ≥1; Special character ≥0): 1.808e+21
CFGH (no digit number): 1.439e+23
DEGH (no lower case letter): 1.182e+22
BEFH (no upper case letter): 1.182e+22
==> All valid passwords (without token): 3.822e+23
---------------------------------
backoff scheme, maximum try times: 173 for a machine
Machines: 500000
==> Try times in total: 86500000 
---------------------------------
==> Bingo Probability: 2.263e-24
"""
#
# modification history:
# --------------------
# 2019/01/31, by Lin Xiongmin, Create
#

import math
numbers = [8, 9, 10, 11, 12]
machines = 500000
GuessN = 1000000  # guess per second

def main():

	# all possible bank account
	allAcounts = getAccounts()

	# # question 1, machines -> 1
	# # question 2, machines -> 500000
	# passwords = getAllPsbPswd()
	# tryTimes = getTryTimes()

	# question 3 a), machines 500000, try with delay
	passwords = getAllPsbPswd()
	tryTimes = getTryTimes_delay()

	# question 3 b), machines 500000, password with OTP
	# passwords = getAllPsbPswd_OTP()
	# tryTimes = getTryTimes()
	
	p = (tryTimes * 1.0) / (passwords * allAcounts)
	
	print("---------------------------------")
	print("==> Bingo Probability: %.3e"%(p))


def getTryTimes_delay():

	x = 1.1
	totalDelay = 0
	year = 5
	allseconds = 60 * 60 * 24 * 365 * year
	tryTimes = 0

	while totalDelay < allseconds:
		wait = x ** tryTimes
		totalDelay += wait
		tryTimes = tryTimes + 1

	print("---------------------------------")
	print("backoff scheme, maximum try times: {} for a machine".format(tryTimes-1))
	print("Machines: {}".format(machines))
	print("==> Try times in total: {} ".format((tryTimes-1)*machines))
	return (tryTimes-1)*machines

def getTryTimes():
	year = 5
	timesPerMachine = GuessN * 60 * 60 * 24 * 365 * year
	totalTimes = machines * timesPerMachine

	print("---------------------------------")
	print("Machines: {}".format(machines))
	print("Try times per merchine: %.3e"%(timesPerMachine))
	print("==> Try times in total: %.3e"%(totalTimes))

	return totalTimes


def getAccounts():
	accounts = 10**8
	print("==>All valid bank accounts: %.3e"%(accounts))

	return accounts

def getAllPsbPswd_OTP():
	psw = getAllPsbPswd()
	tokens = 10**6
	allPsw = psw * tokens
	print("==> All valid passwords (with token): %.3e"%allPsw)

	return allPsw


def getAllPsbPswd():
	
	P = count(95)
	H = count(33)
	E = count(43) - count(33)
	F = count(59) - count(33)
	G = count(59) - count(33)

	CFGH = count(85)
	DEGH = count(69)
	BEFH = count(69)

	A = P - (H+E+F+G+CFGH+DEGH+BEFH)+3*H+2*E+2*F+2*G

	print("---------------------------------")
	print("P (Password space): %.3e"%(P))
	print("H (Only special characters): %.3e"%(H))
	print("E (Only digit number and special character; Digit number ≥1; Special character ≥0): %.3e"%(E))
	print("F (Only lower case letter and special character; Lower case letter ≥1; Special character ≥0): %.3e"%(F))
	print("G (Only upper case letter and special character; Upper case letter ≥1; Special character ≥0): %.3e"%(G))
	print("CFGH (no digit number): %.3e"%(CFGH))
	print("DEGH (no lower case letter): %.3e"%(DEGH))
	print("BEFH (no upper case letter): %.3e"%(BEFH))
	print("==> All valid passwords (without token): %.3e"%(A))

	return A

def count(base):
	total = 0

	for n in numbers:
		total += base ** n
	return total

if __name__ == "__main__":
    main()
