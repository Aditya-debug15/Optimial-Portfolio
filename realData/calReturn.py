import csv
import numpy as np

def getStockTestData(filePath, n_test_start, n_testing_days):
    with open(filePath, 'r') as file:
        csvReader = csv.reader(file)
        next(csvReader)
        temp = []
        for i in range(n_test_start):
            next(csvReader)
        for i in range(n_testing_days):
            row = next(csvReader)
            temp.append(float(row[9]))
        return temp

# read resultLib.csv
with open('resultLib.csv', 'r') as file:
    csvReader = csv.reader(file)
    optimal_b = []
    for row in csvReader:
        optimal_b.append(float(row[1]))

filePaths = ["ADANIPORTS.csv","ASIANPAINT.csv", "AXISBANK.csv","HDFC.csv","ITC.csv","TCS.csv","HINDUNILVR.csv","INFY.csv","LT.csv","ICICIBANK.csv","RELIANCE.csv","KOTAKBANK.csv","HEROMOTOCO.csv","WIPRO.csv","HCLTECH.csv"]
tempTestReturns = []
for i in filePaths:
    tempTestReturns.append(getStockTestData(i, 500, 500))

testReturns = np.array(tempTestReturns)
testReturns /= testReturns[:, 0][:, np.newaxis]

# calculate the returns for the test period and print the final returns
portfolio_value = np.dot(optimal_b, testReturns)

# print("Portfolio value:", portfolio_value)

# average portfolio value
average_portfolio_value = np.mean(portfolio_value)
print("Average portfolio value:", average_portfolio_value)

# standard deviation of portfolio value
std_dev_portfolio_value = np.std(portfolio_value)
print("Standard deviation of portfolio value:", std_dev_portfolio_value)

# min and max portfolio value
min_portfolio_value = np.min(portfolio_value)
print("Minimum portfolio value:", min_portfolio_value)

max_portfolio_value = np.max(portfolio_value)
print("Maximum portfolio value:", max_portfolio_value)