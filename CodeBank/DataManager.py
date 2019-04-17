import os
import re
import pandas as pd 
import numpy as np 

"""
Created on Saturday Apr 13 10:13:02 2019
@author: Michael Wegnerr
@brief: Returns historical price data for each stock ticker
@return: Dictionary with keys being Ticker and value being a dataframe of cleaned historical data
"""

def get_Ticker_prices():
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
	#This function will return a dictionary with the key being the ticker and the value being the dataframe of historical data    
	return(dict(list(All_Tickers.items())[0:2]))




# print(get_Ticker_prices())

"""
Created on Tue Apr 16
@author: Michael Wegnerr
@brief: Returns 2019 Forecast data
@Param1: Optinal to take in a ticker to only recieve the data for said ticker. If no input provided then whole dataset is returned
@return: A dictionary of the forecast data with key being the company ticker symbol
"""
def get_Forecast(op_tick=None):

	root_dir = '../Data/Forecasts'
	Forecasts={}

	for directory, subdirectories, files in os.walk(root_dir):
		for file in files:
			comp_name=re.search("(?<=forecast_)(.*?)(?=\.)", file)
			file_name="../Data/Forecasts/"+file
			Current_pd = pd.read_csv(file_name)
			Current_pd = Current_pd.loc[:, ~Current_pd.columns.str.contains('^Unnamed')]
			Forecasts[comp_name[0]]=Current_pd
	if op_tick==None:
		return(Forecasts)
	else:
		return({op_tick:Forecasts[op_tick]})

	
#For testing remove comment out when necesary
ticker_in="AAPL"
adam_q=get_Forecast(ticker_in)
data=adam_q[ticker_in]
print(data["Lo.95"])


"""
Created on Tue Apr 16 09:13:02 2019
@author: Michael Wegnerr
@brief: Returns historical market data for every market day in 2016,17,18
@return: Dictonary of market data with [date,open,high,low,close,volume,adjusted]
"""

def get_Market_data():
	Market_2016_df = pd.read_csv("../Data/Historical/market_2016.csv")
	##Market 2016 data only has data starting on the 4th of the year
	Market_2017_df = pd.read_csv("../Data/Historical/market_2017.csv")
	##Market 2017 data only has data starting on the 3rd of the year
	Market_2018_df = pd.read_csv("../Data/Historical/market_2018.csv")
	##Market 2018 data only has data starting on the 2nd of the year
	
	return(pd.concat([Market_2016_df, Market_2017_df,Market_2018_df], ignore_index=True, sort=False))

# ##Comment out when not testing
# print(get_Market_data().head())