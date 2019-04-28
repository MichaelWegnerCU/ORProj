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

corr = pd.read_csv("/Users/zanejakobs/Desktop/FIN_ORProj/ORProj/Data/Spearman20002200.csv")
corr = corr.select_dtypes(include=np.number)

timeId = 2113
sd, tkr = var.make_stdevs(timeId)
cov = var.make_covariance(timeId, corr, printErr=False)

rets = pd.read_csv("/Users/zanejakobs/Desktop/FIN_ORProj/ORProj/Data/Historical/BigReturnsMat.csv")
rets = rets.iloc[:, 1:]#rets.drop(columns=['Unnamed: 0'])
retsId = rets.iloc[timeId,:]
#allocate max 5% to any one trade
max_position_size = 0.05
#dollar exposure between -0.05 and +0.25
min_dollar_exposure = -0.3
max_dollar_exposure = 0.3
#risk-neutral
risk_tolerance = 0.5
ERet = pd.DataFrame(retsId).transpose()

solDict = mo.markowitz_optimize(ERet, cov, 
                      max_position_size,
                      risk_tolerance,
                      min_dollar_exposure,
                      max_dollar_exposure,
                      out="Dict")

print(solDict['long'])
print(solDict['short'])
print("Leverage:")
print(solDict['leverage'])
print("Dollar exposure:")
print(solDict['DollarExposure'])
