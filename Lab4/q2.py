# Name: Rasesh Srivastava
# Roll Number: 210123072
# MA374 FE Lab, Assignment 4, Question 2
import numpy as npy
from numpy import random
import matplotlib.pyplot as GraphPlotter
import math

def MinimumVariancePortfolio(Meu, SIGMA):
  u = [1 for i in range(len(Meu))]
  weight_min_var = u @ npy.linalg.inv(SIGMA) / (u @ npy.linalg.inv(SIGMA) @ npy.transpose(u))
  return_of_minimum_variance_portfolio = weight_min_var @ npy.transpose(Meu)
  risk_of_minimum_variance_portfolio = math.sqrt(weight_min_var @ SIGMA @ npy.transpose(weight_min_var))
  return risk_of_minimum_variance_portfolio, return_of_minimum_variance_portfolio

def EquationOfCML(x, y):
  intercept = []
  slope = []
  for i in range(len(x) - 1):
    x1, x2 = x[i], x[i + 1]
    y1, y2 = y[i], y[i + 1]
    slope.append((y2 - y1)/(x2 - x1))
    intercept.append(y1 - slope[-1]*x1)
  return sum(slope)/len(slope), sum(intercept)/len(intercept)

def calculateOne():
  for mu in returns:
    w = WeightsCalcFunction(M_1, C_1, mu)
    if w[0] < 0 or w[1] < 0:
      continue
    weights_1.append(w)
    sigma = math.sqrt(w @ C_1 @ npy.transpose(w))
    riskOne.append(sigma)
    actualReturnsOne.append(mu)

def WeightsCalcFunction(Meu, SIGMA, mu):
  n = len(Meu)
  InverseOfSigma = npy.linalg.inv(SIGMA)
  u = [1 for i in range(n)]
  p = [[1, u @ InverseOfSigma @ npy.transpose(Meu)], [mu, Meu @ InverseOfSigma @ npy.transpose(Meu)]]
  q = [[u @ InverseOfSigma @ npy.transpose(u), 1], [Meu @ InverseOfSigma @ npy.transpose(u), mu]]
  r = [[u @ InverseOfSigma @ npy.transpose(u), u @ InverseOfSigma @ npy.transpose(Meu)], [Meu @ InverseOfSigma @ npy.transpose(u), Meu @ InverseOfSigma @ npy.transpose(Meu)]]
  det_p, det_q, det_r = npy.linalg.det(p), npy.linalg.det(q), npy.linalg.det(r)
  det_p /= det_r
  det_q /= det_r
  w = det_p * (u @ InverseOfSigma) + det_q * (Meu @ InverseOfSigma)
  return w

weights = []
actual_returns = []
returns = npy.linspace(0, 0.5, num = 10000)
risk = []
SIGMA = [[0.005, -0.010, 0.004], [-0.010, 0.040, -0.002], [0.004, -0.002, 0.023]]
Meu = [0.1, 0.2, 0.15]
risk_feasible_region, returns_feasible_region = [], []
returns_plot1 = []
risk_plot1 = []
risk_of_minimum_variance_portfolio, return_of_minimum_variance_portfolio = MinimumVariancePortfolio(Meu, SIGMA)
returns_plot2 = []
risk_plot2 = []

for mu in returns:
  w = WeightsCalcFunction(Meu, SIGMA, mu)
  if w[0] < 0 or w[1] < 0 or w[2] < 0:
    continue
  weights.append(w)
  sigma = math.sqrt(w @ SIGMA @ npy.transpose(w))
  risk.append(sigma)
  actual_returns.append(mu)

for i in range(500):
  w1, w2, w3 = random.randint(100), random.randint(100), random.randint(100)
  SumOfWeights = w1 + w2 + w3
  while SumOfWeights == 0:
    w1, w2, w3 = random.randint(100), random.randint(100), random.randint(100)
    SumOfWeights = w1 + w2 + w3
  w1 /= SumOfWeights
  w2 /= SumOfWeights
  w3 /= SumOfWeights
  w = npy.array([w1, w2, w3])
  returns_feasible_region.append(Meu @ npy.transpose(w))
  risk_feasible_region.append(math.sqrt(w @ SIGMA @ npy.transpose(w)))
  
for i in range(len(actual_returns)):
  if actual_returns[i] >= return_of_minimum_variance_portfolio: 
    returns_plot1.append(actual_returns[i])
    risk_plot1.append(risk[i])
  else:
    returns_plot2.append(actual_returns[i])
    risk_plot2.append(risk[i])

GraphPlotter.plot(risk_plot1, returns_plot1, color = 'red', linewidth = 5, label = 'Efficient Frontier')
GraphPlotter.plot(risk_plot2, returns_plot2, color = 'blue', linewidth = 5)
GraphPlotter.scatter(risk_feasible_region, returns_feasible_region, color = 'cyan', linewidth = 0.1, label = 'Feasible region')
GraphPlotter.scatter(risk_of_minimum_variance_portfolio, return_of_minimum_variance_portfolio, color = 'green', linewidth = 5, label = 'Minimum Variance Point')
GraphPlotter.xlabel("Risk, i.e, sigma")
GraphPlotter.title("Minimum Variance Curve")
GraphPlotter.ylabel("Returns") 
GraphPlotter.grid(True)
GraphPlotter.legend()
GraphPlotter.show()
riskOne = []
actualReturnsOne = []
weights_1 = []
C_1 = [[0.005, -0.010], [-0.010, 0.040]]
M_1 = [0.1, 0.2]
riskTwo = []
actualReturnsTwo = []
weights_2 = []
C_2 = [[0.040, -0.002], [-0.002, 0.023]]
M_2 = [0.2, 0.15]
riskThree = []
actualReturnsThree = []
weights_3 = []
C_3 = [[0.005, 0.004], [0.004, 0.023]]
M_3 = [0.1, 0.15]

calculateOne()
for mu in returns:
  w = WeightsCalcFunction(M_3, C_3, mu)
  if w[0] < 0 or w[1] < 0:
    continue
  weights_3.append(w)
  sigma = math.sqrt(w @ C_3 @ npy.transpose(w))
  riskThree.append(sigma)
  actualReturnsThree.append(mu)

for mu in returns:
  w = WeightsCalcFunction(M_2, C_2, mu)
  if w[0] < 0 or w[1] < 0:
    continue
  weights_2.append(w)
  sigma = math.sqrt(w @ C_2 @ npy.transpose(w))
  riskTwo.append(sigma)
  actualReturnsTwo.append(mu)

GraphPlotter.plot(risk, actual_returns, color='red', label='3 stocks')
GraphPlotter.plot(riskOne, actualReturnsOne, color='blue', label='Stock 1 and 2')
GraphPlotter.plot(riskTwo, actualReturnsTwo, color='yellow', label='Stock 2 and 3')
GraphPlotter.plot(riskThree, actualReturnsThree, color='green', label='Stock 1 and 3')
GraphPlotter.xlabel("Sigma (risk)")
GraphPlotter.title("Minimum Variance Curve with No short sales")
GraphPlotter.ylabel("Returns")
GraphPlotter.legend()
GraphPlotter.grid(True)
GraphPlotter.show()

GraphPlotter.plot(risk, actual_returns, color='yellow', linewidth=5, label='3 stocks')
GraphPlotter.plot(riskOne, actualReturnsOne, color='blue', linewidth=5, label='Stock 1 and 2')
GraphPlotter.plot(riskTwo, actualReturnsTwo, color='green', linewidth=5, label='Stock 2 and 3')
GraphPlotter.plot(riskThree, actualReturnsThree, color='brown', linewidth=5, label='Stock 1 and 3')
GraphPlotter.scatter(risk_feasible_region, returns_feasible_region, color='m', marker='.', label='Feasible region')
GraphPlotter.xlabel("Sigma (risk)")
GraphPlotter.title("Minimum Variance Curve (with feasible region) with No short sales")
GraphPlotter.ylabel("Returns")
GraphPlotter.legend()
GraphPlotter.grid(True)
GraphPlotter.show()
risk.clear()
weights.clear()
for mu in returns:
  w = WeightsCalcFunction(Meu, SIGMA, mu)  
  weights.append(w)
  sigma = math.sqrt(w @ SIGMA @ npy.transpose(w))
  risk.append(sigma)
  
w_01, w_02, w_03 = npy.array([i[0] for i in weights]), npy.array([i[1] for i in weights]), npy.array([i[2] for i in weights])
x = npy.linspace(-5, 5, 1000)
y = [0 for i in range(len(x))]

print("Equation of line w1 versus w2 is:")
m, c = EquationOfCML(w_01, w_02)
print(f"w2 = {m:.2f} w1 + {c:.2f}")
GraphPlotter.axis([-0.5, 1.5, -0.5, 1.5])
GraphPlotter.plot(w_01, w_02, color = 'red', label = 'w1 versus w2')
GraphPlotter.plot(w_01, 1 - w_01, color = 'black', label = 'w1 + w2 = 1')
GraphPlotter.plot(x, y, color = 'blue', label = 'w2 = 0')
GraphPlotter.plot(y, x, color = 'green', label = 'w1 = 0')
GraphPlotter.xlabel("weights_1 (w1)")
GraphPlotter.title("Weights of minimum variance curve (w1 vs w2)")
GraphPlotter.ylabel("weights_2 (w2)") 
GraphPlotter.legend()
GraphPlotter.grid(True)
GraphPlotter.show()

print("Equation of line w2 versus w3 is:")
m, c = EquationOfCML(w_02, w_03)
print(f"w3 = {m:.2f} w2 + {c:.2f}")
GraphPlotter.axis([-0.5, 1.5, -0.5, 1.5])
GraphPlotter.plot(w_02, w_03, color = 'red', label = 'w2 versus w3')
GraphPlotter.plot(w_02, 1 - w_02, color = 'black', label = 'w2 + w3 = 1')
GraphPlotter.plot(x, y, color = 'blue', label = 'w3 = 0')
GraphPlotter.plot(y, x, color = 'green', label = 'w2 = 0')
GraphPlotter.xlabel("weights_2 (w2)")
GraphPlotter.title("Weights of minimum variance curve (w2 vs w3)")
GraphPlotter.ylabel("weights_3 (w3)") 
GraphPlotter.legend()
GraphPlotter.grid(True)
GraphPlotter.show()

print("Equation of line w1 versus w3 is:")
m, c = EquationOfCML(w_01, w_03)
print(f"w3 = {m:.2f} w1 + {c:.2f}")
GraphPlotter.axis([-0.5, 1.5, -0.5, 1.5])
GraphPlotter.plot(w_01, w_03, color = 'red', label = 'w1 versus w3')
GraphPlotter.plot(w_03, 1 - w_03, color = 'black', label = 'w1 + w3 = 1')
GraphPlotter.plot(x, y, color = 'blue', label = 'w3 = 0')
GraphPlotter.plot(y, x, color = 'green', label = 'w1 = 0')
GraphPlotter.xlabel("weights_1 (w1)")
GraphPlotter.title("Weights of minimum variance curve (w1 vs w3)")
GraphPlotter.ylabel("weights_3 (w3)") 
GraphPlotter.legend()
GraphPlotter.grid(True)
GraphPlotter.show()