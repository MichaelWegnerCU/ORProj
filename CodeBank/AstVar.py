#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 16:14:19 2019

@author: zanejakobs

AST variance, defined here:
    https://www.sciencedirect.com/science/article/pii/S0304407610000266#fd1
"""
import math
import DataManager as dm
import numpy as np
from numba import jit

@jit
def K(x):
    num = math.gamma((x + 1.0) * 0.5)
    denom = math.sqrt(math.pi * x) * math.gamma(x*0.5)
    return num/denom

@jit
def B(a, v1, v2):
    return a * K(v1) + (1-a) * K(v2)

@jit
def astAstar(a,v1,v2):
    num = a * K(v1)
    return num/B(a,v1,v2)

@jit
def astVar(a, sigma, v1, v2):
    astar = astAstar(a,v1,v2)
    p1 = a*astar*astar * v1 / (v1 - 2) 
    p1 += (1 - a) * (1-astar) * (1-astar) *v2 / (v2-2)
    
    p2 = -1 * astar * astar * v1 / (v1 - 1) + (1-astar) * (1-astar)*v2/(v2-1)
    p2 = p2 * p2
    
    b = B(a,v1,v2)
    
    return sigma * sigma * (4* p1 - 16 * b * b * p2)
@jit
def astSD(a, sigma, v1, v2):
    var = astVar(a,sigma,v1,v2)
    return math.sqrt(10*var)/10000
    
    
#ssd = astSD( 0.513008,36.8294, 5.4932, 4)
#print(ssd)


#astPar = dm.get_params_time(1000)

#print(astPar['SLG']['scale'])

'''
@author: Zane Jakobs
@param index: index of parameters relative to once-differenced
sp1018 (starting Jan 5 2018, ending Dec. 28 2018)
@return: pair containing vector of standard deviations and list of 
tickers in order
'''
@jit
def make_stdevs(index):
    #get AST distribution parameters
    ASTParams = dm.get_params_time(index)
    #vector of standard deviations
    S = np.zeros(len(ASTParams))
    #iterate over dict
    it = 0
    tickers = []
    for t in ASTParams:
        #dist params
        dPars = ASTParams[t]
        #record ticker to preserve order
        tickers.append(t)
        #calc stdev
        S[it] = astSD(dPars['skewness'],
                        dPars['scale'],
                        dPars['shape'],
                        dPars['shape2'])
        it += 1
    return S, tickers


'''
@author: Zane Jakobs
@param index: index of parameters relative to once-differenced
sp1018 (starting Jan 5 2018, ending Dec. 28 2018)
@param corrMat: Pandas DataFrame containing correlation matrix of stocks
'''

def make_covariance(index, corrMat):
    #get stdevs and list of tickers in order
    S, tkr = make_stdevs(index)
    #verify that order is correct, change otherwise
    matchTix = corrMat.columns
    for i in range(len(S)):
        if tkr[i] != matchTix[i]:
            #if not equal, find equal val, swap
            try:
                swapID = matchTix.index(tkr[i])
                #if index found, swap
                tempT = tkr[i]
                tempS = S[i]
                
                tkr[i] = matchTix[swapID]
                S[i] = S[swapID]
                
                tkr[swapID] = tempT
                S[swapID] = tempS
            except:
                print("Error: corrMat does not contain ticker ", tkr[i], ".\n")
                #delete extra column and row
                #np.delete(corrMat, i, 0)
                #np.delete(corrMat, i, 1)
                #i -= 1
    #cov = S*corr*S
    #corr  = corrMat.values()
    S = np.diag(S) #vector -> diagonal matrix
    return np.matmul(S, np.matmul(corrMat, S))













    
