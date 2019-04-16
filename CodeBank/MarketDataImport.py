# @author: Michael Wegnerr
# @brief: Returns historical market data for every market day in 2016,17,18
# @return: Dictonary of market data with [date,open,high,low,close,volume,adjusted]

import pandas as pd 
import numpy as np 

def get_Market_data():
	Market_2016_df = pd.read_csv("../Data/Historical/market_2016.csv")
	##Market 2016 data only has data starting on the 4th of the year
	Market_2017_df = pd.read_csv("../Data/Historical/market_2017.csv")
	##Market 2017 data only has data starting on the 3rd of the year
	Market_2018_df = pd.read_csv("../Data/Historical/market_2018.csv")
	##Market 2018 data only has data starting on the 2nd of the year
	
	return(pd.concat([Market_2016_df, Market_2017_df,Market_2018_df], ignore_index=True, sort=False))

##Comment out when not testing
print(get_Market_data().head())