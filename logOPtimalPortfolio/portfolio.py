from scipy.optimize import minimize
import math
import numpy as np

# transforming input to combinations
def generate_equations(lines):
    data = [list(map(float, line.split())) for line in lines]
    probabilities = [data[i][0::2] for i in range(n)]
    values = [data[i][1::2] for i in range(n)]

    combinations = np.array(np.meshgrid(*values)).T.reshape(-1, n)
    probabilities_matrix = np.array(np.meshgrid(*probabilities)).T.reshape(-1, n)
    probabilities_vector = np.prod(probabilities_matrix, axis=1)
    return combinations, probabilities_vector

# forming objective
def objective(x):
    sum = 0
    for i in range(len(combination)):
        temp = 0
        for j in range(len(combination[i])):
            temp += combination[i][j]*x[j]
        sum += math.log(temp)*prob_vector[i]
    return -sum

# Define the constraints
def constraint(x):
    return sum(x)-1

n = int(input())
input_lines = []
for i in range(n):
    input_lines.append(input())

combination, prob_vector = generate_equations(input_lines)

# Define the bounds
b = (0,1)
bounds = [b for _ in range(n)]

# Define the initial guess
x0 = [1/n for _ in range(n)]

# Perform the optimization
con = {'type':'eq', 'fun':constraint}
solution = minimize(objective,x0,method='SLSQP',bounds=bounds,constraints=con)
x = solution.x
print(x)
