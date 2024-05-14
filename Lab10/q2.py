import numpy as npy
import math
import matplotlib.pyplot as GraphPlotter
def VarianceReductionUsingControlVariates(PayoffOfOption, control_variate, r, n, dt):
  X_bar = npy.mean(control_variate)
  Y_bar = npy.mean(PayoffOfOption)
  MaximumNumberOfIterations = len(PayoffOfOption)
  num, denom = 0, 0
  for idx in range(MaximumNumberOfIterations):
    num += (control_variate[idx] - X_bar) * (PayoffOfOption[idx] - Y_bar)
    denom += (control_variate[idx] - X_bar) * (control_variate[idx] - X_bar)
  b = num/denom
  redAns = []
  for idx in range(MaximumNumberOfIterations):
    redAns.append((PayoffOfOption[idx] - b*(control_variate[idx] - X_bar) * math.exp(-r*n*dt)))
  return redAns

def GeometricBrownianMotion(S_0, mu, sigma, n):
  dt = 1.0/252
  W_t = npy.random.randn(n)
  prices = []
  for i in range(n):
    S_t = S_0 * math.exp( (mu - sigma**2)*dt + sigma*math.sqrt(dt)*W_t[i])
    prices.append(S_t)
    S_0 = S_t
  return prices

def PriceOfAsianOption(S_0, r, sigma, K, MaximumNumberOfIterations = 1000, path_length = 126, n = 126):
  CallOptionPriceUsingControlVariate, PutOptionPriceUsingControlVariate = [], []
  PayoffOfCallOption, PayoffOfPutOption = [], []
  dt = 1.0/252
  for i in range(MaximumNumberOfIterations):
    S = GeometricBrownianMotion(S_0, r, sigma, path_length)
    CallV = max(npy.mean(S) - K, 0)
    CallP = max(K - npy.mean(S), 0)
    PayoffOfCallOption.append(math.exp(-r*n*dt) * CallV)
    PayoffOfPutOption.append(math.exp(-r*n*dt) * CallP)
    CallOptionPriceUsingControlVariate.append(math.exp(-r*n*dt) * max(K - S[len(S) - 1], 0))
    PutOptionPriceUsingControlVariate.append(math.exp(-r*n*dt) * max(S[len(S) - 1] - K, 0))
  PayoffOfCallOption = VarianceReductionUsingControlVariates(PayoffOfCallOption, CallOptionPriceUsingControlVariate, r, n, dt)
  PayoffOfPutOption = VarianceReductionUsingControlVariates(PayoffOfPutOption, PutOptionPriceUsingControlVariate, r, n, dt)
  return npy.mean(PayoffOfCallOption), npy.mean(PayoffOfPutOption), npy.var(PayoffOfCallOption), npy.var(PayoffOfPutOption)

def Sensitivityr(S0, sigma, K, Plo=True):
  MyCall, MyPut = [], []
  r = npy.linspace(0, 0.5, num=120, endpoint=False)
  for i in r:
    call_price, MyPutPrice, _, _ = PriceOfAsianOption(S0, i, sigma, K, 500, 150, 100)
    MyCall.append(call_price)
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
  K = npy.linspace(70, 140, num=250)
  for i in K:
    call_price, MyPutPrice, _, _ = PriceOfAsianOption(S0, r, sigma, i, 500, 150, 100)
    MyCall.append(call_price)
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
    call_price, MyPutPrice, _, _ = PriceOfAsianOption(S0, r, i, K, 500, 150, 100)
    MyCall.append(call_price)
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
  S0 = npy.linspace(70, 140, num=250)
  for i in S0:
    call_price, MyPutPrice, _, _ = PriceOfAsianOption(i, r, sigma, K, 500, 150, 100)
    MyCall.append(call_price)
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

for K in [90, 105, 110]:
    call_price, MyPutPrice, VarianceOfCallOption, VarianceOfPutlOption = PriceOfAsianOption(100, 0.05, 0.2, K)
    print()
    print()
    print(f"For K = {K},")
    print("Price of Asian Call Option =", call_price)
    print("Variance in Price of Asian Call Option =", VarianceOfCallOption)
    print()
    print("Price of Asian Put Option =", MyPutPrice)
    print("Variance in Price of Asian Put Option =", VarianceOfPutlOption)
SensitivityS0(0.05, 0.2, 105)
SensitivityK(100, 0.05, 0.2)
Sensitivityr(100, 0.2, 105)
Sensitivitysigma(100, 0.05, 105)