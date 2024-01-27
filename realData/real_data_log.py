import numpy as np
import csv
from scipy.optimize import minimize

def getStockData(filePath):
    with open(filePath, 'r') as file:
        csvReader = csv.reader(file)
        next(csvReader)
        temp = []
        # print(header)
        for row in csvReader:
            temp.append(float(row[9]))
        return temp


# Objective function (negative of expected log portfolio value)
def objective_function(b, returns):
    portfolio_value = np.dot(b, returns)
    expected_log_value = -np.mean(np.log(portfolio_value))
    return expected_log_value

# Constraint: sum of fractions equals 1
constraint = ({'type': 'eq', 'fun': lambda b: np.sum(b) - 1})

# Number of stocks and days
n_stocks = 2
n_days = 100

# Generate random returns
tempReturns = []
filePaths = ["ASIANPAINT.csv", "AXISBANK.csv"]
for i in filePaths:
    tempReturns.append(getStockData(i))

print(tempReturns)

for i in range(n_stocks):
    for j in range(1,n_days):
        tempReturns[i][j] = tempReturns[i][j]/tempReturns[i][0]
    tempReturns[i][0] = 1

returns = np.array(tempReturns)
print(returns)
# Initial guess for the fractions
initial_b = np.ones(n_stocks) / n_stocks

# Define the bounds
b = (0,1)
bounds = [b for _ in range(n_stocks)]


# Optimization
result = minimize(objective_function, initial_b, args=(returns,), constraints=constraint, bounds=bounds)

# Optimal fractions
optimal_b = result.x

print("Optimal fractions:", optimal_b)
