#!/usr/bin/python
# coding:UTF-8
"""
calc_entropy.py: calc_entropy
 
//example:
$ python calc_entropy.py 
Please input numbers seperated by a space
1 1
Info([1, 1]) = Entropy([0.5, 0.5]) = 1.0
"""
#
# modification history:
# --------------------
# 2018/09/18, by Lin Xiongmin, Create
#

import math


def main():
    params = inputArray()
    entropy(params)


def inputArray():
    print("Please input numbers seperated by a space")
    str_arr = raw_input().split(' ')  # will take in a string of numbers separated by a space
    arr = [float(num) for num in str_arr]
    return arr

def entropy(params):
    probabilities = []
    self_infos = []
    info = 0
    sum = 0
    for param in params:
        sum += param

    for param in params:
        probabilities.append(1.0*param/sum)

        if param == 0:
            continue
        
        self_infos.append(-log2(1.0*param/sum))

        info += ( -1.0 * param / sum) * log2(1.0 * param/sum)

    print("*****************************************************************")
    print("Info(%s) = Entropy(%s) = %s bits")%(params, probabilities, info)
    print("Self Infos of %s is %s bits")%(probabilities, self_infos)
    print("*****************************************************************")

def log2(param):
    return math.log10(param) / math.log10(2)

if __name__ == "__main__":
    main()
