#!/usr/bin/env python
import math
import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt

 
def drawTimeHistInRange(times, title, xRange):
    plt.figure()
    plt.title(title)
    plt.hist(times, bins=70, range=xRange)


def drawTimesPerTwoProcess(releaseTimes, executionTimes, processes, xlabel = "", ylabel = "", title = "", naProcess=0):
    releaseTimesPerProcess = []
    executionTimesPerProcess = []
    for i in range(len(processes)):
        releaseTimesPerProcess.append([])
        executionTimesPerProcess.append([])
    nTimes = len(releaseTimes)
    for i in range(nTimes):
        rt = releaseTimes[i]
        releaseTimesPerProcess[processes[i]].append(rt)
        executionTimesPerProcess[processes[i]].append(executionTimes[i])
    plt.figure()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.scatter(releaseTimesPerProcess[naProcess], executionTimesPerProcess[naProcess], c='tab:blue', marker='+')
    for i in range(len(processes)):
        if i != naProcess:
            plt.scatter(releaseTimesPerProcess[i], executionTimesPerProcess[i], c='black', marker='x')


