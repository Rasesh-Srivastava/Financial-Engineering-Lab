# Name: Rasesh Srivastava
# Roll Number: 210123072
# MA374 FE Lab, Assignment 4, Question 1
import numpy as npy
import matplotlib.pyplot as GraphPlotter
import math

def MinimumVariancePortfolio(Meu, SIGMA):
  u = [1 for i in range(len(Meu))]
  weight_min_var = u @ npy.linalg.inv(SIGMA) / (u @ npy.linalg.inv(SIGMA) @ npy.transpose(u))
  return_of_minimum_variance_portfolio = weight_min_var @ npy.transpose(Meu)
  risk_of_minimum_variance_portfolio = math.sqrt(weight_min_var @ SIGMA @ npy.transpose(weight_min_var))
  return risk_of_minimum_variance_portfolio, return_of_minimum_variance_portfolio

def WeightsCalcFunction(Meu, SIGMA, mu):
  InverseOfSigma = npy.linalg.inv(SIGMA)
  u = [1 for i in range(len(Meu))]
  p = [[1, u @ InverseOfSigma @ npy.transpose(Meu)], [mu, Meu @ InverseOfSigma @ npy.transpose(Meu)]]
  q = [[u @ InverseOfSigma @ npy.transpose(u), 1], [Meu @ InverseOfSigma @ npy.transpose(u), mu]]
  r = [[u @ InverseOfSigma @ npy.transpose(u), u @ InverseOfSigma @ npy.transpose(Meu)], [Meu @ InverseOfSigma @ npy.transpose(u), Meu @ InverseOfSigma @ npy.transpose(Meu)]]
  det_p, det_q, det_r = npy.linalg.det(p), npy.linalg.det(q), npy.linalg.det(r)
  det_p /= det_r
  det_q /= det_r
  w = det_p * (u @ InverseOfSigma) + det_q * (Meu @ InverseOfSigma)
  return w

def callb():
  print()
  print()
  print("Question 1 Part (b)")
  print()
  print("Index\t\t\tWeights\t\t\t\tReturn\t\t\t\tRisk")
  print()

def lastPart():
  print()
  print()
  print("Question 1 Part (f)")
  print()
  sigma = 0.1
  mu_current = (market_Return_value - mu_rf) * sigma / market_risk_value + mu_rf
  weight_rf = (mu_current - market_Return_value) / (mu_rf - market_Return_value)
  weights_risk = (1 - weight_rf) * market_portfolio_weights
  print(f"Risk = {sigma * 100} %")
  print(f"Risk-Free Weights = {weight_rf}")
  print(f"Risky Weights = {weights_risk}")
  print(f"Returns = {mu_current}")
  sigma = 0.25
  mu_current = (market_Return_value - mu_rf) * sigma / market_risk_value + mu_rf
  weight_rf = (mu_current - market_Return_value) / (mu_rf - market_Return_value)
  weights_risk = (1 - weight_rf) * market_portfolio_weights
  print()
  print()
  print(f"Risk = {sigma * 100} %")
  print(f"Risk-Free Weights = {weight_rf}")
  print(f"Risky Weights = {weights_risk}")
  print(f"Returns = {mu_current}")

print("Question 1 Part (a)")
print()
Meu = [0.1, 0.2, 0.15]
SIGMA = [[0.005, -0.010, 0.004], [-0.010, 0.040, -0.002], [0.004, -0.002, 0.023]]
returns = npy.linspace(0, 0.5, num=10000)
risk = []
weights_10 = []
weights_15 = []
returns_plot1 = []
risk_plot1 = []
risk_of_minimum_variance_portfolio, return_of_minimum_variance_portfolio = MinimumVariancePortfolio(Meu, SIGMA)
returns_plot2 = []
risk_plot2 = []
return_10 = []
risk_10 = []
return_15 = []

Counter = 0
for mu in returns:
  w = WeightsCalcFunction(Meu, SIGMA, mu)
  sigma = math.sqrt(w @ SIGMA @ npy.transpose(w))
  risk.append(sigma)
  Counter += 1
  if Counter % 1000 == 0:
    weights_10.append(w)
    return_10.append(mu)
    risk_10.append(sigma * sigma)
  if abs(sigma - 0.15) < math.pow(10, -4.5):
    weights_15.append(w)
    return_15.append(mu)

for i in range(len(returns)):
  if returns[i] >= return_of_minimum_variance_portfolio: 
    returns_plot1.append(returns[i])
    risk_plot1.append(risk[i])
  else:
    returns_plot2.append(returns[i])
    risk_plot2.append(risk[i])

GraphPlotter.plot(risk_plot1, returns_plot1, color='red', label='Efficient Frontier')
GraphPlotter.plot(risk_plot2, returns_plot2, color='green')
GraphPlotter.xlabel("Risk, i.e, sigma")
GraphPlotter.title("Minimum variance line and the Markowitz Efficient Frontier")
GraphPlotter.ylabel("Returns") 
GraphPlotter.plot(risk_of_minimum_variance_portfolio, return_of_minimum_variance_portfolio, color='green', marker='o')
GraphPlotter.annotate(f'Minimum Variance Portfolio ({round(risk_of_minimum_variance_portfolio, 2)}, {round(return_of_minimum_variance_portfolio, 2)})', 
            xy=(risk_of_minimum_variance_portfolio, return_of_minimum_variance_portfolio), xytext=(risk_of_minimum_variance_portfolio + 0.05, return_of_minimum_variance_portfolio))
GraphPlotter.legend()
GraphPlotter.grid(True)
GraphPlotter.show()

callb()
for i in range(10):
  print(f"{i + 1}.\t{weights_10[i]}\t{return_10[i]}\t{risk_10[i]}")

print()
print()
print("Question 1 Part (c)")
print()
MinimumReturn, MaximumReturn = return_15[0], return_15[1]
MinimumReturnWeights, MaximumReturnWeights = weights_15[0], weights_15[1]
if MinimumReturn > MaximumReturn:
  MinimumReturn, MaximumReturn = MaximumReturn, MinimumReturn
  MinimumReturnWeights, MaximumReturnWeights = MaximumReturnWeights, MinimumReturnWeights

print(f"Minimum return = {MinimumReturn}")
print(f"Weights of the portfolio for Minimum return = {MinimumReturnWeights}")
print(f"\nMaximum return = {MaximumReturn}")
print(f"Weights of the portfolio for Maximum return = {MaximumReturnWeights}")

print()
print()
print("Question 1 Part (d)")
print()
given_return = 0.18
w = WeightsCalcFunction(Meu, SIGMA, given_return)
minimum_risk = math.sqrt(w @ SIGMA @ npy.transpose(w))
print(f"Minimum risk for 18% return = {minimum_risk * 100} %")
print(f"Weights of the portfolio = {w}")

print()
print()
print("Question 1 Part (e)")
print()
mu_rf = 0.1
u = npy.array([1, 1, 1])
market_portfolio_weights = (Meu - mu_rf * u) @ npy.linalg.inv(SIGMA) / ((Meu - mu_rf * u) @ npy.linalg.inv(SIGMA) @ npy.transpose(u) )
market_Return_value = market_portfolio_weights @ npy.transpose(Meu)
market_risk_value = math.sqrt(market_portfolio_weights @ SIGMA @ npy.transpose(market_portfolio_weights))

print(f"Weights of Market Portfolio = {market_portfolio_weights}")
print(f"Return = {market_Return_value}")
print(f"Risk = {market_risk_value * 100} %")
returns_cml = []
risk_cml = npy.linspace(0, 1, num=10000)
for i in risk_cml:
  returns_cml.append(mu_rf + (market_Return_value - mu_rf) * i / market_risk_value)

slope, intercept = (market_Return_value - mu_rf) / market_risk_value, mu_rf

print("\nEquation of Capital Market Line is:")
print(f"y = {slope:.2f} x + {intercept:.2f}\n")
GraphPlotter.scatter(market_risk_value, market_Return_value, color='red', linewidth=3, label='Market Portfolio')
GraphPlotter.plot(risk, returns, color='red', label='Minimum variance curve')
GraphPlotter.plot(risk_cml, returns_cml, color='green', label='Capital Market Line')
GraphPlotter.xlabel("Risk, i.e, sigma")
GraphPlotter.title("Capital Market Line with Minimum variance curve")
GraphPlotter.ylabel("Returns") 
GraphPlotter.grid(True)
GraphPlotter.legend()
GraphPlotter.show()
lastPart()