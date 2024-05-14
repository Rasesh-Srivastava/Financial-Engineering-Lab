import numpy as npy
import math
import matplotlib.pyplot as GraphPlotter
sigma = 0.4
step_size = [1, 5]
S = 100
T = 5
r = 0.05
K = 105

def CheckTheArbitrageConditions(u, d, r, t):
  if d < math.exp(r*t) and math.exp(r*t) < u:
    return False
  else:
    return True

for step in step_size:
    PricesOfTheCallOption = []
    PricesOfThePutOption = []
    for M in range(1, 401, step):
        t = T/M
        d = math.exp(-sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)
        NetInterestRate = math.exp(r*t) # R
        u = math.exp(sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)
        p = (NetInterestRate - d)/(u - d)
        IsArbitrage = CheckTheArbitrageConditions(u, d, r, t)
        if IsArbitrage:
            print(f"Arbitrage Opportunity exists for M = {M}")
            PricesOfThePutOption.append(-1)
            PricesOfTheCallOption.append(-1)
            continue
        else:
            print(f"No arbitrage exists for M = {M}")

        C = [[0 for i in range(M + 1)] for j in range(M + 1)]
        P = [[0 for i in range(M + 1)] for j in range(M + 1)]

        for i in range(0, M + 1):
            C[M][i] = max(0, S*math.pow(u, M - i)*math.pow(d, i) - K)
            P[M][i] = max(0, K - S*math.pow(u, M - i)*math.pow(d, i))

        for j in range(M - 1, -1, -1):
            for i in range(0, j + 1):
                C[j][i] = (p*C[j + 1][i] + (1 - p)*C[j + 1][i + 1]) / NetInterestRate
                P[j][i] = (p*P[j + 1][i] + (1 - p)*P[j + 1][i + 1]) / NetInterestRate

        PricesOfTheCallOption.append(C[0][0])
        PricesOfThePutOption.append(P[0][0])
    x = npy.arange(1, 401, step)
    GraphPlotter.plot(x, PricesOfTheCallOption,color='red')
    GraphPlotter.xlabel("Number of sub-intervals, i.e., M")
    GraphPlotter.title(f"M vs Initial Call Option Price    (for the step size = {step})")
    GraphPlotter.ylabel("Call option prices at t = 0") 
    GraphPlotter.show()
    GraphPlotter.plot(x, PricesOfThePutOption,color='red')
    GraphPlotter.xlabel("Number of sub-intervals, i.e., M")
    GraphPlotter.title(f"M vs Initial Put Option Price    (for the step size = {step})")
    GraphPlotter.ylabel("Put option prices at t = 0") 
    GraphPlotter.show()