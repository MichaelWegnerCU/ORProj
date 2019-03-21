Forecast data:

	For each security, there is one .csv file containing forecasted points from the conditional mean model, which, in this iteration, is an ARIMAX model on the log-returns, with the external regressors being CAPM + trading volume (NB: the Capital Asset Pricing Model, CAPM, is the "Fama-French"-like factor model with market price/returns as the only factor). The leftmost column, an increasing sequence of integers, is an index column; the second column from the left, 'Forecast', contains the forecasted conditional mean at the given index. Lo 80 is the threshold of the 20th percentile of forecasted returns, Hi 80 the threshold for the 80th percentile of returns, and so on with Lo 95 and Hi 95. Note, however, that these estimates of percentiles are forecasted assuming normally distributed log-returns, which is very much NOT the case for the forecasted series. Until I can get the simulations for the GAS model for conditional variance written and working, a decent heuristic is that the standard deviation of the price at a given time step is 

	SD(t) ~ Hi80(t) - Lo80(t),

	the difference between the 80th and 20th percentiles of prices. This is a slight overestimate of the SD for a normal distribution, but since the empirical distribution has fatter tails than a normal, this is a decent estimate for just getting model frameworks written.

	