# Name: Rasesh Srivastava
# Roll Number: 210123072
# MA374 FE Lab, Assignment 3, Question 3
import time
import math
import matplotlib.pyplot as GraphPlotter
def CheckTheArbitrageConditions(u, d, r, t):
  if d < math.exp(r*t) and math.exp(r*t) < u:
    return False
  else:
    return True

def TemporaryStorage(idx, u, d, p, R, M, PriceOfTheStock, CurrentMaximum, PricesOfTheReqOptions):
  if idx == M + 1 or (PriceOfTheStock, CurrentMaximum) in PricesOfTheReqOptions[idx]:
    return

  TemporaryStorage(idx + 1, u, d, p, R, M, PriceOfTheStock*u, max(PriceOfTheStock*u, CurrentMaximum), PricesOfTheReqOptions)
  TemporaryStorage(idx + 1, u, d, p, R, M, PriceOfTheStock*d, max(PriceOfTheStock*d, CurrentMaximum), PricesOfTheReqOptions)

  if idx == M:
    PricesOfTheReqOptions[M][(PriceOfTheStock, CurrentMaximum)] = max(CurrentMaximum - PriceOfTheStock, 0)
  else:
    PricesOfTheReqOptions[idx][(PriceOfTheStock, CurrentMaximum)] = (p*PricesOfTheReqOptions[idx + 1][ (u * PriceOfTheStock, max(u * PriceOfTheStock, CurrentMaximum)) ] + (1 - p)*PricesOfTheReqOptions[idx + 1][ (d * PriceOfTheStock, CurrentMaximum) ]) / R



def LookBackEuropeanOptionEfficient(S0, T, M, r, sigma, WhatIsToBePrinted):
  if WhatIsToBePrinted == 1: 
    print()
    print()
    print(f"Program is running for M = {M}")
    print()
  curr_time_1 = time.time()
  u, d = 0, 0
  t = T/M
  d = math.exp(-sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)  
  PricesOfTheReqOptions = []
  R = math.exp(r*t)
  u = math.exp(sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)
  p = (R - d)/(u - d)
  for i in range(0, M + 1):
    PricesOfTheReqOptions.append(dict())

  TemporaryStorage(0, u, d, p, R, M, S0, S0, PricesOfTheReqOptions)
  IsArbitrage = CheckTheArbitrageConditions(u, d, r, t)
  if IsArbitrage:
    if WhatIsToBePrinted == 1:
      print(f"Arbitrage Opportunity exists for M = {M}")
    return 0, 0
  else:
    if WhatIsToBePrinted == 1:
      print(f"No arbitrage exists for M = {M}")

  if WhatIsToBePrinted == 1: 
    print(f"Initial Price of Loopback Option \t= {PricesOfTheReqOptions[0][ (S0, S0) ]}")
    print(f"Execution Time \t\t\t\t= {time.time() - curr_time_1} seconds\n")
  
  if WhatIsToBePrinted == 2:
    for i in range(len(PricesOfTheReqOptions)):
      print(f"At time t = {i}")
      for key, value in PricesOfTheReqOptions[i].items():
        print(f"Intermediate state = {key}\t\tOption Price = {value}")
      print()

  return PricesOfTheReqOptions[0][ (S0, S0) ]

print("Question 3 Part (a)")
PriceOfTheOption = []
M = [5, 10, 25, 50]
for m in M:
  PriceOfTheOption.append(LookBackEuropeanOptionEfficient(S0 = 100, T = 1, M = m, r = 0.08, sigma = 0.30, WhatIsToBePrinted = 1))

print()
print()
print("Question 3 Part (b)")
GraphPlotter.plot(M, PriceOfTheOption,color="red")
GraphPlotter.ylabel("Prices of the Option at time t = 0")
GraphPlotter.title("Prices of the Option at time t = 0 vs M")
GraphPlotter.xlabel("M")
GraphPlotter.show()
M = [i for i in range(1, 21)]
PriceOfTheOption.clear()
for m in M:
  PriceOfTheOption.append(LookBackEuropeanOptionEfficient(S0 = 100, T = 1, M = m, r = 0.08, sigma = 0.30, WhatIsToBePrinted = 0))

GraphPlotter.plot(M, PriceOfTheOption,color="red")
GraphPlotter.ylabel("Prices of the Option at time t = 0")
GraphPlotter.title("Prices of the Option at time t = 0 vs M (Variation with more data points for M)")
GraphPlotter.xlabel("M")
GraphPlotter.show()
print()
print()
print("Question 3 Part (c)")
LookBackEuropeanOptionEfficient(S0 = 100, T = 1, M = 5, r = 0.08, sigma = 0.30, WhatIsToBePrinted = 2)