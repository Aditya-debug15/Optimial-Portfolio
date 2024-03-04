import os
import numpy as np
import csv

def getStockData(filePath):
    with open(filePath, 'r') as file:
        csvReader = csv.reader(file)
        next(csvReader)
        temp = []
        # print(header)
        for row in csvReader:
            temp.append(float(row[9]))
        return temp

def getStockDates(filePath):
    with open(filePath, 'r') as file:
        csvReader = csv.reader(file)
        next(csvReader)
        temp = []
        for row in csvReader:
            temp.append(row[0])
        return temp

tempReturns = []
filePaths = ["ADANIPORTS.csv","ASIANPAINT.csv", "AXISBANK.csv","HDFC.csv","ITC.csv","TCS.csv","HINDUNILVR.csv","INFY.csv","LT.csv","ICICIBANK.csv","RELIANCE.csv","KOTAKBANK.csv","HEROMOTOCO.csv","WIPRO.csv","HCLTECH.csv"]

for i in filePaths:
    tempReturns.append(getStockData(i))

dates = getStockDates(filePaths[0])

# now write the data to a file each row must contain date and the stock prices for that date
with open('data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["Date"] + filePaths)
    for i in range(len(dates)):
        row = [dates[i]]
        for j in range(len(filePaths)):
            row.append(tempReturns[j][i])
        writer.writerow(row)
