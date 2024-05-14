import scipy.stats as stats
from pandas import to_datetime
import math
import numpy as npy
import matplotlib.pyplot as GraphPlotter
import warnings
warnings.filterwarnings("ignore")
TypeOfStock = ['BSE', 'NSE']
TheStocksUsed = []
import pandas as pand
def ReturnsGraphPlottingFunction(df, TheStocksUsed, TypeOfStock):
  interval = ['daily', 'weekly', 'monthly']
  df_initial = df.copy()
  GraphPlotter.rcParams["figure.figsize"] = (20, 5)
  for StoName in TheStocksUsed:
    df = df_initial.copy()
    for TheInterval in interval:
      if TheInterval == 'weekly':
        df['Day'] = (to_datetime(df['Date'])).dt.day_name()
        df = df.loc[df['Day'] == 'Monday']
        del df['Day']
      elif TheInterval == 'monthly':
        df = df.groupby(pand.DatetimeIndex(df['Date']).to_period('M')).nth(0)

      x = npy.log(df[StoName]/df[StoName].shift(1))
      mean = npy.nanmean(npy.array(x))
      std = npy.nanstd(npy.array(x))
      x = [(i - mean)/std for i in x]
      if TheInterval == 'daily':
        GraphPlotter.subplot(1, 3, 1)
      elif TheInterval == 'weekly':
        GraphPlotter.subplot(1, 3, 2)
      else:
        GraphPlotter.subplot(1, 3, 3)
      n_bins = 40
      GraphPlotter.hist(x, n_bins, density = True, edgecolor = 'black', linewidth = 0.4, color = 'cyan', label = 'Normalized returns')
      mu = 0
      variance = 1
      sigma = math.sqrt(variance)
      x = npy.linspace(mu - 3*sigma, mu + 3*sigma, 100)
      GraphPlotter.plot(x, stats.norm.pdf(x, mu, sigma), color = 'red', label = 'density function, N(0, 1)')
      GraphPlotter.ylabel('Normalised Frequency')
      GraphPlotter.xlabel('Returns')
      GraphPlotter.suptitle(f'Normalized returns with standard normal distribution for {StoName}', fontsize='12')
      GraphPlotter.title(f'On {TheInterval} basis')
      GraphPlotter.legend()
      if TheInterval == 'monthly':
        # GraphPlotter.savefig('./q3/Normalized_Plots/' + TypeOfStock + '/' + StoName + '.png')   
        GraphPlotter.show()

for tempO in TypeOfStock:
  FileToBeRead = ""
  if tempO == 'BSE':
    TheStocksUsed = ['RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'HINDUNILVR.BO', 'INFY.BO','KOTAKBANK.BO', 'ICICIBANK.BO', 'LT.BO', 'AXISBANK.BO', 'SBIN.BO','GOOGL', 'AAPL', 'AMZN', 'MSFT', 'NVDA', 'ADBE', 'NFLX', 'TSLA', 'ORCL', 'CSCO','Sensex']
    FileToBeRead = "bsedata1.csv"
  else:
    TheStocksUsed = ['RELIANCE.NS', 'TCS.NS', 'HINDUNILVR.NS', 'INFY.NS','KOTAKBANK.NS', 'ICICIBANK.NS', 'LT.NS', 'SBIN.NS', 'ITC.NS', 'ONGC.NS','NKE', 'BIDU', 'NVDA', 'KO', 'PYPL', 'SNAP', 'MCD', 'WMT', 'BABA', 'PEP','Nifty']
    FileToBeRead = "nsedata1.csv"
  
  df = pand.read_csv(FileToBeRead)
  ReturnsGraphPlottingFunction(df, TheStocksUsed, tempO)