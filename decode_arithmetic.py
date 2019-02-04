#!/usr/bin/python
# coding:UTF-8
"""
calc_arithmetic.py: calc_arithmetic
 
//example:
$ python decode_arithmetic.py 
Please input probabilities p1 p2 p3 ... seperated by a space
0.2 0.3 0.5
Please input decode number
0.63215699                               
number: 0.6321569900 symbol: x3 low 0.50 high 1.00, prob 0.50
number: 0.2643139800 symbol: x2 low 0.20 high 0.50, prob 0.30
number: 0.2143799333 symbol: x2 low 0.20 high 0.50, prob 0.30
number: 0.0479331111 symbol: x1 low 0.00 high 0.20, prob 0.20
number: 0.2396655556 symbol: x2 low 0.20 high 0.50, prob 0.30
number: 0.1322185185 symbol: x1 low 0.00 high 0.20, prob 0.20
number: 0.6610925926 symbol: x3 low 0.50 high 1.00, prob 0.50
number: 0.3221851852 symbol: x2 low 0.20 high 0.50, prob 0.30
number: 0.4072839506 symbol: x2 low 0.20 high 0.50, prob 0.30
number: 0.6909465021 symbol: x3 low 0.50 high 1.00, prob 0.50
number: 0.3818930041 symbol: x2 low 0.20 high 0.50, prob 0.30
number: 0.6063100137 symbol: x3 low 0.50 high 1.00, prob 0.50
number: 0.2126200274 symbol: x2 low 0.20 high 0.50, prob 0.30
number: 0.0420667582 symbol: x1 low 0.00 high 0.20, prob 0.20
number: 0.2103337908 symbol: x2 low 0.20 high 0.50, prob 0.30
number: 0.0344459693 symbol: x1 low 0.00 high 0.20, prob 0.20
Final result: x3x2x2x1x2x1x3x2x2x3x2x3x2x1x2x1
"""
#
# modification history:
# --------------------
# 2018/11/07, by Lin Xiongmin, Create
#

import math

def main():
    print("Please input probabilities p1 p2 p3 ... seperated by a space")
    str_arr = input().split(' ')
    probs = [float(num) for num in str_arr]

    print("Please input decode number")
    number = float(input())

    symbols = decode(probs, number, 16)
    print("Final result: %s"%(symbols))

def decode(probs, number, max):
    symbols = ""
    while(number > 0 and max > 0):
        max = max - 1

        symbol = getOutputSymbol(probs, number)
        symbol_low_range = getSymbolLowRange(symbol, probs)
        symbol_high_range = getSymbolHighRange(symbol, probs)
        prob = probs[symbol - 1]

        print("number: %2.10f symbol: x%d low %2.2f high %2.2f, prob %2.2f"%(number, symbol, symbol_low_range, symbol_high_range, prob))


        
        number = number - symbol_low_range
        number = number / probs[symbol - 1]

        symbols += "x{}".format(symbol)

    return symbols


def getOutputSymbol(probs, number):
    if number > 1:
        return 0
    sum = 0
    for i in range(len(probs)):
        sum += probs[i]
        if sum > number:
            return i+1

def getSymbolLowRange(symbol, probs):
    lowR = 0.0;
    if symbol <= 0 or symbol > len(probs):
        print("error symbol: %d"%(symbol))
        return lowR
    
    index = symbol - 1
    
    for i in range(index):
        lowR += probs[i]

    return lowR

def getSymbolHighRange(symbol, probs):
    highR = 0.0;
    if symbol <= 0 or symbol > len(probs):
        print("error symbol: %d"%(symbol))
        return highR

    index = symbol
        
    for i in range(index):
        highR += probs[i]

    return highR


if __name__ == "__main__":
    main()
