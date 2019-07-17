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
    print(processes)
    print(processCount)
#    print(states)
    return len(processes), states

def getTwoProcessStates(previousProcessList):
    states = np.zeros(len(previousProcessList), dtype=int)
    for i in range(len(previousProcessList)):
        process = previousProcessList[i]
        if process.startswith("simplePeriodic") or process == '':
            states[i] = 0
        else:
            states[i] = 1
#    print(states)
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

nWakeupInLatency, WILprocesses = getProcessStates(wakeupInLatencyProcessList)
nWakeupInExecution, WIEprocesses = getProcessStates(wakeupInExecutionProcessList)
print(nWakeupInLatency, nWakeupInExecution)

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


WILperTwoProc, WIEperTwoProc = splitLabelsPerCluster(WILprocesses, WIEprocesses, twoProcesses, 2)
        
    
responseTimes = schedulingReleaseDiff +  executionTimeDict['all']

WilWieLabels, nWilLieLabels, labelDict = mergeLabels(WILprocesses, WIEprocesses, nWakeupInLatency, nWakeupInExecution)

timesPerWakeupCluster, schedulingReleaseDiffPerWakeupCluster, executionTimesPerWakeupCluster = \
splitTimesPerCluster(schedulingReleaseDiff, executionTimeDict['all'], WilWieLabels, nWilLieLabels)

noWakeupLabel = labelDict[0]
WIELabel = labelDict[1]

drawTimesPerProcess(schedulingReleaseDiff, executionTimeDict['all'], WilWieLabels,  "latency (ns)", "execution time (ns)", "Wakeup in execution")

print("bootstrap wakeup in execution (execution), all")
calcPFABootstrapMeanDev(executionTimesPerWakeupCluster[WIELabel], \
                        executionTimesPerWakeupCluster[noWakeupLabel])


WilWieLabels, nWilLieLabels, labelDict = mergeLabels(WILperTwoProc[0], WIEperTwoProc[0], nWakeupInLatency, nWakeupInExecution)

timesPerWakeupCluster, schedulingReleaseDiffPerWakeupCluster, executionTimesPerWakeupCluster = \
splitTimesPerCluster(schedulingReleaseDiffPerTwoProc[0], executionTimesPerTwoProc[0], WilWieLabels, nWilLieLabels)

print(len(schedulingReleaseDiffPerWakeupCluster[labelDict[0]]))
print(len(schedulingReleaseDiffPerWakeupCluster[labelDict[1]]))
noWakeupLabel = labelDict[0]
WIELabel = labelDict[1]
print(nWilLieLabels)

print("bootstrap wakeup in exectution, no intermediate")
calcPFABootstrapMeanDev(executionTimesPerWakeupCluster[WIELabel], \
                        executionTimesPerWakeupCluster[noWakeupLabel])


drawTimeHistInRange(schedulingReleaseDiff, "all latencies (ns)", [4000, 9000])
drawTimeHistInRange(schedulingReleaseDiffPerTwoProc[0], "latencies (ns), no intermediate processes", [4000, 9000])
drawTimeHistInRange(schedulingReleaseDiffPerTwoProc[1], "latencies (ns), intermediate processes", [4000, 9000])
drawTimeHistInRange(executionTimeDict['all'], "all execution times (ns)", [8000, 22000])
drawTimeHistInRange(executionTimesPerTwoProc[0], "execution times (ns), no intermediate processes", [8000, 22000])
drawTimeHistInRange(executionTimesPerTwoProc[1], "execution times (ns), intermediate processes", [8000, 22000])



drawTimesPerProcess(schedulingReleaseDiffPerTwoProc[0], executionTimesPerTwoProc[0], WilWieLabels,  "latency", "execution time")

wakeupStrings = [" no wakeup", " wakeup in execution"]
for i in range(2):
    title = "execution times (ns) for" + wakeupStrings[i]
    drawTimeHistInRange(executionTimesPerWakeupCluster[labelDict[i]], title, [8000, 22000])

drawTimesPerProcess(schedulingReleaseDiff, executionTimeDict['all'], processes, "latencies (ns)", "execution times (ns)", "Intermediate processes")


drawSeqTimesAutoCorr(allReleaseTimes, "release times")
drawSeqTimesAutoCorr(schedulingReleaseDiff, "latencies")
drawSeqTimesAutoCorr(executionTimeDict['all'], "execution times", [2, 4])





         
