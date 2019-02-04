#!/usr/bin/python
# coding:UTF-8
"""
classfier_roc.py: classfier_roc
 
//example:
$ python classfier_roc.py 
"""
#
# modification history:
# --------------------
# 2018/11/29, by Lin Xiongmin, Create
#

import matplotlib.pyplot as plt



def main():
    actual_list = [1, 1, 0, 0, 1, 1, 0, 0, 1, 0]
    
    list_a = [0.73, 0.69, 0.44, 0.55, 0.67, 0.47, 0.08, 0.15, 0.45, 0.35]
    TPRs_a = []
    FPRs_a = []

    list_b = [0.61, 0.03, 0.68, 0.31, 0.45, 0.09, 0.38, 0.05, 0.01, 0.04]
    TPRs_b = []
    FPRs_b = []

    # Question 1
    for i in range(1000):
        threshold = i * 1.0 / 1000
        
        predict_list_a = predict(list_a, threshold)
        P, N, TP, FP = getConfustionMatrix(actual_list, predict_list_a)
        TPR_a, FPR_a = getROC(P, N, TP, FP)
        TPRs_a.append(TPR_a)
        FPRs_a.append(FPR_a)

        predict_list_b = predict(list_b, threshold)
        P, N, TP, FP = getConfustionMatrix(actual_list, predict_list_b)
        TPR_b, FPR_b = getROC(P, N, TP, FP)
        TPRs_b.append(TPR_b)
        FPRs_b.append(FPR_b)


    plt.plot(FPRs_a, TPRs_a, label="classifier A")
    plt.plot(FPRs_b, TPRs_b, label="classfiier B")
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.title("ROC Graph")
    plt.grid(True)
    plt.legend()
    plt.show()

    # Question 2
    predict_list_a = predict(list_a, 0.5)
    P, N, TP, FP = getConfustionMatrix(actual_list, predict_list_a)
    print("=====Classifier A: ======")
    print("P %d, N %d, TP %d, FP %d"%(P, N, TP, FP))
    print("Precision: %f"%(getPrecision(TP, FP)))
    print("Recall: %f"%(getRecall(TP, P)))
    print("F-Measure: %f"%(getFMeasure(P, TP, FP)))

    # Question 3
    print("=====Classifier B: ======")
    predict_list_b = predict(list_b, 0.5)
    P, N, TP, FP = getConfustionMatrix(actual_list, predict_list_b)
    print("P %d, N %d, TP %d, FP %d"%(P, N, TP, FP))
    print("Precision: %f"%(getPrecision(TP, FP)))
    print("Recall: %f"%(getRecall(TP, P)))
    print("F-Measure: %f"%(getFMeasure(P, TP, FP)))

    # Question 4
    thresholds = [0.1, 0.5]
    for threshold in thresholds:
        
        predict_list_a = predict(list_a, threshold)
        P, N, TP, FP = getConfustionMatrix(actual_list, predict_list_a)
        TPR_a, FPR_a = getROC(P, N, TP, FP)
        TPRs_a.append(TPR_a)
        FPRs_a.append(FPR_a)


    print(TPRs_a)
    print(FPRs_a)

    plt.plot(FPRs_a, TPRs_a, label="classifier A")
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.title("ROC Graph")
    plt.grid(True)
    plt.legend()
    plt.show()

def getPrecision(TP, FP):
    return TP * 1.0 / (TP + FP)

def getRecall(TP, P):
    return TP * 1.0 / P

def getFMeasure(P, TP, FP):
    precision = getPrecision(TP, FP)
    recall = getRecall(TP, P)
    fMeasure = 2 * precision * recall / (precision + recall)
    return fMeasure

def predict(m_list, threshold):
    predict_class_list = []
    for data in m_list:
        if data > threshold:
            predict_class_list.append(1)
        else:
            predict_class_list.append(0)

    return predict_class_list


def getConfustionMatrix(actual_class_list, predict_class_list):
    P = 0
    N = 0
    TP = 0
    FP = 0
    for i in range(len(actual_class_list)):
        if actual_class_list[i] == 1:
            P = P + 1
            if predict_class_list[i] == 1:
                TP = TP + 1
        else:
            N = N + 1
            if predict_class_list[i] == 1:
                FP = FP + 1

    return P, N, TP, FP

def getROC(P, N, TP, FP):
    TPR = TP * 1.0 / P
    FPR = FP * 1.0 / N

    return TPR, FPR

if __name__ == "__main__":
    main()
