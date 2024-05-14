# Name: Rasesh Srivastava
# Roll Number: 210123072
# MA374 FE Lab, Assignment 4, Question 3
import numpy as npy
import math
import matplotlib.pyplot as GraphPlotter
import pandas as pd

def WeightCalcFunction(Meu, SIGMA, mu):
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

df = pd.read_csv('./StockPriceData.csv')
df.set_index('Date', inplace=True)
df = df.pct_change()
Meu = npy.mean(df, axis = 0) * 12
SIGMA = df.cov()
returns = npy.linspace(-3, 5, num = 5000)
u = npy.array([1 for i in range(len(Meu))])
risk = []

def partb():
  print()
  print()
  print("Question 3 Part (b)")
  print()
  formatted_weights = ["{:.12f}".format(weight) for weight in market_portfolio_weights]
  print("Market Portfolio Weights =", formatted_weights)
  print("Return = ", market_Return_value)
  print("Risk = ", market_risk_value * 100, " %")

for mu in returns:
  w = WeightCalcFunction(Meu, SIGMA, mu)
  sigma = math.sqrt(w @ SIGMA @ npy.transpose(w))
  risk.append(sigma)

weight_min_var = u @ npy.linalg.inv(SIGMA) / (u @ npy.linalg.inv(SIGMA) @ npy.transpose(u))
return_of_minimum_variance_portfolio = weight_min_var @ npy.transpose(Meu)
risk_of_minimum_variance_portfolio = math.sqrt(weight_min_var @ SIGMA @ npy.transpose(weight_min_var))

returns_plot1, risk_plot1, returns_plot2, risk_plot2 = [], [], [], []
for i in range(len(returns)):
  if returns[i] >= return_of_minimum_variance_portfolio: 
    returns_plot1.append(returns[i])
    risk_plot1.append(risk[i])
  else:
    returns_plot2.append(returns[i])
    risk_plot2.append(risk[i])

print()
print()
print("Question 3 Part (a)")
print()
mu_rf = 0.05
market_portfolio_weights = (Meu - mu_rf * u) @ npy.linalg.inv(SIGMA) / ((Meu - mu_rf * u) @ npy.linalg.inv(SIGMA) @ npy.transpose(u) )
market_Return_value = market_portfolio_weights @ npy.transpose(Meu)
market_risk_value = math.sqrt(market_portfolio_weights @ SIGMA @ npy.transpose(market_portfolio_weights))

GraphPlotter.plot(risk_plot1, returns_plot1, color = 'red', label = 'Efficient Frontier')
GraphPlotter.plot(risk_plot2, returns_plot2, color = 'green')
GraphPlotter.xlabel("Risk ,i.e., sigma")
GraphPlotter.title("Minimum Variance Curve and Efficient Frontier")
GraphPlotter.ylabel("Returns") 
GraphPlotter.plot(market_risk_value, market_Return_value, color = 'blue', marker = 'o')
GraphPlotter.annotate('Market Portfolio (' + str(round(market_risk_value, 2)) + ', ' + str(round(market_Return_value, 2)) + ')', 
            xy=(market_risk_value, market_Return_value), xytext=(0.2, 0.6))
GraphPlotter.plot(risk_of_minimum_variance_portfolio, return_of_minimum_variance_portfolio, color = 'green', marker = 'o')
GraphPlotter.annotate('Minimum Variance Portfolio (' + str(round(risk_of_minimum_variance_portfolio, 2)) + ', ' + str(round(return_of_minimum_variance_portfolio, 2)) + ')', 
            xy=(risk_of_minimum_variance_portfolio, return_of_minimum_variance_portfolio), xytext=(risk_of_minimum_variance_portfolio, -0.6))
GraphPlotter.legend()
GraphPlotter.grid(True)
GraphPlotter.show()

partb()
print()
print()
print("Question 3 Part (c)")
print()
returns_cml = []
risk_cml = npy.linspace(0, 2, num = 5000)
for i in risk_cml:
  returns_cml.append(mu_rf + (market_Return_value - mu_rf) * i / market_risk_value)

slope, intercept = (market_Return_value - mu_rf) / market_risk_value, mu_rf
print()
print("Equation of CML is:")
print(f"y = {slope:.2f} x + {intercept:.2f}\n")

GraphPlotter.plot(risk, returns, color='brown', label='Minimum Variance Curve')
GraphPlotter.plot(risk_cml, returns_cml, color='cyan', label='Capital Market Line',alpha=0.7)
GraphPlotter.xlabel("Risk, i.e., sigma")
GraphPlotter.ylabel("Returns")
GraphPlotter.title("Capital Market Line with Markowitz Efficient Frontier")
GraphPlotter.grid(True)
GraphPlotter.legend()
GraphPlotter.show()

GraphPlotter.plot(risk_cml, returns_cml, color='red')
GraphPlotter.xlabel("Risk, i.e., sigma")
GraphPlotter.ylabel("Returns")
GraphPlotter.title("Capital Market Line")
GraphPlotter.grid(True)
GraphPlotter.show()
print()
print()
print("Question 3 Part (d)")
print()
StockPricesDataArray = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'NVDA','PYPL', 'IBM', 'CSCO', 'JPM']

beta_k = npy.linspace(-1, 1, 5000)
mu_k = mu_rf + (market_Return_value - mu_rf) * beta_k
GraphPlotter.plot(beta_k, mu_k)
print("Equation of Security Market Line is:")
print(f"mu = {market_Return_value - mu_rf:.2f} beta + {mu_rf:.2f}")
GraphPlotter.title('Security Market Line for all the 10 stocks')
GraphPlotter.xlabel("Beta")
GraphPlotter.ylabel("Mean Return")
GraphPlotter.grid(True)
GraphPlotter.show()