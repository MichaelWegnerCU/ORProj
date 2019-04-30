#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 08:08:03 2019

@author: zanejakobs
"""

import AstVar as var
import pandas as pd
import numpy as np
import DataManager as dm
import MarkowitzOptimizer as mo
import QuantUtils as utl
from math import sqrt

corr = pd.read_csv("/Users/zanejakobs/Desktop/FIN_ORProj/ORProj/Data/Historical/Spearman10002200.csv")
corr = corr.select_dtypes(include=np.number)

timeId = 1000
sd, tkr = var.make_stdevs(timeId)
cov = var.make_covariance(timeId, corr, printErr=False)

rets = pd.read_csv("/Users/zanejakobs/Desktop/FIN_ORProj/ORProj/Data/Historical/BigReturnsMat.csv")
rets = rets.iloc[:, 1:]#rets.drop(columns=['Unnamed: 0'])
retsId = rets.iloc[timeId,:]

#test noisify_returns
realSd = np.std(retsId)
noisyRet = utl.noisify_returns(retsId, 0.0, 1.5*realSd)
print("pre-noise mean:", np.mean(retsId))
print("noisy mean:", np.mean(noisyRet))


#allocate max 5% to any one trade
max_position_size = 0.05
#dollar exposure between -0.05 and +0.25
min_dollar_exposure = -0.3
max_dollar_exposure = 0.3
#risk-neutral
risk_tolerance = 0.5
ERet = pd.DataFrame(retsId).transpose()

NERet = pd.DataFrame(noisyRet).transpose()

solDict = mo.markowitz_optimize(NERet, cov, 
                      max_position_size,
                      risk_tolerance,
                      min_dollar_exposure,
                      max_dollar_exposure,
                      out="Dict")
'''
print(solDict['long'])
print(solDict['short'])
print("Leverage:")
print(solDict['leverage'])
print("Dollar exposure:")
print(solDict['DollarExposure'])
print("Longs after re-keying:")
print(utl.all_key_to_ticker(solDict['long']))
'''
Ws = utl.dict_to_weight(solDict, ERet)
#print("Result of dict_to_weight:")
#print(Ws)
print("Realized one-day return:")
rret = 100 * Ws.dot(retsId)
print(rret, "percent.")
print("Realized standard deviation:")
rsd = 100 * sqrt(np.linalg.multi_dot([Ws ,cov, np.transpose(Ws)]) )
print(rsd, "percent.")
print("Realized Sharpe:")
print(rret/rsd)


#jan 18 2018 is 2025
print("Backtest from Dec. 12, 2017 to Jan18, 2018 with uniform noise:")

testMat1 = utl.markowitz_backtest(corr, 2000, 2025, max_position_size,
                                 risk_tolerance, min_dollar_exposure,
                                 max_dollar_exposure, noiseMu=0,
                                 noiseSdFact=5, dist="Unif")
print(testMat1)
print("Running test 2")
np.savetxt("../Data/Test/UnifNoise5.0/121217-011818Lin.csv", testMat1)

testMat2 = utl.markowitz_backtest(corr, 2000, 2025, max_position_size,
                                 risk_tolerance, min_dollar_exposure,
                                 max_dollar_exposure, noiseMu=0,
                                 noiseSdFact=6.5, dist="Unif")
print(testMat2)
print("Running test 3")
np.savetxt("../Data/Test/UnifNoise6.5/121217-011818Lin.csv", testMat2)


testMat3 = utl.markowitz_backtest(corr, 2000, 2025, max_position_size,
                                 risk_tolerance, min_dollar_exposure,
                                 max_dollar_exposure, noiseMu=0,
                                 noiseSdFact=8, dist="Unif")
print(testMat3)
np.savetxt("../Data/Test/UnifNoise8.0/121217-011818Lin.csv", testMat3)








