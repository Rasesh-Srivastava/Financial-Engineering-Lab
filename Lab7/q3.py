from scipy.stats import norm
from matplotlib import cm
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
T = 1
K = 1
r = 0.05
sigma = 0.6
PricesOfCallOption, PricesOfPutOption = [], []
sValues = npy.linspace(0.0001, 2, num = 100)
tValues = npy.linspace(0, 1, num = 100)
sValues, tValues = npy.meshgrid(sValues, tValues)
row, col = len(sValues), len(sValues[0])
for i in range(row):
  PricesOfCallOption.append([])
  PricesOfPutOption.append([])
  for j in range(col):
    C, P = ClassicalBlackScholesMertonModel(sValues[i][j], tValues[i][j], T, K, r, sigma)
    PricesOfCallOption[i].append(C)
    PricesOfPutOption[i].append(P)

PricesOfCallOption = npy.array(PricesOfCallOption)
PricesOfPutOption = npy.array(PricesOfPutOption)  
FigurePlotter = GraphPlotter.figure()
threDvar = FigurePlotter.add_subplot(projection='3d')
SurfacePlotter = threDvar.plot_surface(sValues, tValues, PricesOfCallOption, cmap=cm.copper)
FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
threDvar.set_zlabel("C(t,s)")
threDvar.set_ylabel("t") 
GraphPlotter.title('C(t,s) versus t and s')
threDvar.set_xlabel("s") 
GraphPlotter.show()
FigurePlotter = GraphPlotter.figure()
threDvar = FigurePlotter.add_subplot(projection='3d')
SurfacePlotter = threDvar.plot_surface(sValues, tValues, PricesOfPutOption, cmap=cm.viridis)
FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5,location='left')
threDvar.set_zlabel("P(t,s)")
threDvar.set_ylabel("t") 
GraphPlotter.title('P(t,s) versus t and s')
threDvar.set_xlabel("s") 
GraphPlotter.show()