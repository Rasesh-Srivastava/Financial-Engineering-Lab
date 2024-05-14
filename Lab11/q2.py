import matplotlib.pyplot as GraphPlotter
import math
import numpy as npy
def CIRModel(beta, mu, sigma, r, t, T_list):
  Yield = []
  for T in T_list:  
    gamma = math.sqrt(beta*beta + 2*sigma*sigma)
    A = math.pow( ( 2*gamma*math.exp(0.5*(beta + gamma)*(T - t)) ) / (2*gamma + (gamma + beta)*(math.exp(gamma*(T - t)) - 1)), 2*beta*mu / (sigma*sigma) ) 
    B = 2 *(math.exp(gamma * (T - t)) - 1)  / ( 2*gamma + (gamma + beta) * (math.exp(gamma * (T - t)) - 1))
    P = A * math.exp(-B * r)
    y = -math.log(P) / (T - t)
    Yield.append(y)
  return Yield

GivenValues = [[0.02, 0.7, 0.02, 0.1], [0.7, 0.1, 0.3, 0.2], [0.06, 0.09, 0.5, 0.02]]
for indexValues in range(len(GivenValues)):
    beta, mu, sigma, r = GivenValues[indexValues]
    T = npy.linspace(0.1, 10, num=10, endpoint=False)
    Yield = CIRModel(beta, mu, sigma, r, 0, T)
    GraphPlotter.plot(T, Yield, marker='s',color='red')
    GraphPlotter.ylabel('Yield')
    GraphPlotter.title(f'Term structure for parameter set - {indexValues + 1}')
    GraphPlotter.xlabel('Maturity Time (T)')
    GraphPlotter.show()
  
T = npy.linspace(0.1, 600, num=600, endpoint=False)
rValues = [0.1 * i for i in range(1, 11)]
GivenValues = [[0.02, 0.7, 0.02]]
for indexValues in range(len(GivenValues)):
    beta, mu, sigma = GivenValues[indexValues]
    for r in rValues:
      Yield = CIRModel(beta, mu, sigma, r, 0, T)
      GraphPlotter.plot(T, Yield)
    
    GraphPlotter.ylabel('Yield')
    GraphPlotter.title('Term structure for 10 different values of r(0) & 600 time units for parameter set [0.02, 0.7, 0.02]')
    GraphPlotter.xlabel('Maturity Time (T)')
    GraphPlotter.show()