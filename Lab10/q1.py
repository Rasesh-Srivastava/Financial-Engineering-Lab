import numpy as npy
import math
import matplotlib.pyplot as GraphPlotter
def GeometricBrownianMotion(S_0, mu, sigma, n):
  dt = 1.0/252
  W_t = npy.random.normal(0, 1, n)
  prices = []
  for i in range(n):
    S_t = S_0 * math.exp( (mu - sigma**2)*dt + sigma*math.sqrt(dt)*W_t[i])
    prices.append(S_t)
    S_0 = S_t
  return prices

def pathOfGBM(S_0, mu, sigma, heading):
  n = 252
  x = npy.arange(n)
  for i in range(10):
    prices = GeometricBrownianMotion(S_0, mu, sigma, n)
    GraphPlotter.plot(x, prices)
  GraphPlotter.ylabel('Stock prices, S(t)')
  GraphPlotter.title(heading)
  GraphPlotter.xlabel('time, t (in days)')
  GraphPlotter.show()

def PriceOfAsianOption(S_0, r, sigma, K, MaximumNumberOfIterations = 1000, path_length = 126, n = 126):
  dt = 1.0/252
  PayoffOfCallOption, PayoffOfPutlOption = [], []
  for i in range(MaximumNumberOfIterations):
    S = GeometricBrownianMotion(S_0, r, sigma, path_length)
    CallV = max(npy.mean(S) - K, 0)
    CallP = max(K - npy.mean(S), 0)
    PayoffOfCallOption.append(math.exp(-r*n*dt) * CallV)
    PayoffOfPutlOption.append(math.exp(-r*n*dt) * CallP)
  return npy.mean(PayoffOfCallOption), npy.mean(PayoffOfPutlOption), npy.var(PayoffOfCallOption), npy.var(PayoffOfPutlOption)

def Sensitivityr(S0, sigma, K, Plo=True):
  MyCall, MyPut = [], []
  r = npy.linspace(0, 0.5, num=120, endpoint=False)
  for i in r:
    MyCallPrice, MyPutPrice, _, _ = PriceOfAsianOption(S0, i, sigma, K, 500, 150, 100)
    MyCall.append(MyCallPrice)
    MyPut.append(MyPutPrice)
  if Plo != False:
    GraphPlotter.plot(r, MyCall, color='red')
    GraphPlotter.ylabel("Price of Asian Call Option")
    GraphPlotter.title("Dependence of Price of Asian Call Option on r")
    GraphPlotter.xlabel("Risk-free rate (r)")
    GraphPlotter.show()
    GraphPlotter.plot(r, MyPut, color='red')
    GraphPlotter.ylabel("Price of Asian Put Option")
    GraphPlotter.title("Dependence of Price of Asian Put Option on r")
    GraphPlotter.xlabel("Risk-free rate (r)")
    GraphPlotter.show()
  return MyCall, MyPut

def SensitivityK(S0, r, sigma, Plo=True):
  MyCall, MyPut = [], []
  K = npy.linspace(50, 150, num=250)
  for i in K:
    MyCallPrice, MyPutPrice, _, _ = PriceOfAsianOption(S0, r, sigma, i, 500, 150, 100)
    MyCall.append(MyCallPrice)
    MyPut.append(MyPutPrice)
  if Plo != False:
    GraphPlotter.plot(K, MyCall, color='red')
    GraphPlotter.ylabel("Price of Asian Call Option")
    GraphPlotter.title("Dependence of Price of Asian Call Option on K")
    GraphPlotter.xlabel("Strike price (K)")
    GraphPlotter.show()
    GraphPlotter.plot(K, MyPut, color='red')
    GraphPlotter.ylabel("Price of Asian Put Option")
    GraphPlotter.title("Dependence of Price of Asian Put Option on K")
    GraphPlotter.xlabel("Strike price (K)")
    GraphPlotter.show()
  return MyCall, MyPut

def Sensitivitysigma(S0, r, K, Plo=True):
  MyCall, MyPut = [], []
  sigma = npy.linspace(0, 1, num=120, endpoint=False)
  for i in sigma:
    MyCallPrice, MyPutPrice, _, _ = PriceOfAsianOption(S0, r, i, K, 500, 150, 100)
    MyCall.append(MyCallPrice)
    MyPut.append(MyPutPrice)
  if Plo != False:
    GraphPlotter.plot(sigma, MyCall, color='red')
    GraphPlotter.ylabel("Price of Asian Call Option")
    GraphPlotter.title("Dependence of Price of Asian Call Option on sigma")
    GraphPlotter.xlabel("Volatility (sigma)")
    GraphPlotter.show()
    GraphPlotter.plot(sigma, MyPut, color='red')
    GraphPlotter.ylabel("Price of Asian Put Option")
    GraphPlotter.title("Dependence of Price of Asian Put Option on sigma")
    GraphPlotter.xlabel("Volatility (sigma)")
    GraphPlotter.show()
  return MyCall, MyPut

def SensitivityS0(r, sigma, K, Plo=True):
  MyCall, MyPut = [], []
  S0 = npy.linspace(50, 150, num=250)
  for i in S0:
    MyCallPrice, MyPutPrice, _, _ = PriceOfAsianOption(i, r, sigma, K, 500, 150, 100)
    MyCall.append(MyCallPrice)
    MyPut.append(MyPutPrice)
  if Plo != False:
    GraphPlotter.plot(S0, MyCall, color='red')
    GraphPlotter.ylabel("Price of Asian Call Option")
    GraphPlotter.title("Dependence of Price of Asian Call Option on S0")
    GraphPlotter.xlabel("Asset Price at t = 0 (S0)")
    GraphPlotter.show()
    GraphPlotter.plot(S0, MyPut, color='red')
    GraphPlotter.ylabel("Price of Asian Put Option")
    GraphPlotter.title("Dependence of Price of Asian Put Option on S0")
    GraphPlotter.xlabel("Asset Price at t = 0 (S0)")
    GraphPlotter.show()
  return MyCall, MyPut

pathOfGBM(100, 0.1, 0.2, "Asset price in real world")
pathOfGBM(100, 0.05, 0.2, "Asset price in risk-neutral world")
for K in [90, 105, 110]:
  MyCallPrice, MyPutPrice, VarianceOfCallOption, VarianceOfPutlOption = PriceOfAsianOption(100, 0.05, 0.2, K)
  print()
  print()
  print(f"For K = {K},")
  print("Price of Asian Call Option =", MyCallPrice)
  print("Variance in Price of Asian Call Option =", VarianceOfCallOption)
  print()
  print("Price of Asian Put Option =", MyPutPrice)
  print("Variance in Price of Asian Put Option =", VarianceOfPutlOption)
SensitivityS0(0.05, 0.2, 105)
SensitivityK(100, 0.05, 0.2)
Sensitivityr(100, 0.2, 105)
Sensitivitysigma(100, 0.05, 105)