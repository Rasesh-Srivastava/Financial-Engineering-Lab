# Name: Rasesh Srivastava
# Roll Number: 210123072
# MA374 FE Lab, Assignment 3, Question 2
import time
import math
import matplotlib.pyplot as GraphPlotter
def CalculatingThePriceOfTheOption(i, S0, u, d, M):
  path = format(i, 'b').zfill(M)
  payoff = S0
  for idx in path:
    if idx == '1':
      S0 *= d
    else:
      S0 *= u
    payoff = max(payoff, S0)
  
  return payoff - S0

def CheckTheArbitrageConditions(u, d, r, t):
  if d < math.exp(r*t) and math.exp(r*t) < u:
    return False
  else:
    return True

def LookBackEuropeanOption(S0, T, M, r, sigma, WhatIsToBePrinted):
  if WhatIsToBePrinted == 1: 
    print()
    print()
    print(f"Program is running for M = {M}")
    print()
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

  PriceOfTheRequiredOption = []
  for i in range(0, M + 1):
    D = []
    for j in range(int(pow(2, i))):
      D.append(0)
    PriceOfTheRequiredOption.append(D)
    
  for i in range(int(pow(2, M))):
    NeededPrice = CalculatingThePriceOfTheOption(i, S0, u, d, M)
    PriceOfTheRequiredOption[M][i] = max(NeededPrice, 0)
  
  for j in range(M - 1, -1, -1):
    for i in range(0, int(pow(2, j))):
      PriceOfTheRequiredOption[j][i] = (p*PriceOfTheRequiredOption[j + 1][2*i] + (1 - p)*PriceOfTheRequiredOption[j + 1][2*i + 1]) / R;

  if WhatIsToBePrinted == 1: 
    print(f"Initial Price of Loopback Option \t= {PriceOfTheRequiredOption[0][0]}")
    print(f"Execution Time \t\t\t\t= {time.time() - CurrentTime} seconds\n")

  if WhatIsToBePrinted == 2:
    for i in range(len(PriceOfTheRequiredOption)):
      print(f"At time t = {i}")
      for j in range(len(PriceOfTheRequiredOption[i])):
        print(f"Index Number = {j}\tOption Price = {PriceOfTheRequiredOption[i][j]}")
      print()
  return PriceOfTheRequiredOption[0][0]

print("Question 2 Part (a)")
PriceOfTheOption = []
M = [5, 10, 25]
for m in M:
  PriceOfTheOption.append(LookBackEuropeanOption(S0 = 100, T = 1, M = m, r = 0.08, sigma = 0.30, WhatIsToBePrinted = 1))

print()
print()
print("Question 2 Part (b)")
GraphPlotter.plot(M, PriceOfTheOption,color="red")
GraphPlotter.ylabel("Prices of the Option at time t = 0")
GraphPlotter.title("Prices of the Option at time t = 0 vs M")
GraphPlotter.xlabel("M")
GraphPlotter.show()
M = [i for i in range(1, 21)]
PriceOfTheOption.clear()
for m in M:
  PriceOfTheOption.append(LookBackEuropeanOption(S0 = 100, T = 1, M = m, r = 0.08, sigma = 0.30, WhatIsToBePrinted = 0))

GraphPlotter.plot(M, PriceOfTheOption,color="red")
GraphPlotter.ylabel("Prices of the Option at time t = 0")
GraphPlotter.title("Prices of the Option at time t = 0 vs M (Variation with more data points for M)")
GraphPlotter.xlabel("M")
GraphPlotter.show()
print()
print()
print("Question 2 Part (c)")
LookBackEuropeanOption(S0 = 100, T = 1, M = 5, r = 0.08, sigma = 0.30, WhatIsToBePrinted = 2)