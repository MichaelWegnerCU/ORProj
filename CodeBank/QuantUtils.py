#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 08:53:47 2019

@author: zanejakobs
"""
import pandas as pd
import numpy as np
from numba import jit

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
    
    if not isinstance(price_series, pd.DataFrame):
        raise Exception('price_series must by a Pandas dataframe, but it is of type',type(price_series))
        
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





