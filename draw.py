#!/usr/bin/python
"""
encode_arithmetic.py: encode_arithmetic
 
//example:

"""
#
# modification history:
# --------------------
# 2018/11/08, by Lin Xiongmin, Create
#
import numpy as np
import matplotlib.pyplot as plt
import math

def main():
	cA = []
	cB = []
	N = 100
	xarray = []
	for i in range(N):
		x = (1.0 * (i + 1)) / (2 * N)
		cA.append(channelCapacityA(x))
		cB.append(channelCapacityB(x))
		xarray.append(x)

	plt.plot(xarray, cA)
	plt.plot(xarray, cB)
	plt.show()

def channelCapacityA(x):
	return log2(3) - entropy([1-2*x, x, x])

def channelCapacityB(x):
	return log2(3) - entropy([6 * x * x - 4 * x + 1, 2 * x - 3 * x * x, 2 * x - 3 * x * x])

def log2(param):
    return math.log10(param) / math.log10(2)

def entropy(params):
	print(params)
	info = 0
	for i in range(len(params)):
		param = params[i]
		if param > 0:
			info += ( -1.0 * param) * log2(1.0 * param)
	return info


if __name__ == "__main__":
    main()