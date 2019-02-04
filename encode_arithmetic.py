#!/usr/bin/python
# coding:UTF-8
"""
encode_arithmetic.py: encode_arithmetic
 
//example:
$ python encode_arithmetic.py
Please input probabilities p1 p2 p3 ... seperated by a space
0.7 0.2 0.1
Please input source symbols index 1 2 3 for x1 x2 x3 ... seperated by a space
1 1 2
==============================
probabilities: [0.7, 0.2, 0.1]
source symbol index: [0.7, 0.2, 0.1]
x1: [low range: 0.00, high range: 0.70) -> [0.0000000000, 0.7000000000) -> ['0', '1']
x1: [low range: 0.00, high range: 0.70) -> [0.0000000000, 0.4900000000) -> ['00', '01']
x2: [low range: 0.70, high range: 0.90) -> [0.3430000000, 0.4410000000) -> ['010', '011']
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

    print("Please input source symbols index 1 2 3 for x1 x2 x3 ... seperated by a space")
    str_arr = input().split(' ')
    symbols = [int(num) for num in str_arr]

    print("==============================")
    print("probabilities: %s"%(probs))
    print("source symbol index: %s"%(symbols))

    encode(probs, symbols)

def encode(probs, symbols):

    low = 0
    high = 1
    symbol_range = 1

    characs = ""

    for i in range(len(symbols)):
        symbol = symbols[i]

        characs += "x{}".format(symbol)

        lowR = getSymbolLowRange(symbol, probs)
        highR = getSymbolHighRange(symbol, probs)

        high = low + symbol_range * highR
        low = low + symbol_range * lowR

        symbol_range = high - low

        print("x%d: [low range: %2.2f, high range: %2.2f)  [low: %2.10f, high: %2.10f) -> %18s : %s"%(symbol, lowR, highR, low, high, characs, convertBinary(low, high)))

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

# convertBinary(0.4304514, 0.43053862)
# ['01101110001100', '01101110001101']
def convertBinary(low, high):
    if low > 1 or high > 1:
        print("number should be less than 1")
        return 0
    
    binaryLow = ""
    binaryHigh = ""

    l = int(0)
    h = int(0)
    

    while((l is 1 and h is 1) or (l is 0 and h is 0)):
        low = low * 2
        high = high * 2

        l = int(low) // 1
        h = int(high) // 1

        binaryLow += "{}".format(l)
        binaryHigh += "{}".format(h)

        if l is 1:
            low = low - 1
    
        if h is 1:
            high = high - 1


    return [binaryLow, binaryHigh]


if __name__ == "__main__":
    main()
