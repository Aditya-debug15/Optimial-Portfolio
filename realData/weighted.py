import numpy as np
import csv
from scipy.optimize import minimize

def getStockData(filePath):
    with open(filePath, 'r') as file:
        csvReader = csv.reader(file)
        next(csvReader)
        temp = []
        for row in csvReader:
            temp.append(float(row[9]))
        return temp

# Objective function (negative of expected log portfolio value)
def objective_function(b, returns, weights):
    portfolio_value = np.dot(b, returns)
    
    # Calculate the log portfolio value
    log_portfolio_value = np.log(portfolio_value)
    # take mean
    # mean_log_portfolio_value = np.mean(log_portfolio_value)
    # return -mean_log_portfolio_value  # Return the negative value for minimization
    
    # Calculate the weighted mean of the log portfolio value
    weighted_mean_log_portfolio = np.sum(log_portfolio_value * weights) / np.sum(weights)    
    return -weighted_mean_log_portfolio  # Return the negative value for minimization

    
def keep_last_1000_lines(input_file):
    with open(input_file, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        lines = list(csv_reader)[-1000:]

    with open(input_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
        csv_writer.writerows(lines)

# Constraint: sum of fractions equals 1
constraint = ({'type': 'eq', 'fun': lambda b: np.sum(b) - 1})

individual_stock_constraint = ({'type': 'ineq', 'fun': lambda b: b - 0.05})  # Adjust the threshold as needed

# Generate random returns
tempReturns = []
# filePaths = [ "AXISBANK.csv","HDFC.csv","ITC.csv","TCS.csv","INFY.csv","LT.csv","ICICIBANK.csv","RELIANCE.csv","KOTAKBANK.csv","HEROMOTOCO.csv","MARUTI.csv","WIPRO.csv","HCLTECH.csv"]
filepath = "data.csv"
start = '2016-01-01'
end = '2019-12-30'

# Tickers of assets
assets = ['JCI', 'TGT', 'CMCSA', 'CPB', 'MO', 'APA', 'MMC', 'JPM',
          'ZION', 'PSA', 'BAX', 'BMY', 'LUV', 'PCAR', 'TXT', 'TMO',
          'DE', 'MSFT', 'HPQ', 'SEE', 'VZ', 'CNP', 'NI', 'T']
# creat a 2d array to store the stock values
stockValues = [[] for i in range(len(assets))]
dict = {}
count=0
with open(filepath, 'r') as file:
    csvReader = csv.reader(file)
    # get the header from the first line
    header = next(csvReader)
    # print(header)
    # find the column numbers of the assets in header
    for i in range(len(header)):
        if header[i] in assets:
            dict[header[i]] = i
    print(dict)
    # now extract the corresponsing stock values
    for row in csvReader:
        # check if the date is in the range
        # if row[0] < start or row[0] > end:
        #     continue
        count+=1
        for i in range(len(assets)):
            stockValues[i].append(float(row[dict[assets[i]]]))
    
    
n_stocks = len(assets)
n_days = count
# # keep last 1000 lines
# for i in filePaths:
#     keep_last_1000_lines(i)

# for i in filePaths:
#     tempReturns.append(getStockData(i))

# Weighting scheme (exponential decay)
decay_factor = 0.95  # You can adjust this parameter
weights = np.array([decay_factor**(n_days - i - 1) for i in range(n_days)])
# print("Weights:", weights)

returns = np.array(stockValues)
# print("Original returns:")
# print(returns)

# Normalize returns based on the first day
returns /= returns[:, 0][:, np.newaxis]
# print("Normalized returns:")
# print(returns)

# Initial guess for the fractions
initial_b = np.ones(n_stocks) / n_stocks

# Define the bounds
b = (0, 1)
bounds = [b for _ in range(n_stocks)]

# Optimization
result = minimize(objective_function, initial_b, args=(returns,weights), constraints=[constraint], bounds=bounds)

# Optimal fractions
optimal_b = result.x
# print the optimal fractions along with the stock names
print("Optimal fractions:")
for i in range(n_stocks):
    #remove csv extension
    # round off to 3 decimal places
    print(assets[i], round(optimal_b[i], 3))