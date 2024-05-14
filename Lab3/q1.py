# Name: Rasesh Srivastava
# Roll Number: 210123072
# MA374 FE Lab, Assignment 3, Question 1
import matplotlib.pyplot as GraphPlotter
import math
import numpy as np
def CheckTheArbitrageConditions(u, d, r, t):
  if d < math.exp(r*t) and math.exp(r*t) < u:
    return False
  else:
    return True
  
r = 0.08
K = 100
T = 1
sigma = 0.3
M = 100
S0 = 100

def AmericanOptionPricing(S0, K, T, M, r, sigma, IsDisplay):
    t = T/M
    d = np.exp(-sigma*np.sqrt(t) + (r - 0.5*sigma*sigma)*t)
    R = math.exp(r*t)
    u= np.exp(sigma*np.sqrt(t) + (r - 0.5*sigma*sigma)*t)
    p = (R - d)/(u - d)
    check = CheckTheArbitrageConditions(u, d, r, t)
    if check:
        print(f"Arbitrage Opportunity exists for M = {M}")
        return 0,0
    else:
        if IsDisplay:
            print(f"No arbitrage exists for M = {M}")
    
    PricesOfCallOption = np.zeros((M+1, M+1))
    PricesOfPutOption = np.zeros((M+1, M+1)) 
    for i in range(0, M + 1):
        PricesOfCallOption[M][i] = max(0, S0 * math.pow(u, M - i) * math.pow(d, i) - K)
        PricesOfPutOption[M][i] = max(0, K - S0 * math.pow(u, M - i) * math.pow(d, i))

    for j in range(M - 1, -1, -1):
        for i in range(0, j + 1):
            PricesOfCallOption[j][i] = max((p * PricesOfCallOption[j + 1][i] + (1 - p) * PricesOfCallOption[j + 1][i + 1]) * np.exp(-r*t), S0*math.pow(u, j-i)*math.pow(d,i) - K)
            PricesOfPutOption[j][i] = max((p * PricesOfPutOption[j + 1][i] + (1 - p) * PricesOfPutOption[j + 1][i + 1]) * np.exp(-r*t), K - S0*math.pow(u, j-i)*math.pow(d,i))

    if IsDisplay:
        print(f"The initial price of the American Call Option = {PricesOfCallOption[0][0]}")
        print(f"The initial price of the American Put Option = {PricesOfPutOption[0][0]}")
        print()
        print()
    return PricesOfCallOption[0][0], PricesOfPutOption[0][0]

def FunctionToPlotGraphs(x, y, Xaxis, Yaxis, title):
    GraphPlotter.plot(x, y,color = 'red')
    GraphPlotter.ylabel(Yaxis) 
    GraphPlotter.title(title)
    GraphPlotter.xlabel(Xaxis)
    GraphPlotter.show()

def PlotWithVariationIn_S0():
    S0 = np.linspace(0,210)
    ArrayOfPutPrices = []
    ArrayOfCallPrices = []
    for s0 in S0:
        PricesOfCallOption,PricesOfPutOption = AmericanOptionPricing(s0,K,T,M,r,sigma,0)
        ArrayOfCallPrices.append(PricesOfCallOption)
        ArrayOfPutPrices.append(PricesOfPutOption)
        
    FunctionToPlotGraphs(S0,ArrayOfCallPrices,"S(0)", "Intial Prices of Call Option","Call option prices at t = 0 with varying S(0)")
    FunctionToPlotGraphs(S0,ArrayOfPutPrices,"S(0)", "Intial Prices of Put Option","Put option prices at t = 0 with varying S(0)")

def PlotWithVariationIn_sigma():
    Sigma = np.linspace(0.01,1)
    ArrayOfPutPrices = []
    ArrayOfCallPrices = []
    for sigma in Sigma:
        PricesOfCallOption,PricesOfPutOption = AmericanOptionPricing(S0,K,T,M,r,sigma,0)
        ArrayOfCallPrices.append(PricesOfCallOption)
        ArrayOfPutPrices.append(PricesOfPutOption)
        
    FunctionToPlotGraphs(Sigma,ArrayOfCallPrices,"Sigma", "Intial Prices of Call Option","Call option prices at t = 0 with varying sigma")
    FunctionToPlotGraphs(Sigma,ArrayOfPutPrices,"Sigma", "Intial Prices of Put Option","Put option prices at t = 0 with varying sigma")


def PlotWithVariationIn_r():
    R = np.linspace(0,1)
    ArrayOfPutPrices = []
    ArrayOfCallPrices = []
    for r in R:
        PricesOfCallOption,PricesOfPutOption = AmericanOptionPricing(S0,K,T,M,r,sigma,0)
        ArrayOfCallPrices.append(PricesOfCallOption)
        ArrayOfPutPrices.append(PricesOfPutOption)
        
    FunctionToPlotGraphs(R,ArrayOfCallPrices,"r", "Intial Prices of Call Option","Call option prices at t = 0 with varying r")
    FunctionToPlotGraphs(R,ArrayOfPutPrices,"r", "Intial Prices of Put Option","Put option prices at t = 0 with varying r")

def PlotWithVariationIn_K():
    K = np.linspace(0,210)
    ArrayOfPutPrices = []
    ArrayOfCallPrices = []
    for k in K:
        PricesOfCallOption,PricesOfPutOption = AmericanOptionPricing(S0,k,T,M,r,sigma,0)
        ArrayOfCallPrices.append(PricesOfCallOption)
        ArrayOfPutPrices.append(PricesOfPutOption)
        
    FunctionToPlotGraphs(K,ArrayOfCallPrices,"K", "Intial Prices of Call Option","Call option prices at t = 0 with varying K")
    FunctionToPlotGraphs(K,ArrayOfPutPrices,"K", "Intial Prices of Put Option","Put option prices at t = 0 with varying K")

def PlotWithVariationIn_M():
    M_values = [i for i in range(1,200)]
    K = [95,100,105]
    for k in K:
        ArrayOfPutPrices = []
        ArrayOfCallPrices = []
        for M in M_values:
            PricesOfCallOption,PricesOfPutOption = AmericanOptionPricing(S0,k,T,M,r,sigma,0)
            ArrayOfCallPrices.append(PricesOfCallOption)
            ArrayOfPutPrices.append(PricesOfPutOption)
            
        FunctionToPlotGraphs(M_values,ArrayOfCallPrices,"M", "Intial Prices of Call Option",f"Call option prices at t = 0 with varying M with K = {k}")
        FunctionToPlotGraphs(M_values,ArrayOfPutPrices,"M", "Intial Prices of Put Option",f"Put option prices at t = 0 with varying M with K = {k}")

AmericanOptionPricing(S0,K,T,M,r,sigma,1)
PlotWithVariationIn_S0()
PlotWithVariationIn_K()
PlotWithVariationIn_r()
PlotWithVariationIn_sigma()
PlotWithVariationIn_M()