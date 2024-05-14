# Name: Rasesh Srivastava
# Roll Number: 210123072
# MA374 FE Lab, Assignment 2, Question 1

# Whole Program takes a lot of time to run due to the plotting of many 2d and 3d graphs. To run specific parts of the program, comment the other function calls present at the end of the code file.
import matplotlib.pyplot as GraphPlotter
import numpy as npy
import math

def BinomialModelForOptionPricing(S0, K, T, M, r, sigma, set, PrintTheOptionPrices):
  u, d = 0, 0
  t = T/M
  if set == 1:
    u = math.exp(sigma*math.sqrt(t))
    d = math.exp(-sigma*math.sqrt(t)) 
  else:
    u = math.exp(sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)
    d = math.exp(-sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)

  R = math.exp(r*t)
  p = (R - d)/(u - d)
  # Checking the No-Arbitrage Conditions
  isArbitrage = False
  if d < math.exp(r*t) and math.exp(r*t) < u:
    isArbitrage = False
  else:
    isArbitrage = True

  if isArbitrage:
    if PrintTheOptionPrices == 1:
      print(f"Arbitrage Opportunity exists for M = {M}")
    return 0, 0
  else:
    if PrintTheOptionPrices == 1:
      print(f"No arbitrage exists for M = {M}")

  C = [[0 for i in range(M + 1)] for j in range(M + 1)]
  P = [[0 for i in range(M + 1)] for j in range(M + 1)]

  for i in range(0, M + 1):
    C[M][i] = max(0, S0*math.pow(u, M - i)*math.pow(d, i) - K)
    P[M][i] = max(0, K - S0*math.pow(u, M - i)*math.pow(d, i))

  for j in range(M - 1, -1, -1):
    for i in range(0, j + 1):
      C[j][i] = (p*C[j + 1][i] + (1 - p)*C[j + 1][i + 1]) / R
      P[j][i] = (p*P[j + 1][i] + (1 - p)*P[j + 1][i + 1]) / R
  
  if PrintTheOptionPrices == 1: 
    print(f"For Set {set},")
    print(f"Initial Price of European Call Option = {C[0][0]}")
    print(f"Initial Price of European Put Option = {P[0][0]}\n")

  return C[0][0], P[0][0]

def ThreeD_GraphPlotter(x, y, z, HoriAxis, VertAxis, z_axis, title):
  ax = GraphPlotter.axes(projection='3d')
  ax.scatter3D(x, y, z, color = 'red')
  ax.set_xlabel(HoriAxis)
  ax.set_zlabel(z_axis)
  GraphPlotter.title(title)
  ax.set_ylabel(VertAxis)
  GraphPlotter.show()

def TwoD_GraphPlotter(x, y, HoriAxis, VertAxis, title):
  GraphPlotter.plot(x, y, color = 'red')
  GraphPlotter.ylabel(VertAxis)
  GraphPlotter.title(title)
  GraphPlotter.xlabel(HoriAxis)
  GraphPlotter.show()

def VaryingS0_2d():
  S =  npy.linspace(20, 200, 100)
  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    for s in S:
      c, p = BinomialModelForOptionPricing(S0 = s, K = 100, T = 1, M = 100, r = 0.08, sigma = 0.30, set = set1or2, PrintTheOptionPrices = 0)
      PricesOfCallOption.append(c)
      PricesOfPutOption.append(p)

    TwoD_GraphPlotter(S, PricesOfCallOption, "S(0)", "Initial Call Option Prices", "Variation of Initial Call Option Prices with S(0) for set " + str(set1or2))
    TwoD_GraphPlotter(S, PricesOfPutOption, "S(0)", "Initial Put Option Prices", "Variation of Initial Put Option Prices with S(0) for set " + str(set1or2))

def VaryingK_2d():
  K =  npy.linspace(20, 200, 100)
  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    for k in K:
      c, p = BinomialModelForOptionPricing(S0 = 100, K = k, T = 1, M = 100, r = 0.08, sigma = 0.30, set = set1or2, PrintTheOptionPrices = 0)
      PricesOfCallOption.append(c)
      PricesOfPutOption.append(p)

    TwoD_GraphPlotter(K, PricesOfCallOption, "K", "Initial Call Option Prices", "Variation of Initial Call Option Prices with K for set " + str(set1or2))
    TwoD_GraphPlotter(K, PricesOfPutOption, "K", "Initial Put Option Prices", "Variation of Initial Put Option Prices with K for set " + str(set1or2))

def Varyingr_2d():
  ValuesOfrToBeTaken =  npy.linspace(0, 1, 100)

  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    for rate in ValuesOfrToBeTaken:
      c, p = BinomialModelForOptionPricing(S0 = 100, K = 100, T = 1, M = 100, r = rate, sigma = 0.30, set = set1or2, PrintTheOptionPrices = 0)
      PricesOfCallOption.append(c)
      PricesOfPutOption.append(p)

    TwoD_GraphPlotter(ValuesOfrToBeTaken, PricesOfCallOption, "r", "Initial Call Option Prices", "Variation of Initial Call Option Prices with rate(r) for set " + str(set1or2))
    TwoD_GraphPlotter(ValuesOfrToBeTaken, PricesOfPutOption, "r", "Initial Put Option Prices", "Variation of Initial Put Option Prices with rate(r) for set " + str(set1or2))

def VaryingSigma_2d():
  ValuesOfSigmaToBeTaken =  npy.linspace(0.01, 1, 100)

  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    for sg in ValuesOfSigmaToBeTaken:
      c, p = BinomialModelForOptionPricing(S0 = 100, K = 100, T = 1, M = 100, r = 0.08, sigma = sg, set = set1or2, PrintTheOptionPrices = 0)
      PricesOfCallOption.append(c)
      PricesOfPutOption.append(p)

    TwoD_GraphPlotter(ValuesOfSigmaToBeTaken, PricesOfCallOption, "sigma", "Initial Call Option Prices", "Variation of Initial Call Option Prices with sigma for set " + str(set1or2))
    TwoD_GraphPlotter(ValuesOfSigmaToBeTaken, PricesOfPutOption, "sigma", "Initial Put Option Prices", "Variation of Initial Put Option Prices with sigma for set " + str(set1or2))

def VaryingM_2d():
  ValuesOfMToBeTaken =  [i for i in range(50, 200)]
  ValuesOfKToBeTaken = [95, 100, 105]

  for k in ValuesOfKToBeTaken:
    for set1or2 in [1,2]:
      PricesOfCallOption = []
      PricesOfPutOption = []
      for m in ValuesOfMToBeTaken:
        c, p = BinomialModelForOptionPricing(S0 = 100, K = k, T = 1, M = m, r = 0.08, sigma = 0.30, set = set1or2, PrintTheOptionPrices = 0)
        PricesOfCallOption.append(c)
        PricesOfPutOption.append(p)

      TwoD_GraphPlotter(ValuesOfMToBeTaken, PricesOfCallOption, "M", "Initial Call Option Prices", "Variation of Initial Call Option Prices with M for set " + str(set1or2) + " and K " + str(k))
      TwoD_GraphPlotter(ValuesOfMToBeTaken, PricesOfPutOption, "M", "Initial Put Option Prices", "Variation of Initial Put Option Prices with M for set " + str(set1or2) + " and K " + str(k))

def VaryingS0_K_3d():
  S =  npy.linspace(20, 200, 50)
  K =  npy.linspace(20, 200, 50)
  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    VertAxis = []
    HoriAxis = []
    for s in S:
      for k in K:
        c, p = BinomialModelForOptionPricing(S0 = s, K = k, T = 1, M = 100, r = 0.08, sigma = 0.30, set = set1or2, PrintTheOptionPrices = 0)
        HoriAxis.append(s)
        VertAxis.append(k)
        PricesOfCallOption.append(c)
        PricesOfPutOption.append(p)

    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfCallOption, "S(0)", "K", "Initial Call Option Prices", "Variation of Initial Call Option Prices with S(0) and K for set " + str(set1or2))
    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfPutOption, "S(0)", "K", "Initial Put Option Prices", "Variation of Initial Put Option Prices with S(0) and K for set " + str(set1or2))


def VaryingS0_r_3d():
  S =  npy.linspace(20, 200, 50)
  ValuesOfrToBeTaken =  npy.linspace(0, 1, 50)
  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    VertAxis = []
    HoriAxis = []
    for s in S:
      for rate in ValuesOfrToBeTaken:
        c, p = BinomialModelForOptionPricing(S0 = s, K = 100, T = 1, M = 100, r = rate, sigma = 0.30, set = set1or2, PrintTheOptionPrices = 0)
        HoriAxis.append(s)
        VertAxis.append(rate)
        PricesOfCallOption.append(c)
        PricesOfPutOption.append(p)

    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfCallOption, "S(0)", "r", "Initial Call Option Prices", "Variation of Initial Call Option Prices with S(0) and rate(r) for set " + str(set1or2))
    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfPutOption, "S(0)", "r", "Initial Put Option Prices", "Variation of Initial Put Option Prices with S(0) and rate(r) for set " + str(set1or2))


def VaryingS0_Sigma_3d():
  S =  npy.linspace(20, 200, 50)
  ValuesOfSigmaToBeTaken =  npy.linspace(0.01, 1, 50)
  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    VertAxis = []
    HoriAxis = []
    for s in S:
      for sg in ValuesOfSigmaToBeTaken:
        c, p = BinomialModelForOptionPricing(S0 = s, K = 100, T = 1, M = 100, r = 0.08, sigma = sg, set = set1or2, PrintTheOptionPrices = 0)
        HoriAxis.append(s)
        VertAxis.append(sg)
        PricesOfCallOption.append(c)
        PricesOfPutOption.append(p)

    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfCallOption, "S(0)", "sigma", "Initial Call Option Prices", "Variation of Initial Call Option Prices with S(0) and sigma for set " + str(set1or2))
    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfPutOption, "S(0)", "sigma", "Initial Put Option Prices", "Variation of Initial Put Option Prices with S(0) and sigma for set " + str(set1or2))


def VaryingS0_M_3d():
  S =  npy.linspace(20, 200, 50)
  ValuesOfMToBeTaken =  [i for i in range(50, 200)]
  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    VertAxis = []
    HoriAxis = []
    for s in S:
      for m in ValuesOfMToBeTaken:
        c, p = BinomialModelForOptionPricing(S0 = s, K = 100, T = 1, M = m, r = 0.08, sigma = 0.30, set = set1or2, PrintTheOptionPrices = 0)
        HoriAxis.append(s)
        VertAxis.append(m)
        PricesOfCallOption.append(c)
        PricesOfPutOption.append(p)

    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfCallOption, "S(0)", "M", "Initial Call Option Prices", "Variation of Initial Call Option Prices with S(0) and M for set " + str(set1or2))
    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfPutOption, "S(0)", "M", "Initial Put Option Prices", "Variation of Initial Put Option Prices with S(0) and M for set " + str(set1or2))


def VaryingK_r_3d():
  K =  npy.linspace(20, 200, 50)
  ValuesOfrToBeTaken =  npy.linspace(0, 1, 50)
  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    VertAxis = []
    HoriAxis = []
    for k in K:
      for rate in ValuesOfrToBeTaken:
        c, p = BinomialModelForOptionPricing(S0 = 100, K = k, T = 1, M = 100, r = rate, sigma = 0.30, set = set1or2, PrintTheOptionPrices = 0)
        HoriAxis.append(k)
        VertAxis.append(rate)
        PricesOfCallOption.append(c)
        PricesOfPutOption.append(p)

    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfCallOption, "K", "r", "Initial Call Option Prices", "Variation of Initial Call Option Prices with K and rate(r) for set " + str(set1or2))
    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfPutOption, "K", "r", "Initial Put Option Prices", "Variation of Initial Put Option Prices with K and rate(r) for set " + str(set1or2))


def VaryingK_Sigma_3d():
  K =  npy.linspace(20, 200, 50)
  ValuesOfSigmaToBeTaken =  npy.linspace(0.01, 1, 50)
  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    VertAxis = []
    HoriAxis = []
    for k in K:
      for sg in ValuesOfSigmaToBeTaken:
        c, p = BinomialModelForOptionPricing(S0 = 100, K = k, T = 1, M = 100, r = 0.08, sigma = sg, set = set1or2, PrintTheOptionPrices = 0)
        HoriAxis.append(k)
        VertAxis.append(sg)
        PricesOfCallOption.append(c)
        PricesOfPutOption.append(p)

    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfCallOption, "K", "sigma", "Initial Call Option Prices", "Variation of Initial Call Option Prices with K and sigma for set " + str(set1or2))
    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfPutOption, "K", "sigma", "Initial Put Option Prices", "Variation of Initial Put Option Prices with K and sigma for set " + str(set1or2))


def VaryingK_M_3d():
  K =  npy.linspace(20, 200, 50)
  ValuesOfMToBeTaken =  [i for i in range(50, 200, 2)]

  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    VertAxis = []
    HoriAxis = []
    for k in K:
      for m in ValuesOfMToBeTaken:
        c, p = BinomialModelForOptionPricing(S0 = 100, K = k, T = 1, M = m, r = 0.08, sigma = 0.30, set = set1or2, PrintTheOptionPrices = 0)
        HoriAxis.append(k)
        VertAxis.append(m)
        PricesOfCallOption.append(c)
        PricesOfPutOption.append(p)

    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfCallOption, "K", "M", "Initial Call Option Prices", "Variation of Initial Call Option Prices with K and M for set " + str(set1or2))
    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfPutOption, "K", "M", "Initial Put Option Prices", "Variation of Initial Put Option Prices with K and M for set " + str(set1or2))


def Varyingr_Sigma_3d():
  ValuesOfrToBeTaken =  npy.linspace(0, 1, 50)
  ValuesOfSigmaToBeTaken =  npy.linspace(0.15, 1, 50)
  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    VertAxis = []
    HoriAxis = []
    for rate in ValuesOfrToBeTaken:
      for sg in ValuesOfSigmaToBeTaken:
        c, p = BinomialModelForOptionPricing(S0 = 100, K = 100, T = 1, M = 100, r = rate, sigma = sg, set = set1or2, PrintTheOptionPrices = 0)
        HoriAxis.append(rate)
        VertAxis.append(sg)
        PricesOfCallOption.append(c)
        PricesOfPutOption.append(p)

    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfCallOption, "r", "sigma", "Initial Call Option Prices", "Variation of Initial Call Option Prices with rate(r) and sigma for set " + str(set1or2))
    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfPutOption, "r", "sigma", "Initial Put Option Prices", "Variation of Initial Put Option Prices with rate(r) and sigma for set " + str(set1or2))


def Varyingr_M_3d():
  ValuesOfrToBeTaken =  npy.linspace(0, 1, 50)
  ValuesOfMToBeTaken =  [i for i in range(50, 200, 2)]
  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    VertAxis = []
    HoriAxis = []
    for rate in ValuesOfrToBeTaken:
      for m in ValuesOfMToBeTaken:
        c, p = BinomialModelForOptionPricing(S0 = 100, K = 100, T = 1, M = m, r = rate, sigma = 0.30, set = set1or2, PrintTheOptionPrices = 0)
        HoriAxis.append(rate)
        VertAxis.append(m)
        PricesOfCallOption.append(c)
        PricesOfPutOption.append(p)

    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfCallOption, "r", "M", "Initial Call Option Prices", "Variation of Initial Call Option Prices with rate(r) and M for set " + str(set1or2))
    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfPutOption, "r", "M", "Initial Put Option Prices", "Variation of Initial Put Option Prices with rate(r) and M for set " + str(set1or2))


def VaryingSigma_M_3d():
  ValuesOfSigmaToBeTaken =  npy.linspace(0.1, 1, 50)
  ValuesOfMToBeTaken =  [i for i in range(50, 200, 2)]
  for set1or2 in [1,2]:
    PricesOfCallOption = []
    PricesOfPutOption = []
    VertAxis = []
    HoriAxis = []
    for sg in ValuesOfSigmaToBeTaken:
      for m in ValuesOfMToBeTaken:
        c, p = BinomialModelForOptionPricing(S0 = 100, K = 100, T = 1, M = m, r = 0.08, sigma = sg, set = set1or2, PrintTheOptionPrices = 0)
        HoriAxis.append(sg)
        VertAxis.append(m)
        PricesOfCallOption.append(c)
        PricesOfPutOption.append(p)

    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfCallOption, "sigma", "M", "Initial Call Option Prices", "Variation of Initial Call Option Prices with sigma and M for set " + str(set1or2))
    ThreeD_GraphPlotter(HoriAxis, VertAxis, PricesOfPutOption, "sigma", "M", "Initial Put Option Prices", "Variation of Initial Put Option Prices with sigma and M for set " + str(set1or2))

BinomialModelForOptionPricing(S0 = 100, K = 100, T = 1, M = 100, r = 0.08, sigma = 0.30, set = 1, PrintTheOptionPrices = 1)
BinomialModelForOptionPricing(S0 = 100, K = 100, T = 1, M = 100, r = 0.08, sigma = 0.30, set = 2, PrintTheOptionPrices = 1)
VaryingS0_2d()
VaryingK_2d()
Varyingr_2d()
VaryingSigma_2d()
VaryingM_2d()
VaryingS0_K_3d()
VaryingS0_r_3d()
VaryingS0_Sigma_3d()
VaryingS0_M_3d()
VaryingK_r_3d()
VaryingK_Sigma_3d()
VaryingK_M_3d()
Varyingr_Sigma_3d()
Varyingr_M_3d()
VaryingSigma_M_3d()