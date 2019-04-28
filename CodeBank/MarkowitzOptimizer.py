#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:13:02 2019

@author: zanejakobs
"""

import gurobipy as grb
import pandas as pd


'''
@author: Zane Jakobs
@param var: variances of equities
@param ER: expected returns
@param max_pos: max position size regardless of Kelly
@return: position size bounds
'''
def calc_max_pos(var,ER, max_pos):
    bounds = ER
    for i in range(len(ER)):
        kOpt = ER[0,i]/var[i]
        if kOpt > 0:
            if kOpt < max_pos:
                bounds[i] = kOpt
            else:
                bounds[i] = max_pos
        else:
            if kOpt > -max_pos:
                bounds[i] = kOpt
            else:
                bounds[i] = -max_pos



'''
Author: Zane Jakobs

Param expReturns: expected returns of each security as a Pandas dataframe.
Each column label must be the security's ticker, and the value in that
 column is the expected value.

Param expCov: expected covariance matrix as a numpy array

Param riskTol: risk tolerance factor. Input -1 to choose Kelly-optimal 
risk tolerances; NOT IMPLEMENTED YET

Param max_pos_size: maximum fraction of the portfolio to allocate to any
given position

Param max/min_dollar_exposure: maximum and minimum dollar exposures, which
will end up as max/min market beta

Param leverage_lb: lower bound for leverage of the model. Default >= 95% of 
capital must be allocated

Param leverage_ub: upper bound for leverage of the model. Default to no 
borrowing (max leverage 1)

Param name: name of the model

Param out: "Print" or "Write" for print to terminal or write to file.
"Dict" for dictionary to return

Param modLog: print model output log to console? default false

Return: Markowitz-optimal portfolio--that is, the w that solve the QP

min w^T * expCov * w - riskTol * w^T * r

s.t.

weights sum to within dollar exposure interval

abs val of weights sum to within leverage interval

individual weights are within the position size interval
'''
def markowitz_optimize(expReturns, expCov, max_pos_size, riskTol,
                   min_dollar_exposure, max_dollar_exposure,
                   leverage_lb = 0.95, leverage_ub = 1.0, 
                   name = 'Markowitz', out="Print",
                   modLog=False):
    
    mod = grb.Model(name)
    
    tickers = expReturns.columns
    nSec = len(tickers)
    #expected return values
    rets = expReturns.values
    #extract variances
    #var = np.diag(expCov)
    
    #one decision var per ticker with the given max size
    posWeights = pd.Series(mod.addVars(tickers, lb = 0,
                        ub = max_pos_size, name='Long'), index=tickers)
    negWeights = pd.Series(mod.addVars(tickers, lb = -max_pos_size,
                    ub = 0, name='Short'), index=tickers)
    mod.update()
    #risk = w^T * expCov * w 
    #adjusted return = riskTol* w^T * r

    objective = grb.QuadExpr() 
    
    for i in range(nSec):
        for j in range(nSec):
            objective += (posWeights.iloc[i]+ negWeights.iloc[i]) * expCov.iloc[i,j] * (posWeights.iloc[j] + negWeights.iloc[j])        
    for i in range(nSec):
        objective += -1.0 * riskTol * (posWeights.iloc[i] + negWeights.iloc[i]) * rets[0,i]
                             
    #minimize the objective
    mod.setObjective(objective, grb.GRB.MINIMIZE)
    mod.update()
    #min dollar exposure constraint
    mod.addConstr(posWeights.sum() + negWeights.sum() <= max_dollar_exposure)
    #max dollar exposure constraint
    mod.addConstr(posWeights.sum() + negWeights.sum() >= min_dollar_exposure)
    mod.update()
    #leverage constraints
    mod.addConstr(posWeights.sum() - negWeights.sum() <= leverage_ub)# * max_pos_size)
    mod.update()
    #set output flag to 0?
    if not modLog:
        mod.setParam('OutputFlag', 0)
        mod.update()
    #optimize
    mod.optimize()
    totLev = 0
    dolExp = 0
    if out == "Print":
        nL = []
        pL = []
        if mod.status == grb.GRB.Status.OPTIMAL:
            for w in mod.getVars():
                if w.X > 1.0e-9:
                    pL.append(w)
                    totLev += w.X
                    dolExp += w.X
                elif w.X < -1.0e-9:
                    nL.append(w)
                    totLev -= w.X
                    dolExp += w.X
            print("Long positions:")
            for long in pL:
                print("%s %.4E" % (long.Varname, long.X))
            print("Short positions:")
            for short in nL:
                print("%s %.4E" % (short.Varname, short.X))
                    #print("%s %f" % (w.Varname, w.X))
                    #totLev += abs(w.X)
            print("Total leverage:", totLev)
            print("Dollar exposure:",dolExp)
        else:
            print("Error: model status", mod.status)
    elif out == "Dict":
        dct = {}
        pdct = {}
        ndct = {}
        if mod.status == grb.GRB.Status.OPTIMAL:
            for w in mod.getVars():
                if w.X > 1.0e-7:
                    pdct[w.Varname] = w.X
                    totLev += w.X
                    dolExp += w.X
                elif w.X < -1.0e-7:
                    ndct[w.Varname] = w.X
                    totLev -= w.X
                    dolExp += w.X
            dct['long'] = pdct
            dct['short'] = ndct
            dct['leverage'] = totLev
            dct['DollarExposure'] = dolExp
            return dct
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    