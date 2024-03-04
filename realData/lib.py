import csv
import riskfolio as rp
import pandas as pd
import numpy as np

data = pd.read_csv('data.csv')
# first row is the header
data = data.iloc[1:]
# first 1001 rows are to be used for training and the rest for testing

# first column is the date
data = data.drop(columns=['Date'])
# convert to float
data = data.astype(float)
# split the data training is from rows 501 to 1500 and testing is from 1501 to 2000
train = data.iloc[0:500]

# calculate returns
Y = train.pct_change().dropna()

port = rp.Portfolio(returns=Y)

# Calculating optimal portfolio

# Select method and estimate input parameters:

method_mu='hist' # Method to estimate expected returns based on historical data.
method_cov='hist' # Method to estimate covariance matrix based on historical data.

port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

# Estimate optimal portfolio:

model='Classic' # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
rm = 'MV' # Risk measure used, this time will be variance
obj = 'Sharpe' # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
hist = True # Use historical scenarios for risk measures that depend on scenarios
rf = 0 # Risk free rate
l = 0 # Risk aversion factor, only useful when obj is 'Utility'

w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)

print(w)