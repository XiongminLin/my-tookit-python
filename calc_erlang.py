#!/usr/bin/python
# coding:UTF-8
"""
calc_erlang.py: calc_erlang
 
//example:
$ python calc_erlang.py 
"""
#
# modification history:
# --------------------
# 2019/01/22, by Lin Xiongmin, Create
#

import math


def main():
    N = 5
    A = 5
    P = 1.0
    for i in range(N+1):
        P = (A * P)  / (i + A * P)
        print("when i = {}, P = {}".format(i, P))


if __name__ == "__main__":
    main()
