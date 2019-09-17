# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:00:10 2019

@author: annaf
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


    

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


   