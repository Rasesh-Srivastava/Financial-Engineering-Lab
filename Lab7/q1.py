from scipy.stats import norm
import math
def ClassicalBlackScholesMertonModel(s, t, T, K, r, sigma):
  if t == T:
    return max(0, s - K), max(0, K - s)
  d2 = (math.log(s/K) + (r - 0.5 * sigma * sigma) * (T - t) ) / ( sigma * math.sqrt(T - t))
  d1 = (math.log(s/K) + (r + 0.5 * sigma * sigma) * (T - t) ) / ( sigma * math.sqrt(T - t))
  PriceOfPutOption = K * math.exp( -r * (T - t) ) * norm.cdf(-d2) - s * norm.cdf(-d1)
  PriceOfCallOption = s * norm.cdf(d1) - K * math.exp( -r * (T - t) ) * norm.cdf(d2)
  return PriceOfCallOption, PriceOfPutOption

K = 1
t = 0
sigma = 0.6
T = 1
r = 0.05
s = 1.5
C, P = ClassicalBlackScholesMertonModel(s, t, T, K, r, sigma)
print(f"Using Model paramaters as: s = {s}, t = {t}, T = {T}, K = {K}, r = {r}, sigma = {sigma}\n")
print("Price of European Put Option =", P)
print("Price of European Call Option =", C)