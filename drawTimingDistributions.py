#!/usr/bin/env python
import math
import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt

 
def drawSeqTimesAutoCorr(times, timesString, xlines=[]):
    plt.figure()
    title = "Sequential " + timesString
    plt.title(title)
    plt.plot(times)
    autoCorr = np.correlate(times, times, mode='full')
    etNorm = 0
    for i in range(len(times)):
        etNorm += times[i]**2
    autoCorr = autoCorr[(int)(autoCorr.size/2):]/etNorm
    plt.figure()
    title = "Autocorrelation function " + timesString
    plt.title(title)
    plt.plot(autoCorr)
    plt.xlim(0, 50)
    plt.ylim(0.8, 1.0)
    for item in xlines:
        plt.axvline(x=item)

def drawTimeHistInRange(times, title, xRange):
    plt.figure()
    plt.title(title)
    plt.hist(times, bins=70, range=xRange)

def drawTimesPerProcess(releaseTimes, executionTimes, processes, xlabel = "", ylabel = "", title = ""):
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
    cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    plt.figure()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    for i in range(10):
        plt.scatter(releaseTimesPerProcess[i], executionTimesPerProcess[i], c=cycle[i])


