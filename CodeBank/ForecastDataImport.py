"""
Created on Tue Apr 16
@author: Michael Wegnerr
@brief: Returns 2019 Forecast data
@return: A dictionary of the forecast data with key being the company ticker symbol
"""
import os
import re
import pandas as pd 
import numpy as np 

def get_Forecast():

	root_dir = '../Data/Forecasts'
	Forecasts={}

	for directory, subdirectories, files in os.walk(root_dir):
		for file in files:
			comp_name=re.search("(?<=forecast_)(.*?)(?=\.)", file)
			file_name="../Data/Forecasts/"+file
			Current_pd = pd.read_csv(file_name)
			Current_pd = Current_pd.loc[:, ~Current_pd.columns.str.contains('^Unnamed')]
			Forecasts[comp_name[0]]=Current_pd
	return(Forecasts)

	
#For testing remove comment out when necesary
print(get_Forecast())

