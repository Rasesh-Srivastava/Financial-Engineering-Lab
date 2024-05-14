# Name: Rasesh Srivastava
# Roll Number: 210123072
# MA374 FE Lab, Assignment 3, Question 4
import functools
import time
import math
import operator as TheOperator
import matplotlib.pyplot as GraphPlotter
def CalculatingThePriceOfTheOption(i, S0, u, d, M):
  path = format(i, 'b').zfill(M)
  for idx in path:
    if idx == '1':
      S0 *= d
    else:
      S0 *= u
  return S0

def CheckTheArbitrageConditions(u, d, r, t):
  if d < math.exp(r*t) and math.exp(r*t) < u:
    return False
  else:
    return True

def EfficientBinomialMethod(S0, K, T, M, r, sigma, WhatIsToBePrinted):
  CurrentTime = time.time()
  t = T/M
  d = math.exp(-sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)
  R = math.exp(r*t)
  u = math.exp(sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)
  p = (R - d)/(u - d)
  IsArbitrage = CheckTheArbitrageConditions(u, d, r, t)
  if IsArbitrage:
    if WhatIsToBePrinted == 1:
      print("Arbitrage Opportunity exists for M = {}".format(M))
    return
  else:
    if WhatIsToBePrinted == 1:
      print("No arbitrage exists for M = {}".format(M))

  C = [[0 for i in range(M + 1)] for j in range(M + 1)]

  for i in range(0, M + 1):
    C[M][i] = max(0, S0*math.pow(u, M - i)*math.pow(d, i) - K)

  for j in range(M - 1, -1, -1):
    for i in range(0, j + 1):
      C[j][i] = (p*C[j + 1][i] + (1 - p)*C[j + 1][i + 1]) / R;
    
  if WhatIsToBePrinted == 1: 
    print(f"Price European Call Option \t\t= {C[0][0]}")
    print(f"Execution Time \t\t\t= {time.time() - CurrentTime} seconds\n")

  if WhatIsToBePrinted == 2:
    for i in range(M + 1):
      print(f"At t = {i}")
      for j in range(i + 1):
        print(f"Index Number = {j}\tOption Price = {C[i][j]}")
      print()
      
  return C[0][0]


def BinomialCoefficient(n, r):
  r = min(r, n-r)
  numer = functools.reduce(TheOperator.mul, range(n, n-r, -1), 1)
  denom = functools.reduce(TheOperator.mul, range(1, r+1), 1)
  return numer // denom   

def MaxEfficientBinomialMethod(S0, K, T, M, r, sigma, WhatIsToBePrinted):
  CurrentTime = time.time()
  u, d = 0, 0
  t = T/M
  d = math.exp(-sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)  
  R = math.exp(r*t)
  u = math.exp(sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)
  p = (R - d)/(u - d)
  IsArbitrage = CheckTheArbitrageConditions(u, d, r, t)

  if IsArbitrage:
    if WhatIsToBePrinted == 1:
      print(f"Arbitrage Opportunity exists for M = {M}")
    return 0, 0
  else:
    if WhatIsToBePrinted == 1:
      print(f"No arbitrage exists for M = {M}")

  PriceOfTheRequiredOption = 0
  for j in range(0, M + 1):
    PriceOfTheRequiredOption += BinomialCoefficient(M, j) * math.pow(p, j) * math.pow(1 - p, M - j) * max(S0 * math.pow(u, j) * math.pow(d, M - j) - K, 0)
  
  PriceOfTheRequiredOption /= math.pow(R, M)
  if WhatIsToBePrinted == 1: 
    print(f"Price of European Call Option \t\t= {PriceOfTheRequiredOption}")
    print(f"Execution Time \t\t\t= {time.time() - CurrentTime} seconds\n")

  return PriceOfTheRequiredOption

def BinomialMethodWithoutAnyOptimisations(S0, K, T, M, r, sigma, WhatIsToBePrinted):
  CurrentTime = time.time()
  u, d = 0, 0
  t = T/M
  u = math.exp(sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)
  d = math.exp(-sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)  
  R = math.exp(r*t)
  p = (R - d)/(u - d);
  IsArbitrage = CheckTheArbitrageConditions(u, d, r, t)
  if IsArbitrage:
    if WhatIsToBePrinted == 1:
      print(f"Arbitrage Opportunity exists for M = {M}")
    return 0, 0
  else:
    if WhatIsToBePrinted == 1:
      print(f"No arbitrage exists for M = {M}")

  PriceOfTheRequiredOption = []
  for i in range(0, M + 1):
    D = []
    for j in range(int(pow(2, i))):
      D.append(0)
    PriceOfTheRequiredOption.append(D)
    
  for i in range(int(pow(2, M))):
    NeededPrice = CalculatingThePriceOfTheOption(i, S0, u, d, M)
    PriceOfTheRequiredOption[M][i] = max(NeededPrice - K, 0)
  
  for j in range(M - 1, -1, -1):
    for i in range(0, int(pow(2, j))):
      PriceOfTheRequiredOption[j][i] = (p*PriceOfTheRequiredOption[j + 1][2*i] + (1 - p)*PriceOfTheRequiredOption[j + 1][2*i + 1]) / R;

  if WhatIsToBePrinted == 1: 
    print(f"Price of European Call Option \t\t= {PriceOfTheRequiredOption[0][0]}")
    print(f"Execution Time \t\t\t= {time.time() - CurrentTime} seconds\n")
    
  return PriceOfTheRequiredOption[0][0]

def FunctionToPlotGraphs(x, y, Xaxis, Yaxis, title):
  GraphPlotter.plot(x, y,color = 'red')
  GraphPlotter.ylabel(Yaxis) 
  GraphPlotter.title(title)
  GraphPlotter.xlabel(Xaxis)
  GraphPlotter.show()

print("Question 4 Part (a)")
SecondSetOfvaluesOfM = [5, 10, 25, 50]
FirstPricesOfOption, SecondPricesOfOption, ThirdPricesOfOption = [], [], []
FirstSetOfvaluesOfM = [5, 10, 25]

print('Unoptimised Binomial Algorithm to price an European Call Option is running')
for m in FirstSetOfvaluesOfM:
  FirstPricesOfOption.append(BinomialMethodWithoutAnyOptimisations(S0 = 100, T = 1, K = 100, M = m, r = 0.08, sigma = 0.30, WhatIsToBePrinted = 1))

print()
print()
print('Efficient Binomial Algorithm to price an European Call Option is running (Markov Based)')
for m in SecondSetOfvaluesOfM:
  SecondPricesOfOption.append(EfficientBinomialMethod(S0 = 100, T = 1, K = 100, M = m, r = 0.08, sigma = 0.30, WhatIsToBePrinted = 1))

print()
print()
print('Most Efficient Binomial Algorithm to price an European Call Option is running (Markov Based)')
for m in SecondSetOfvaluesOfM:
  ThirdPricesOfOption.append(MaxEfficientBinomialMethod(S0 = 100, T = 1, K = 100, M = m, r = 0.08, sigma = 0.30, WhatIsToBePrinted = 1))

print()
print()
print("Question 4 Part (b)")
FunctionToPlotGraphs(SecondSetOfvaluesOfM, SecondPricesOfOption, "M", "Prices of the Option at time t = 0", "Prices of the Option at time t = 0 vs M")
M = [i for i in range(1, 21)]
FirstPricesOfOption.clear()
for m in M:
  FirstPricesOfOption.append(MaxEfficientBinomialMethod(S0 = 100, T = 1, K = 100, M = m, r = 0.08, sigma = 0.30, WhatIsToBePrinted = 0))
FunctionToPlotGraphs(M, FirstPricesOfOption, "M", "Prices of the Option at time t = 0", "Prices of the Option at time t = 0 vs M (Variation with more data-points for M)")

print()
print()
print("Question 4 Part (c)")
EfficientBinomialMethod(S0 = 100, T = 1, K = 100, M = 5, r = 0.08, sigma = 0.30, WhatIsToBePrinted = 2)