import matplotlib.pyplot as GraphPlotter
import math
import numpy as npy
def VasicekModel(beta, mu, sigma, r, t, T_list):
  Yield = []
  for T in T_list:  
    B = (1 - math.exp(-beta *  (T - t))) / beta
    A = math.exp((B - T + t)*(beta*beta*mu - sigma*sigma*0.5)/(beta*beta) - math.pow(sigma * B, 2)/(4*beta))
    P = A * math.exp(-B * r)
    y = -math.log(P) / (T - t)
    Yield.append(y)
  return Yield

GivenValues = [[5.9, 0.2, 0.3, 0.1], [3.9, 0.1, 0.3, 0.2], [0.1, 0.4, 0.11, 0.1]]
for indexValues in range(len(GivenValues)):
    beta, mu, sigma, r = GivenValues[indexValues]
    T = npy.linspace(0.01, 10, num=10, endpoint=False)
    Yield = VasicekModel(beta, mu, sigma, r, 0, T)
    GraphPlotter.plot(T, Yield, marker='s',color='red')
    GraphPlotter.ylabel('Yield')
    GraphPlotter.title(f'Term structure for parameter set - {indexValues + 1}')
    GraphPlotter.xlabel('Maturity Time (T)')
    GraphPlotter.show()
  
T = npy.linspace(0.01, 10, num=500, endpoint=False)
rValues = [0.1 * i for i in range(1, 11)]
for indexValues in range(len(GivenValues)):
    beta, mu, sigma, r = GivenValues[indexValues]
    for r in rValues:
      Yield = VasicekModel(beta, mu, sigma, r, 0, T)
      GraphPlotter.plot(T, Yield)

    GraphPlotter.ylabel('Yield')
    GraphPlotter.title(f'Term structure for 10 different values of r(0) and 500 time units for parameter set {indexValues+1}')
    GraphPlotter.xlabel('Maturity Time (T)')
    GraphPlotter.show()