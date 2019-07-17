#!/usr/bin/env python
def calcSumi(n):
    sumi = 0
    for i in range(n):
        sumi += i
    return sumi

def calcSumiSq(n):
    sumiSq = 0
    for i in range(n):
        sumiSq += i*i
    return sumiSq

def calcSumTimes(times):
    sumTimes = 0
    for time in times:
        sumTimes += time
    return sumTimes
        
def calcSumiTimes(times, n):
    sumiTimes = 0
    for i in range(n):
        sumiTimes += i*times[i]
    return sumiTimes    
        
def periodEstimate(times, approximatePeriod):
    n = len(times)
    sumi = calcSumi(n)
    sumiSq = calcSumiSq(n)
    sumTimes = calcSumTimes(times)
    sumitimes = calcSumiTimes(times, n)
    numerator = sumi*sumTimes/n - sumitimes
    denominator = sumi*sumi/n - sumiSq
    estimatedPeriod = numerator/ denominator
    print("period estimate min sq err", estimatedPeriod)
    return estimatedPeriod





