import numpy as npy
import math
import matplotlib.pyplot as GraphPlotter
from matplotlib import cm
from scipy.stats import norm
from tabulate import tabulate
def ClassicalBlackScholesMertonModel(s, t, T, K, r, sigma):
  if t == T:
    return max(0, s - K), max(0, K - s)
  d2 = (math.log(s/K) + (r - 0.5 * sigma * sigma) * (T - t) ) / ( sigma * math.sqrt(T - t))
  d1 = (math.log(s/K) + (r + 0.5 * sigma * sigma) * (T - t) ) / ( sigma * math.sqrt(T - t))
  PriceOfPutOption = K * math.exp( -r * (T - t) ) * norm.cdf(-d2) - s * norm.cdf(-d1)
  PriceOfCallOption = s * norm.cdf(d1) - K * math.exp( -r * (T - t) ) * norm.cdf(d2)
  return PriceOfCallOption, PriceOfPutOption

def VaryingKAndsigma(s, t, T, r):
  print("Variation of C(t,s) and P(t,s) with K and sigma\n")
  PricesOfCallOption, PricesOfPutOption = [], []
  vAluesOfK = npy.linspace(0.01, 2, num = 100)
  vAluesOfSigma = npy.linspace(0.01, 1, num = 100, endpoint = False)
  vAluesOfK, vAluesOfSigma = npy.meshgrid(vAluesOfK, vAluesOfSigma)
  row, col = len(vAluesOfK), len(vAluesOfK[0])
  for i in range(row):
    PricesOfCallOption.append([])
    PricesOfPutOption.append([])
    for j in range(col):
      C, P = ClassicalBlackScholesMertonModel(s, t, T, vAluesOfK[i][j], r, vAluesOfSigma[i][j])
      PricesOfCallOption[i].append(C)
      PricesOfPutOption[i].append(P)
  PricesOfCallOption = npy.array(PricesOfCallOption)
  PricesOfPutOption = npy.array(PricesOfPutOption)  
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(vAluesOfK, vAluesOfSigma, PricesOfCallOption, cmap=cm.copper)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("C(t,s)")
  GraphPlotter.title('C(t,s) versus K and sigma')
  threDvar.set_ylabel("sigma") 
  threDvar.set_xlabel("K") 
  GraphPlotter.show()
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(vAluesOfK, vAluesOfSigma, PricesOfPutOption, cmap=cm.viridis)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("P(t,s)")
  GraphPlotter.title('P(t,s) versus K and sigma')
  threDvar.set_ylabel("sigma") 
  threDvar.set_xlabel("K") 
  GraphPlotter.show()

def Varyingr(T, K, sigma):
  t = 0
  sValues = [0.4, 0.6, 0.8, 1.0, 1.2]
  r_list = npy.linspace(0, 1, num = 500, endpoint = False)
  PricesOfCallOption, PricesOfPutOption = [], []
  cntr = 0
  data = []
  for s in sValues:
    EuropeanCallOptionPricesArray, EuropeanPutOptionPricesArray = [], []
    for r in r_list:
      C, P = ClassicalBlackScholesMertonModel(s, t, T, K, r, sigma)
      EuropeanCallOptionPricesArray.append(C)
      EuropeanPutOptionPricesArray.append(P)
      if s == 0.8:
          if cntr % 50 == 0:
            data.append([1 + int(cntr/50), r, C, P])
          cntr += 1
    PricesOfCallOption.append(EuropeanCallOptionPricesArray)
    PricesOfPutOption.append(EuropeanPutOptionPricesArray)
  print("Variation of C(t,s) and P(t,s) with r\n")
  heading = ['Serial Number', 'r', 'C(t,s)', 'P(t,s)']
  print(tabulate(data, headers = heading))
  for IndexVariable in range(len(sValues)):
    GraphPlotter.plot(r_list, PricesOfCallOption[IndexVariable], label = f's = {sValues[IndexVariable]}')
  GraphPlotter.grid()
  GraphPlotter.ylabel('C(t,s)')
  GraphPlotter.title('Graph for C(t,s) versus r')
  GraphPlotter.xlabel('r')
  GraphPlotter.legend()
  GraphPlotter.show()
  for IndexVariable in range(len(sValues)):
    GraphPlotter.plot(r_list, PricesOfPutOption[IndexVariable], label = f's = {sValues[IndexVariable]}')
  GraphPlotter.xlabel('r')
  GraphPlotter.ylabel('P(t,s)')
  GraphPlotter.title('Graph for P(t,s) versus r')
  GraphPlotter.legend()
  GraphPlotter.grid()
  GraphPlotter.show()

def VaryingKAndr(s, t, T, sigma):
  print("Variation of C(t,s) and P(t,s) with K and r\n")
  PricesOfCallOption, PricesOfPutOption = [], []
  vAluesOfK = npy.linspace(0.01, 2, num = 100)
  r_list = npy.linspace(0, 1, num = 100, endpoint = False)
  vAluesOfK, r_list = npy.meshgrid(vAluesOfK, r_list)
  row, col = len(vAluesOfK), len(vAluesOfK[0])
  for i in range(row):
    PricesOfCallOption.append([])
    PricesOfPutOption.append([])
    for j in range(col):
      C, P = ClassicalBlackScholesMertonModel(s, t, T, vAluesOfK[i][j], r_list[i][j], sigma)
      PricesOfCallOption[i].append(C)
      PricesOfPutOption[i].append(P)
  PricesOfCallOption = npy.array(PricesOfCallOption)
  PricesOfPutOption = npy.array(PricesOfPutOption)  
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(vAluesOfK, r_list, PricesOfCallOption, cmap=cm.copper)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("C(t,s)")
  GraphPlotter.title('C(t,s) versus K and r')
  threDvar.set_ylabel("r") 
  threDvar.set_xlabel("K") 
  GraphPlotter.show()
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(vAluesOfK, r_list, PricesOfPutOption, cmap=cm.viridis)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("P(t,s)")
  GraphPlotter.title('P(t,s) versus K and r')
  threDvar.set_ylabel("r") 
  threDvar.set_xlabel("K") 
  GraphPlotter.show()

def VaryingTAndK(s, t, r, sigma):
  print("Variation of C(t,s) and P(t,s) with T and K\n")
  PricesOfCallOption, PricesOfPutOption = [], []
  vAluesOfK = npy.linspace(0.01, 2, num = 100)
  ValuesOfTpossible = npy.linspace(0.1, 5, num = 100)
  vAluesOfK, ValuesOfTpossible = npy.meshgrid(vAluesOfK, ValuesOfTpossible)
  row, col = len(vAluesOfK), len(vAluesOfK[0])
  for i in range(row):
    PricesOfCallOption.append([])
    PricesOfPutOption.append([])
    for j in range(col):
      C, P = ClassicalBlackScholesMertonModel(s, t, ValuesOfTpossible[i][j], vAluesOfK[i][j], r, sigma)
      PricesOfCallOption[i].append(C)
      PricesOfPutOption[i].append(P)
  PricesOfCallOption = npy.array(PricesOfCallOption)
  PricesOfPutOption = npy.array(PricesOfPutOption)  
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(vAluesOfK, ValuesOfTpossible, PricesOfCallOption, cmap=cm.copper)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("C(t,s)")
  GraphPlotter.title('C(t,s) versus K and T')
  threDvar.set_ylabel("T") 
  threDvar.set_xlabel("K") 
  GraphPlotter.show()
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(vAluesOfK, ValuesOfTpossible, PricesOfPutOption, cmap=cm.viridis)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("P(t,s)")
  GraphPlotter.title('P(t,s) versus K and T')
  threDvar.set_ylabel("T") 
  threDvar.set_xlabel("K") 
  GraphPlotter.show()

def VaryingrAndsigma(s, t, T, K):
  print("Variation of C(t,s) and P(t,s) with r and sigma\n")
  PricesOfCallOption, PricesOfPutOption = [], []
  vAluesOfSigma = npy.linspace(0.01, 1, num = 100, endpoint = False)
  r_list = npy.linspace(0.001, 1, num = 100, endpoint = False)
  vAluesOfSigma, r_list = npy.meshgrid(vAluesOfSigma, r_list)
  row, col = len(vAluesOfSigma), len(vAluesOfSigma[0])
  for i in range(row):
    PricesOfCallOption.append([])
    PricesOfPutOption.append([])
    for j in range(col):
      C, P = ClassicalBlackScholesMertonModel(s, t, T, K, r_list[i][j], vAluesOfSigma[i][j])
      PricesOfCallOption[i].append(C)
      PricesOfPutOption[i].append(P)
  PricesOfCallOption = npy.array(PricesOfCallOption)
  PricesOfPutOption = npy.array(PricesOfPutOption)  
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(vAluesOfSigma, r_list, PricesOfCallOption, cmap=cm.copper)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("C(t,s)")
  GraphPlotter.title('C(t,s) versus sigma and r')
  threDvar.set_ylabel("r") 
  threDvar.set_xlabel("sigma") 
  GraphPlotter.show()
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(vAluesOfSigma, r_list, PricesOfPutOption, cmap=cm.viridis)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("P(t,s)")
  GraphPlotter.title('P(t,s) versus sigma and r')
  threDvar.set_ylabel("r") 
  threDvar.set_xlabel("sigma") 
  GraphPlotter.show()

def VaryingTAndr(s, t, K, sigma):
  print("Variation of C(t,s) and P(t,s) with T and r\n")
  PricesOfCallOption, PricesOfPutOption = [], []
  r_list = npy.linspace(0.01, 1, num = 100)
  ValuesOfTpossible = npy.linspace(0.1, 5, num = 100)
  r_list, ValuesOfTpossible = npy.meshgrid(r_list, ValuesOfTpossible)
  row, col = len(r_list), len(r_list[0])
  for i in range(row):
    PricesOfCallOption.append([])
    PricesOfPutOption.append([])
    for j in range(col):
      C, P = ClassicalBlackScholesMertonModel(s, t, ValuesOfTpossible[i][j], K, r_list[i][j], sigma)
      PricesOfCallOption[i].append(C)
      PricesOfPutOption[i].append(P)
  PricesOfCallOption = npy.array(PricesOfCallOption)
  PricesOfPutOption = npy.array(PricesOfPutOption)  
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(ValuesOfTpossible, r_list, PricesOfCallOption, cmap=cm.copper)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("C(t,s)")
  GraphPlotter.title('C(t,s) versus T and r')
  threDvar.set_ylabel("r") 
  threDvar.set_xlabel("T") 
  GraphPlotter.show()
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(ValuesOfTpossible, r_list, PricesOfPutOption, cmap=cm.viridis)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("P(t,s)")
  GraphPlotter.title('P(t,s) versus T and r')
  threDvar.set_ylabel("r") 
  threDvar.set_xlabel("T") 
  GraphPlotter.show()

def VaryingTAndsigma(s, t, K, r):
  print("Variation of C(t,s) and P(t,s) with T and sigma\n")
  PricesOfCallOption, PricesOfPutOption = [], []
  vAluesOfSigma = npy.linspace(0.01, 1, num = 100)
  ValuesOfTpossible = npy.linspace(0.1, 5, num = 100)
  vAluesOfSigma, ValuesOfTpossible = npy.meshgrid(vAluesOfSigma, ValuesOfTpossible)
  row, col = len(vAluesOfSigma), len(vAluesOfSigma[0])
  for i in range(row):
    PricesOfCallOption.append([])
    PricesOfPutOption.append([])
    for j in range(col):
      C, P = ClassicalBlackScholesMertonModel(s, t, ValuesOfTpossible[i][j], K, r, vAluesOfSigma[i][j])
      PricesOfCallOption[i].append(C)
      PricesOfPutOption[i].append(P)
  PricesOfCallOption = npy.array(PricesOfCallOption)
  PricesOfPutOption = npy.array(PricesOfPutOption)  
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(ValuesOfTpossible, vAluesOfSigma, PricesOfCallOption, cmap=cm.copper)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("C(t,s)")
  GraphPlotter.title('C(t,s) versus T and sigma')
  threDvar.set_ylabel("sigma") 
  threDvar.set_xlabel("T") 
  GraphPlotter.show()
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(ValuesOfTpossible, vAluesOfSigma, PricesOfPutOption, cmap=cm.viridis)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("P(t,s)")
  GraphPlotter.title('P(t,s) versus T and sigma')
  threDvar.set_ylabel("sigma") 
  threDvar.set_xlabel("T") 
  GraphPlotter.show()

def VaryingT(K, r, sigma):
  t = 0
  sValues = [0.4, 0.6, 0.8, 1.0, 1.2]
  ValuesOfTpossible = npy.linspace(0.1, 5, num = 500)
  PricesOfCallOption, PricesOfPutOption = [], []
  cntr = 0
  data = []
  for s in sValues:
    EuropeanCallOptionPricesArray, EuropeanPutOptionPricesArray = [], []
    for T in ValuesOfTpossible:
      C, P = ClassicalBlackScholesMertonModel(s, t, T, K, r, sigma)
      EuropeanCallOptionPricesArray.append(C)
      EuropeanPutOptionPricesArray.append(P)
      if s == 0.8:
          if cntr % 50 == 0:
            data.append([1 + int(cntr/50), T, C, P])
          cntr += 1
    PricesOfCallOption.append(EuropeanCallOptionPricesArray)
    PricesOfPutOption.append(EuropeanPutOptionPricesArray)
  print("Variation of C(t,s) and P(t,s) with T\n")
  heading = ['Serial Number', 'T', 'C(t,s)', 'P(t,s)']
  print(tabulate(data, headers = heading))
  for IndexVariable in range(len(sValues)):
    GraphPlotter.plot(ValuesOfTpossible, PricesOfCallOption[IndexVariable], label = f's = {sValues[IndexVariable]}')
  GraphPlotter.grid()
  GraphPlotter.ylabel('C(t,s)')
  GraphPlotter.title('Graph for C(t,s) versus T')
  GraphPlotter.xlabel('T')
  GraphPlotter.legend()
  GraphPlotter.show()
  for IndexVariable in range(len(sValues)):
    GraphPlotter.plot(ValuesOfTpossible, PricesOfPutOption[IndexVariable], label = f's = {sValues[IndexVariable]}')
  GraphPlotter.grid()
  GraphPlotter.ylabel('P(t,s)')
  GraphPlotter.title('Graph for P(t,s) versus T')
  GraphPlotter.xlabel('T')
  GraphPlotter.legend()
  GraphPlotter.show()

def VaryingTAnds(t, K, r, sigma):
  print("Variation of C(t,s) and P(t,s) with T and s\n")
  PricesOfCallOption, PricesOfPutOption = [], []
  sValues = npy.linspace(0.2, 2, num = 100)
  ValuesOfTpossible = npy.linspace(0.1, 5, num = 100)
  sValues, ValuesOfTpossible = npy.meshgrid(sValues, ValuesOfTpossible)
  row, col = len(sValues), len(sValues[0])
  for i in range(row):
    PricesOfCallOption.append([])
    PricesOfPutOption.append([])
    for j in range(col):
      C, P = ClassicalBlackScholesMertonModel(sValues[i][j], t, ValuesOfTpossible[i][j], K, r, sigma)
      PricesOfCallOption[i].append(C)
      PricesOfPutOption[i].append(P)
  PricesOfCallOption = npy.array(PricesOfCallOption)
  PricesOfPutOption = npy.array(PricesOfPutOption)  
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(ValuesOfTpossible, sValues, PricesOfCallOption, cmap=cm.copper)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("C(t,s)")
  GraphPlotter.title('C(t,s) versus T and s')
  threDvar.set_ylabel("s") 
  threDvar.set_xlabel("T") 
  GraphPlotter.show()
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(ValuesOfTpossible, sValues, PricesOfPutOption, cmap=cm.viridis)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("P(t,s)")
  GraphPlotter.title('P(t,s) versus T and s')
  threDvar.set_ylabel("s") 
  threDvar.set_xlabel("T") 
  GraphPlotter.show()

def VaryingsAndsigma(t, K, T, r):
  print("Variation of C(t,s) and P(t,s) with s and sigma\n")
  PricesOfCallOption, PricesOfPutOption = [], []
  sValues = npy.linspace(0.2, 2, num = 100)
  vAluesOfSigma = npy.linspace(0.01, 1, num = 100)
  sValues, vAluesOfSigma = npy.meshgrid(sValues, vAluesOfSigma)
  row, col = len(sValues), len(sValues[0])
  for i in range(row):
    PricesOfCallOption.append([])
    PricesOfPutOption.append([])
    for j in range(col):
      C, P = ClassicalBlackScholesMertonModel(sValues[i][j], t, T, K, r, vAluesOfSigma[i][j])
      PricesOfCallOption[i].append(C)
      PricesOfPutOption[i].append(P)
  PricesOfCallOption = npy.array(PricesOfCallOption)
  PricesOfPutOption = npy.array(PricesOfPutOption)  
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(sValues, vAluesOfSigma, PricesOfCallOption, cmap=cm.copper)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("C(t,s)")
  GraphPlotter.title('C(t,s) versus s and sigma')
  threDvar.set_ylabel("sigma") 
  threDvar.set_xlabel("s") 
  GraphPlotter.show()
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(sValues, vAluesOfSigma, PricesOfPutOption, cmap=cm.viridis)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("P(t,s)")
  GraphPlotter.title('P(t,s) versus s and sigma')
  threDvar.set_ylabel("sigma") 
  threDvar.set_xlabel("s") 
  GraphPlotter.show()

def VaryingsAndr(t, K, T, sigma):
  print("Variation of C(t,s) and P(t,s) with s and r\n")
  PricesOfCallOption, PricesOfPutOption = [], []
  sValues = npy.linspace(0.2, 2, num = 100)
  r_list = npy.linspace(0.01, 1, num = 100)
  sValues, r_list = npy.meshgrid(sValues, r_list)
  row, col = len(sValues), len(sValues[0])
  for i in range(row):
    PricesOfCallOption.append([])
    PricesOfPutOption.append([])
    for j in range(col):
      C, P = ClassicalBlackScholesMertonModel(sValues[i][j], t, T, K, r_list[i][j], sigma)
      PricesOfCallOption[i].append(C)
      PricesOfPutOption[i].append(P)
  PricesOfCallOption = npy.array(PricesOfCallOption)
  PricesOfPutOption = npy.array(PricesOfPutOption)  
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(sValues, r_list, PricesOfCallOption, cmap=cm.copper)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("C(t,s)")
  GraphPlotter.title('C(t,s) versus s and r')
  threDvar.set_ylabel("r") 
  threDvar.set_xlabel("s") 
  GraphPlotter.show()
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(sValues, r_list, PricesOfPutOption, cmap=cm.viridis)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("P(t,s)")
  GraphPlotter.title('P(t,s) versus s and r')
  threDvar.set_ylabel("r") 
  threDvar.set_xlabel("s") 
  GraphPlotter.show()

def Varyingsigma(T, K, r):
  t = 0
  sValues = [0.4, 0.6, 0.8, 1.0, 1.2]
  vAluesOfSigma = npy.linspace(0.001, 1, num = 500, endpoint = False)
  PricesOfCallOption, PricesOfPutOption = [], []
  cntr = 0
  data = []
  for s in sValues:
    EuropeanCallOptionPricesArray, EuropeanPutOptionPricesArray = [], []
    for sigma in vAluesOfSigma:
      C, P = ClassicalBlackScholesMertonModel(s, t, T, K, r, sigma)
      EuropeanCallOptionPricesArray.append(C)
      EuropeanPutOptionPricesArray.append(P)
      if s == 0.8:
          if cntr % 50 == 0:
            data.append([1 + int(cntr/50), sigma, C, P])
          cntr += 1
    PricesOfCallOption.append(EuropeanCallOptionPricesArray)
    PricesOfPutOption.append(EuropeanPutOptionPricesArray)
  print("Variation of C(t,s) and P(t,s) with sigma\n")
  heading = ['Serial No.', 'sigma', 'C(t,s)', 'P(t,s)']
  print(tabulate(data, headers = heading))
  for IndexVariable in range(len(sValues)):
    GraphPlotter.plot(vAluesOfSigma, PricesOfCallOption[IndexVariable], label = f's = {sValues[IndexVariable]}')
  GraphPlotter.grid()
  GraphPlotter.ylabel('C(t,s)')
  GraphPlotter.title('Graph for C(t,s) versus sigma')
  GraphPlotter.xlabel('sigma')
  GraphPlotter.legend()
  GraphPlotter.show()
  for IndexVariable in range(len(sValues)):
    GraphPlotter.plot(vAluesOfSigma, PricesOfPutOption[IndexVariable], label = f's = {sValues[IndexVariable]}')
  GraphPlotter.grid()
  GraphPlotter.ylabel('P(t,s)')
  GraphPlotter.title('Graph for P(t,s) versus sigma')
  GraphPlotter.xlabel('sigma')
  GraphPlotter.legend()
  GraphPlotter.show()

def VaryingKAnds(t, T, r, sigma):
  print("Variation of C(t,s) and P(t,s) with K and s\n")
  PricesOfCallOption, PricesOfPutOption = [], []
  vAluesOfK = npy.linspace(0.01, 2, num = 100)
  sValues = npy.linspace(0.2, 2, num = 100)
  vAluesOfK, sValues = npy.meshgrid(vAluesOfK, sValues)
  row, col = len(sValues), len(sValues[0])
  for i in range(row):
    PricesOfCallOption.append([])
    PricesOfPutOption.append([])
    for j in range(col):
      C, P = ClassicalBlackScholesMertonModel(sValues[i][j], t, T, vAluesOfK[i][j], r, sigma)
      PricesOfCallOption[i].append(C)
      PricesOfPutOption[i].append(P)
  PricesOfCallOption = npy.array(PricesOfCallOption)
  PricesOfPutOption = npy.array(PricesOfPutOption)  
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(vAluesOfK, sValues, PricesOfCallOption, cmap=cm.copper)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("C(t,s)")
  GraphPlotter.title('C(t,s) versus K and s')
  threDvar.set_ylabel("s") 
  threDvar.set_xlabel("K") 
  GraphPlotter.show()
  FigurePlotter = GraphPlotter.figure()
  threDvar = FigurePlotter.add_subplot(projection='3d')
  SurfacePlotter = threDvar.plot_surface(vAluesOfK, sValues, PricesOfPutOption, cmap=cm.viridis)
  FigurePlotter.colorbar(SurfacePlotter, shrink=0.5, aspect=5)
  threDvar.set_zlabel("P(t,s)")
  GraphPlotter.title('P(t,s) versus K and s')
  threDvar.set_ylabel("s") 
  threDvar.set_xlabel("K") 
  GraphPlotter.show()

def VaryingK(T, r, sigma):
  t = 0
  sValues = [0.4, 0.6, 0.8, 1.0, 1.2]
  vAluesOfK = npy.linspace(0.1, 2, num = 500)
  PricesOfCallOption, PricesOfPutOption = [], []
  cntr = 0
  data = []
  for s in sValues:
    EuropeanCallOptionPricesArray, EuropeanPutOptionPricesArray = [], []
    for K in vAluesOfK:
      C, P = ClassicalBlackScholesMertonModel(s, t, T, K, r, sigma)
      EuropeanCallOptionPricesArray.append(C)
      EuropeanPutOptionPricesArray.append(P)
      if s == 0.8:
        if cntr % 50 == 0:
          data.append([1 + int(cntr/50), K, C, P])
        cntr += 1
    PricesOfCallOption.append(EuropeanCallOptionPricesArray)
    PricesOfPutOption.append(EuropeanPutOptionPricesArray)
  print("Variation of C(t,s) and P(t,s) with K\n")
  heading = ['Serial Number', 'K', 'C(t,s)', 'P(t,s)']
  print(tabulate(data, headers = heading))
  for IndexVariable in range(len(sValues)):
    GraphPlotter.plot(vAluesOfK, PricesOfCallOption[IndexVariable], label = f's = {sValues[IndexVariable]}')
  GraphPlotter.grid()
  GraphPlotter.ylabel('C(t,s)')
  GraphPlotter.title('Graph for C(t,s) versus K')
  GraphPlotter.xlabel('K')
  GraphPlotter.legend()
  GraphPlotter.show()
  for IndexVariable in range(len(sValues)):
    GraphPlotter.plot(vAluesOfK, PricesOfPutOption[IndexVariable], label = f's = {sValues[IndexVariable]}')
  GraphPlotter.grid()
  GraphPlotter.ylabel('P(t,s)')
  GraphPlotter.title('Graph for P(t,s) versus K')
  GraphPlotter.xlabel('K')
  GraphPlotter.legend()
  GraphPlotter.show()

VaryingT(1, 0.05, 0.6)
VaryingK(1, 0.05, 0.6)
Varyingr(1, 1, 0.6)
Varyingsigma(1, 1, 0.05)
VaryingKAndr(0.8, 0, 1, 0.6)
VaryingKAndsigma(0.8, 0, 1, 0.05)
VaryingrAndsigma(0.8, 0, 1, 1)
VaryingTAndK(0.8, 0, 0.05, 0.6)
VaryingTAndr(0.8, 0, 1, 0.6)
VaryingTAndsigma(0.8, 0, 1, 0.05)
VaryingKAnds(0, 1, 0.05, 0.6)
VaryingTAnds(0, 1, 0.05, 0.6)
VaryingsAndr(0, 1, 1, 0.6)
VaryingsAndsigma(0, 1, 1, 0.05)