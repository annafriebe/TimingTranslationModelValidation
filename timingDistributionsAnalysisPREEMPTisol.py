#!/usr/bin/env python
import math
import numpy as np
import cluster
import minSqErrPeriodEstimate
import switchDataForCPU
import drawTimingDistributions
import PFABootstrapCalcMeanDev


def periodicAdjustedTimes(times, period, factor = 1):
    periodicAdjustedTimes = np.zeros(len(times))
    for i in range(len(times)):
        periodicAdjustedTimes[i] = ((times[i]* factor) % period) / factor
    return periodicAdjustedTimes


def getProcessStates(previousProcessList):
    states = np.zeros(len(previousProcessList), dtype=int)
    processes = []
    processCount = []
    for i in range(len(previousProcessList)):
        process = previousProcessList[i]
        if not process in processes:
            processes.append(process)
            processCount.append(0)
        states[i] = processes.index(process)
        processCount[processes.index(process)] += 1
    print('processes')
    print(processes)
    print('number of samples')
    print(processCount)
    return len(processes), states

def getTwoProcessStates(previousProcessList):
    states = np.zeros(len(previousProcessList), dtype=int)
    for i in range(len(previousProcessList)):
        process = previousProcessList[i]
        if process.startswith("simplePeriodic") or process == '':
            states[i] = 0
        else:
            states[i] = 1
    return states



np.random.seed(300)

switchWakeupData = getSwitchAndWakeupDataForCPU('20190514_preempt_100_isol-report', '[003]')

releaseTimeDict, schedulingTimeDict, executionTimeDict, previousProcessList,\
wakeupInLatencyProcessList, wakeupInExecutionProcessList = \
getTimeDicts(switchWakeupData, 'simplePeriodic')

factor = 1

estimatedPeriod = int(factor * periodEstimate(releaseTimeDict['all'], 10000000) + 0.5)
print("Estimated period from release times:", estimatedPeriod)

allSchedulingTimes = np.zeros(0)
allReleaseTimes = np.zeros(0)

for item in releaseTimeDict:
    releaseTimeDict[item] = periodicAdjustedTimes(releaseTimeDict[item], estimatedPeriod, factor)
    if item == 'all':
        allReleaseTimes = releaseTimeDict[item]

for item in schedulingTimeDict:
    schedulingTimeDict[item] = periodicAdjustedTimes(schedulingTimeDict[item], estimatedPeriod, factor)
    if item == 'all':
        allSchedulingTimes = schedulingTimeDict[item]

print("wakeup in latency")
nWakeupInLatency, WILprocesses = getProcessStates(wakeupInLatencyProcessList)
print("wakeup in execution")
nWakeupInExecution, WIEprocesses = getProcessStates(wakeupInExecutionProcessList)

schedulingReleaseDiff = allSchedulingTimes - allReleaseTimes
    
        
nProcesses, processes = getProcessStates(previousProcessList)
twoProcesses = getTwoProcessStates(previousProcessList)

timesPerTwoProc, schedulingReleaseDiffPerTwoProc, executionTimesPerTwoProc = \
splitTimesPerCluster(schedulingReleaseDiff, executionTimeDict['all'], twoProcesses, 2)


print("bootstrap intermediate processes latency")
calcPFABootstrapMeanDev(schedulingReleaseDiffPerTwoProc[1], \
                        schedulingReleaseDiffPerTwoProc[0])
print("bootstrap intermediate processes execution time")
calcPFABootstrapMeanDev(executionTimesPerTwoProc[1], \
                        executionTimesPerTwoProc[0])


drawTimeHistInRange(schedulingReleaseDiffPerTwoProc[0], "latencies (ns), no intermediate processes", [4000, 9000])
drawTimeHistInRange(schedulingReleaseDiffPerTwoProc[1], "latencies (ns), intermediate processes", [4000, 9000])

drawTimeHistInRange(executionTimesPerTwoProc[0], "execution times (ns), no intermediate processes", [8000, 22000])
drawTimeHistInRange(executionTimesPerTwoProc[1], "execution times (ns), intermediate processes", [8000, 22000])

drawTimesPerTwoProcess(schedulingReleaseDiff, executionTimeDict['all'], processes, "latencies (ns)", "execution times (ns)", "Intermediate processes", 1)





         
