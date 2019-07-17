# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:00:10 2019

@author: annaf
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def mergeLabels(WILLabels, WIELabels, nWILLabels, nWIELabels):
    nLabels = nWILLabels * nWIELabels
    labels = np.zeros(len(WILLabels), dtype=int)
    labelDict = {}
    label = 0
    for i in range(len(labels)):
        dictIndex = WILLabels[i] + WIELabels[i]*nWILLabels
        if not dictIndex in labelDict:
            labelDict[dictIndex] = label
            label += 1
        labels[i] = labelDict[dictIndex]
    return labels, label, labelDict
    

def splitTimesPerCluster(releaseTimes, executionTimes, labels, k):
    splitTimes = []
    splitReleaseTimes = []
    splitExecutionTimes = []
    unique, counts = np.unique(labels, return_counts=True)
    for i in range(k):
        kTimes = np.zeros((counts[i], 2))
        splitTimes.append(kTimes)
        kTimes = np.zeros(counts[i])
        splitReleaseTimes.append(kTimes)
        kTimes = np.zeros(counts[i])
        splitExecutionTimes.append(kTimes)
    labelIndices = np.zeros(k, dtype=int)
    for i in range(labels.size):
        label = labels[i]
        splitTimes[label][labelIndices[label]][0] = releaseTimes[i]
        splitTimes[label][labelIndices[label]][1] = executionTimes[i]
        splitReleaseTimes[label][labelIndices[label]] = releaseTimes[i]
        splitExecutionTimes[label][labelIndices[label]] = executionTimes[i]
        labelIndices[label] += 1
    return splitTimes, splitReleaseTimes, splitExecutionTimes

def splitLabelsPerCluster(labels1, labels2, splitLabels, k):
    splitLabels1 = []
    splitLabels2 = []
    unique, counts = np.unique(splitLabels, return_counts=True)
    for i in range(k):
        kLabels1 = np.zeros(counts[i])
        splitLabels1.append(kLabels1)
        kLabels2 = np.zeros(counts[i])
        splitLabels2.append(kLabels2)
    labelIndices = np.zeros(k, dtype=int)
    for i in range(splitLabels.size):
        label = splitLabels[i]
        splitLabels1[label][labelIndices[label]] = labels1[i]
        splitLabels2[label][labelIndices[label]] = labels2[i]
        labelIndices[label] += 1
    return splitLabels1, splitLabels2


   