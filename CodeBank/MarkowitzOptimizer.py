#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:13:02 2019

@author: zanejakobs
"""

import gurobipy as grb
import pandas as pd
import numpy as np

'''
Author: Zane Jakobs

Param expReturns: expected returns of each security as a Pandas dataframe.
Each column label must be the security's ticker, and the value in that
 column is the expected value.

Param expCov: expected covariance matrix as a numpy array

Param riskTol: risk tolerance factor. Input -1 to choose Kelly-optimal 
risk tolerances

Param max_pos_size: maximum fraction of the portfolio to allocate to any
given position

Param max/min_dollar_exposure: maximum and minimum dollar exposures, which
will end up as max/min market beta

Param leverage_lb: lower bound for leverage of the model. Default >= 95% of 
capital must be allocated

Param leverage_ub: upper bound for leverage of the model. Default to no 
borrowing (max leverage 1)

Param name: name of the model

Return: Markowitz-optimal portfolio--that is, the w that solve the QP

min w^T * expCov * w - riskTol * w^T * r

s.t.

weights sum to within dollar exposure interval

abs val of weights sum to within leverage interval

individual weights are within the position size interval
'''
def make_gurobi_QP(expReturns, expCov, max_pos_size, riskTol,
                   min_dollar_exposure, max_dollar_exposure,
                   leverage_lb = 0.95, leverage_ub = 1.0, name = 'Markowitz'):
    
    mod = grb.Model(name)
    
    tickers = expReturns.columns
    
    rets = expReturns.iloc[0]
    
    #one decision var per ticker with the given max size
    weights = pd.Series(mod.addVars(tickers, lb = -max_pos_size,
                        ub = max_pos_size, index = tickers) )
    #risk = w^T * expCov * w 
    risk = np.linalg.multi_dot(weights, expCov, weights)
    #adjusted return = riskTol* w^T * r
    adjRet = riskTol * rets.dot(weights)
    #minimize the objective
    objective = risk - adjRet
    
    mod.setObjective(objective, grb.GRB.MINIMIZE)
    #min dollar exposure constraint
    mod.addConstr(weights.sum() <= max_dollar_exposure)
    #max dollar exposure constraint
    mod.addConstr(weights.sum() >= min_dollar_exposure)
    #leverage constraints
    mod.addConstr(abs(weights).sum() >= leverage_lb)
    mod.addConstr(abs(weights).sum() <= leverage_ub)
    #set output flag to 0?  we'll see based on the output
    #mod.setParam('OutputFlag', 0)
    #optimize
    mod.optimize()
    return weights
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    