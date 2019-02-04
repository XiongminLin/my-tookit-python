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
    numerators = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    denominators = numerators

    for d in denominators:
        results = []
        for n in numerators:
            value = log2(n * 1.0 / d)
            results.append(value * 1000 / 1000)
        print(results)


def log2(param):
    return math.log10(param) / math.log10(2)

if __name__ == "__main__":
    main()
