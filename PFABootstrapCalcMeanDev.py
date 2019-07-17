#!/usr/bin/env python
import math
import numpy as np
import scipy.stats as stats

nGenerated = 100
nEstimateDeltaFeatures = 100
nZDeltas = 100

def calcT(measuredW, expW, varW):
    tmp = 0
    for i in range(len(measuredW)):
        tmp += np.square(measuredW[i] - expW)/varW
    return tmp/len(measuredW)


def estimateEmpiricalLogProbability(z, samples, timeInterval):
    halfInterval = timeInterval/2
    logProbabilities = np.zeros(len(z))
    for i in range(len(z)):
        val = z[i]
        intervalMin = val - halfInterval
        intervalMax = val + halfInterval
        count = np.count_nonzero(np.where((intervalMin < samples) & (samples < intervalMax)))
        logProbabilities[i] = np.log(count + 1)
    return logProbabilities
            
def estimateZDelta(z, sampleFrom):
    indicesZ = np.random.randint(len(z), size=(nEstimateDeltaFeatures))
    indicesSampleFrom = np.random.randint(len(sampleFrom), size=(nEstimateDeltaFeatures))
    bootStrapZ = z[indicesZ]
    bootStrapSampleFrom = sampleFrom[indicesSampleFrom]
    bootStrapZDelta = bootStrapZ - bootStrapSampleFrom
    zDeltaMean = np.mean(bootStrapZDelta)
    zDeltaStdDev = np.std(bootStrapZDelta)
    return zDeltaMean, zDeltaStdDev
   
            

def calcPFABootstrapMeanDev(z, sampleFrom):
    print("length z", len(z))
    print("length sampleFrom", len(sampleFrom))
    zDeltaMean, zDeltaStdDev = estimateZDelta(z, sampleFrom)
    print(zDeltaMean, zDeltaStdDev)
    timeInterval = np.std(sampleFrom)
    print("timeinterval: ", timeInterval)
    # sample zDeltas
    zDeltas = np.random.normal(zDeltaMean, zDeltaStdDev, nZDeltas)
    betas = np.zeros(nZDeltas)    
    sampleFromMean = np.mean(sampleFrom)    
    sampleFromStdDev = np.std(sampleFrom)
    for i in range(nZDeltas):
        indices = np.random.randint(len(sampleFrom), size=(nGenerated, len(z)))
        generatedData = sampleFrom[indices]
        translatedData = z - zDeltas[i]
        logLikelihoodsData = estimateEmpiricalLogProbability(translatedData, sampleFrom, timeInterval)
        logLikelihoodsGen = np.zeros((nGenerated, len(z)))
        for j in range(nGenerated):
            logLikelihoodsGen[j] = \
            estimateEmpiricalLogProbability(generatedData[j], sampleFrom, timeInterval) 
        expW = np.mean(logLikelihoodsGen)
        varW = np.var(logLikelihoodsGen)
        measuredT = calcT(logLikelihoodsData, expW, varW)
        generatedT = np.zeros(nGenerated)
        for k in range(nGenerated):
            generatedT[k] = calcT(logLikelihoodsGen[k], expW, varW)
        betas[i] = np.count_nonzero(generatedT <= measuredT)/nGenerated
    print(betas)
    betaMean = np.mean(betas)
    PFA = min(betaMean, 1-betaMean)
    print("PFA mean:", PFA)
    return 



        
        
  

