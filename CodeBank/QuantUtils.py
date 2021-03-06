#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 08:53:47 2019

@author: zanejakobs
"""
import pandas as pd
import numpy as np
from numba import jit
import MarkowitzOptimizer as mo
from math import sqrt
import AstVar as var

'''
Author: Zane Jakobs

Param rets: numpy array of returns

Param mu: mean of Gaussian noise to add, or lower bound on uniform

Param sd: standard deviation of Gaussian noise to add, or upper bound on uniform

Param dist: normal ("Norm") or uniform ("Unif") distribution?

ASSUMPTION NOTE: WE'RE ADDING GAUSSIAN NOISE, SO WE'LL BE DISTORTING
THE RETURNS DISTRIBUTION BY MAKING IT MORE GAUSSIAN (SINCE THE NORMAL
IS A STABLE DISTRIBUTION). 
'''
@jit
def noisify_returns(rets, mu, sd, dist="Norm"):
    if dist == "Norm":
        noise = np.random.normal(mu, sd, rets.shape)
    elif dist == "Unif":
        noise = np.random.uniform(-1*sd,sd,rets.shape)
    noisyRets = rets + noise
    return noisyRets

'''
Author: Zane Jakobs

Param key: key in dictionary; MUST BE DICTIONARY OUTPUT 
FROM CALL TO markowitz_optimize() 

Return: ticker corresponding to that key
'''
def key_to_ticker(key):
    return key[(key.find("[") + 1):key.find("]")]

#applies above to whole dict
@jit
def all_key_to_ticker(dct):
    newDct = {}
    for key in dct.keys():
        knew = key_to_ticker(key)
        newDct[knew] = dct[key]
    return newDct


'''
Author: Zane Jakobs

Param dct: result of call to markowitz_optimize(... ,out="Dict",...) 

Param ret: Pandas dataframe of returns in the same format
as the expReturns parameter of markowitz_optimize(...)

Return: numpy array of portfolio weights aligned with
correct spot relative to returns vector and covariance matrix
'''
@jit
def dict_to_weight(dct, ret):
    #ordered tickers
    tkr = ret.columns
    #return values to turn into output
    r = ret.values
    #get longs and shorts
    longs = all_key_to_ticker(dct['long'])
    shorts = all_key_to_ticker(dct['short'])
    #loop through tickers and emplace weights
    vecId = 0
    for t in tkr:
        if t in longs:
            r[0,vecId] = longs[t]
            vecId += 1
        elif t in shorts:
            r[0,vecId] = shorts[t]
            vecId += 1
        else:
            r[0,vecId] = 0
            vecId += 1
    return r
    

'''
Author: Zane Jakobs

Param price_series: Pandas dataframe with column "adjusted"
that contains adjusted prices of the security, column 
"symbol" containing the security's ticker, and column 
"date"

Param n: how many (trading) days per period?

Return: dataframe containing dates, ticker, and n-day returns
for each day in the range of the date column, minus the first n.
Column names are, in order of ticker, date, return, 'symbol', 'date','adjusted'
'''
@jit
def n_day_returns(price_series, n):
    
    assert isinstance(price_series, pd.DataFrame)
        
    rows = price_series.shape[0]
    
    returns = price_series[['symbol','date','adjusted']]
    

    for i in range(n,rows):
        #return is (new price - old price)/(old price)
        returns[i,2] = (returns[i,2] - returns[i-n, 2])/(returns[i-n, 2])
    
    returns = returns[n:,:]
    return returns

'''
Author: Zane Jakobs

Param weights: numpy array (col vector) containing weights of security k (k being an index 
ranging from 1 to ~500) in the portfolio
Param rets: numpy array (col vector) containing realized returns of security k 
over the backtest period

Return: what would the portfolio returns have been if we ran this strategy?
NOTE: THIS IGNORES SLIPPAGE, TRANSACTION COSTS (INCLUDING BROKERAGE FEES), 
DROPOUT BIAS (FIRMS GOING BANKRUPT/DROPPING OFF EXCHANGE), AND MANY OTHER 
IMPRTANT CONSIDERATIONS. DO NOT USE THIS ON A REAL PORTFOLIO.
'''
@jit
def portfolio_return(weights, rets):
    wRows = weights.shape[0]
    wCols = weights.shape[1]
    
    rRows = rets.shape[0]
    rCols = rets.shape[1]
    
    if wRows != rRows:
        raise Exception('Weights and rets must have the same number of rows')
        
    if wCols != 1 or rCols != 1:
        raise Exception('Weights and rets must have exactly 1 column')
        
    #realized portfolio return is w^T * r
    return np.asscalar(np.matmul(np.transpose(weights), rets))



'''
Author: Zane Jakobs

Param weights: pandas DataFrame containing column of tickers called 'symbol' and 
a column of weights of securities in the portfolio called 'weight'
Param daily_data: pandas DataFrame of stock data with (at least) columns 'symbol'
and 'adjusted'

Return: daily variance of the portfolio over one backtest period
NOTE: THIS IGNORES SLIPPAGE, TRANSACTION COSTS (INCLUDING BROKERAGE FEES), 
DROPOUT BIAS (FIRMS GOING BANKRUPT/DROPPING OFF EXCHANGE), AND MANY OTHER 
IMPRTANT CONSIDERATIONS. DO NOT USE THIS ON A REAL PORTFOLIO.
'''
@jit
def daily_portfolio_variance(weights, daily_data):
    #sort
    weights = weights.sort_values(b=['symbol'])
    
    daily_var = weights['weight']
    
    wRows = weights.shape[0]
    
    for t in range(wRows):
        equityDf = daily_data.loc[daily_data['symbol'] == weights['symbol'][t] ]
        dailyRet = n_day_returns(equityDf, 1)
        dailyRet = dailyRet['adjusted']
        #calculate variance
        daily_var[t] = np.var(dailyRet)
        
    #square weights
    squareW = np.power(weights['weight'], 2)
    #var[ sum over i of a_iX_i] = sum over i of ( a_i^2 * var(X_i))
    return np.asscalar(np.matmul(np.transpose(squareW), daily_var))

'''
Author: Zane Jakobs

Notes: not using JIT compilation, since it won't be able to deduce the 
return type; if it turns out that all by options return the same type, then
the return type should be specified if possible. However, I suspect that
since the return dataframes contain both strings and floating point types,
numba won't have that as a settable type

Param returns: Pandas DataFrame of expected returns. Each column label
must be the equity's ticker, and the value in that column is the 
expected value. NOTE THAT THIS IS THE OPPOSITE CONVENTION OF THE ONE 
USED IN DAILY_PORTFOLIO_VARIANCE, AND IS NECESSARY FOR THE 
GUROBI SOLVER

Param nlong: pick the nlong equities w/ largest forecast returns

Param nshort: pick the nshort equities w/ largest negative (smallest) forecast
returns.

Param by: criterion for selecting equities:
    "Return" goes on expected returns only. 
    POSSIBLY TO BE ADDED IN THE FUTURE: selection based on Sharpe, Sortino
    ratios.

Return: equities we should look to trade, which 
'''
def select_equities(returns, nlong = 200, nshort = 200, by="Return"):
    if by == "Return":
        #sort by row, which contains the forecasted returns
        sortedRets = returns.sort_values(by = 1, ascending = False, axis=1)
        #pick longs and shorts
        longs = sortedRets.loc[0:nlong]
        shorts = sortedRets.loc[-nshort:]
        #join along columns
        tradeableEquities = pd.concat([longs,shorts], axis=1)
        return tradeableEquities
    
@jit
def markowitz_one_day_test(ERets, realRets, covMat,  max_position_size,
                           risk_tolerance, min_dollar_exposure,
                           max_dollar_exposure):
    testRes = mo.markowitz_optimize(ERets, covMat, max_position_size,
                                    risk_tolerance, min_dollar_exposure,
                                    max_dollar_exposure, out="Dict")
    Ws = dict_to_weight(testRes, ERets)
    realizedRet = Ws.dot(realRets)
    realizedSD =  sqrt(np.linalg.multi_dot([Ws ,covMat, np.transpose(Ws)]) )
    return realizedRet, realizedSD
    
    

def get_BigReturnsMat():
    return pd.read_csv("../Data/Historical/BigReturnsMat.csv")




'''
Author: Zane Jakobs

Brief: run backtest for Markowitz optimizer over one covariance matrix

Return: array of daily returns in order
'''
@jit
def markowitz_backtest(corrMat, startId, endId, maxPos, riskTol, 
                       minDol, maxDol, noiseMu=0.0, noiseSdFact=0.0,
                       dist="Norm"):
    testLen = endId - startId
    assert testLen > 0
    
    rets = get_BigReturnsMat()
    rets = rets.iloc[:, 1:]#rets.drop(columns=['Unnamed: 0'])
    
    dataHolder = np.zeros((testLen,2))
    for day in range(testLen):
        sd, tkr = var.make_stdevs(startId + day)
        cov = var.make_covariance(startId + day, corrMat, printErr=False)
        retsId = rets.iloc[startId + day,:]
        if noiseSdFact > 0:
            realSd = np.std(retsId)
            noisyRet = noisify_returns(retsId, noiseMu, noiseSdFact*realSd, dist)
        else:
            noisyRet = retsId
        
        noisyRet = pd.DataFrame(noisyRet).transpose()
        ret, risk = markowitz_one_day_test(noisyRet, retsId, cov,
                                           maxPos, riskTol, minDol,
                                           maxDol)
        dataHolder[day,0] = ret
        dataHolder[day,1] = risk
    return dataHolder














