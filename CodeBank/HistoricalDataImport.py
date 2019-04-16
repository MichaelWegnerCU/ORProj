
# @author: Michael Wegnerr
# @brief: Returns historical price data for each stock ticker
# @return: Dictionary with keys being Ticker and value being a dataframe of cleaned historical data

import pandas as pd 
import numpy as np 

def get_Tickers_prices():
	Price_2016_df = pd.read_csv("../Data/Historical/prices_2016.csv")
	##Removing the company "WY" which only appears in the 2016 data set
	Price_2016_df = Price_2016_df[Price_2016_df.symbol != "WY"]

	Price_2017_df = pd.read_csv("../Data/Historical/prices_2017.csv")
	Price_2018_df = pd.read_csv("../Data/Historical/prices_2018.csv")

	known_tickers=Price_2016_df.symbol.unique()

	ticker_2016 ={}
	ticker_2017 ={}
	ticker_2018 ={}
	for t in known_tickers:
	    ticker_2016[t] = Price_2016_df.loc[Price_2016_df['symbol'] == t]
	    ticker_2017[t] = Price_2017_df.loc[Price_2017_df['symbol'] == t]
	    ticker_2018[t] = Price_2018_df.loc[Price_2018_df['symbol'] == t]
	    
	All_Tickers={}
	for t in known_tickers:
	    All_Tickers[t]=pd.concat([ticker_2016[t], ticker_2017[t],ticker_2018[t]], ignore_index=True, sort=False)
	    
	return(dict(list(All_Tickers.items())[0:2]))

