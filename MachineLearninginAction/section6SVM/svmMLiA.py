#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/7 16:47
# @Author  : Lelsey
# @Site    : 
# @File    : svmMLiA.py
# @Software: PyCharm Community Edition
# @Description: SMO算法中的辅助函数
import random
from numpy import *
def loadDataSet(filename):
    dataMet = []
    labelMet = []
    fr = open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMet.append([float(lineArr[0]), float(lineArr[1])])
        labelMet.append([float(lineArr[2])])
    return dataMet, labelMet
def selectJrand(i, m):
    j = i
    while j==i:
        j = int(random.uniform(0,m))
    return j
def clipAlpha(aj, H, L):
    if aj >H:
        aj = H
    if L >aj:
        aj = L
    return aj
def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()
    b = 0
    m, n = shape(dataMatrix)
    alphas = mat(zeros((m,1)))
    iter = 0
    while iter < maxIter:
        alphaPairChanged = 0
        for i in range(m):
            print multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[i,:].T)
            print "*"
            print labelMat[i]
            fXi = float(multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[i,:].T)) + b
            #fXi = float(multiply(alphas, labelMat).T * (dataMatrix*dataMatrix[i,:].T)) + b
            Ei = fXi - float(labelMat[i])
            if (labelMat[i] * Ei < -toler) and (alphas[i] < C) or \
                    ((labelMat[i] * Ei > toler) and (alphas[i] > 0)):
                j = selectJrand(i, m)
                fXj = float(multiply(alphas, labelMat).T * (dataMatrix*dataMatrix[j, :])) + b
                Ej = fXj - float(labelMat[j])
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()
                if (labelMat[i] != labelMat[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L == H:
                    print "L==H"
                    continue
                eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - \
                    dataMatrix[i,:]*dataMatrix[1,:].T - \
                    dataMatrix[j,:]*dataMatrix[j,:].T
                if eta >= 0:
                    print "eta>=0"
                    continue
                alphas[j] -= labelMat[j]*(Ei - Ej) / eta
                alphas[j] = clipAlpha(alphas[j], H, L)
                if abs(alphas[j] - alphaJold) < 0.00001:
                    print "j not moving enough"
                    continue
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold - alphas[j])
                b1 = b - Ei - labelMat[i]*(alphas[i] - alphaJold)*\
                    dataMatrix[i,:]*dataMatrix[i,:].T - \
                    labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b - Ej - labelMat[i]*(alphas[i] - alphaJold)*\
                    dataMatrix[i,:]*dataMatrix[j,:].T - \
                    labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if (0 < alphas[i]) and (C > alphas[i]):
                    b = b1
                elif (0 < alphas[j]) and (C > alphas[j]):
                    b = b2
                else:
                    b = (b1 + b2)/2.0
                alphaPairChanged +=1
                print "iter: %d i:%d, pairs changed %d" %(iter, i ,alphaPairChanged)
        if alphaPairChanged == 0:
            iter +=1
        else:
            iter = 0
        print "iteration number: %d" %iter
    return b, alphas
dataArr, lableArr = loadDataSet('testSet.txt')
b,alphs = smoSimple(dataArr, lableArr, 0.6, 0.001, 40)