from scipy.stats import norm
import math
import matplotlib.pyplot as GraphPlotter
import numpy as npy
def ClassicalBlackScholesMertonModel(s, t, T, K, r, sigma):
  if t == T:
    return max(0, s - K), max(0, K - s)
  d2 = (math.log(s/K) + (r - 0.5 * sigma * sigma) * (T - t) ) / ( sigma * math.sqrt(T - t))
  d1 = (math.log(s/K) + (r + 0.5 * sigma * sigma) * (T - t) ) / ( sigma * math.sqrt(T - t))
  PriceOfPutOption = K * math.exp( -r * (T - t) ) * norm.cdf(-d2) - s * norm.cdf(-d1)
  PriceOfCallOption = s * norm.cdf(d1) - K * math.exp( -r * (T - t) ) * norm.cdf(d2)
  return PriceOfCallOption, PriceOfPutOption

def PlotGraphsin_threeD(sValues, tValues, ArrayOfPricesOfCallOption, z_label, titleOfGraph):
  x, y, z = [], [], []
  for idx1 in range(len(tValues)):
    for idx2 in range(len(sValues)):
      x.append(sValues[idx2])
      y.append(tValues[idx1])
      z.append(ArrayOfPricesOfCallOption[idx1][idx2])
    
  threDvar = GraphPlotter.axes(projection='3d')
  threDvar.scatter3D(x, y, z, cmap='Greens',color='r')
  threDvar.set_zlabel(z_label)
  threDvar.set_ylabel("t")
  GraphPlotter.title(titleOfGraph)
  threDvar.set_xlabel("s") 
  GraphPlotter.show()

tValues = [0, 0.2, 0.4, 0.6, 0.8, 1]
T = 1
K = 1
r = 0.05
sigma = 0.6
PricesOfCallOption, PricesOfPutOption = [], []
sValues = npy.linspace(0.1, 2, num = 1000)
for t in tValues:
  ArrayOfPricesOfCallOption, ArrayOfPricesOfPutOption = [], []  
  for s in sValues:
    C, P = ClassicalBlackScholesMertonModel(s, t, T, K, r, sigma)
    ArrayOfPricesOfCallOption.append(C)
    ArrayOfPricesOfPutOption.append(P)
  PricesOfCallOption.append(ArrayOfPricesOfCallOption)
  PricesOfPutOption.append(ArrayOfPricesOfPutOption)

colors = ['red', 'blue', 'green', 'purple', 'orange',  'cyan']
v = 0
for IndexVariable in range(len(tValues)):
  GraphPlotter.plot(sValues, PricesOfCallOption[IndexVariable], label = f"t = {tValues[IndexVariable]}",color = colors[v])
  v += 1
v = 0
GraphPlotter.ylabel('C(t,s)')
GraphPlotter.legend()
GraphPlotter.title('Graph for C(t,s) versus s')
GraphPlotter.xlabel('s')
GraphPlotter.grid()
GraphPlotter.show()
PlotGraphsin_threeD(sValues, tValues, PricesOfCallOption, "C(t,s)", "Variation of C(t,s) with t and s")
for IndexVariable in range(len(tValues)):
  GraphPlotter.plot(sValues, PricesOfPutOption[IndexVariable], label = f"t = {tValues[IndexVariable]}",color = colors[v])
  v += 1
v = 0
GraphPlotter.ylabel('P(t,s)')
GraphPlotter.legend()
GraphPlotter.title('Graph for P(t,s) versus s')
GraphPlotter.xlabel('s')
GraphPlotter.grid()
GraphPlotter.show()
PlotGraphsin_threeD(sValues, tValues, PricesOfPutOption, "P(t,s)", "Variation of P(t,s) with t and s")