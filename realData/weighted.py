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
    weighted_portfolio_value = np.dot(weights, portfolio_value)
    expected_log_value = -np.mean(np.log(weighted_portfolio_value))
    return expected_log_value

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
filePaths = ["ADANIPORTS.csv","ASIANPAINT.csv", "AXISBANK.csv","HDFC.csv","ITC.csv","TCS.csv","HINDUNILVR.csv","INFY.csv","LT.csv","ICICIBANK.csv","RELIANCE.csv","KOTAKBANK.csv","HEROMOTOCO.csv","MARUTI.csv","WIPRO.csv","HCLTECH.csv"]
n_stocks = len(filePaths)
n_days = 1000
# keep last 1000 lines
for i in filePaths:
    keep_last_1000_lines(i)

for i in filePaths:
    tempReturns.append(getStockData(i))

# Weighting scheme (exponential decay)
decay_factor = 0.95  # You can adjust this parameter
weights = np.array([decay_factor**(n_days - i - 1) for i in range(n_days)])
# print("Weights:", weights)

returns = np.array(tempReturns)
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
result = minimize(objective_function, initial_b, args=(returns,weights), constraints=[constraint,individual_stock_constraint], bounds=bounds)

# Optimal fractions
optimal_b = result.x

print("Optimal fractions:", optimal_b)
