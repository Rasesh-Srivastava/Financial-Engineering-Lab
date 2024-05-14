import matplotlib.pyplot as GraphPlotter
import numpy as npy
from pandas import to_datetime
import math
import warnings
warnings.filterwarnings("ignore")
TypeOfStock = ['BSE', 'NSE']
TheStocksUsed = []
import pandas as pand
def GraphPlottingFunction(df, TheStocksUsed,TypeOfStock):
  interval = ['daily', 'weekly', 'monthly']
  df_initial = df.copy()
  for StoName in TheStocksUsed:
    df = df_initial.copy()
    for TheInterval in interval:
      if TheInterval == 'weekly':
        df['Day'] = (to_datetime(df['Date'])).dt.day_name()
        df = df.loc[df['Day'] == 'Monday']
        del df['Day']
      elif TheInterval == 'monthly':
        df = df.groupby(pand.DatetimeIndex(df['Date']).to_period('M')).nth(0)

      x = df['Date'].to_list()
      y = df[StoName].to_list()
      GraphPlotter.rcParams["figure.figsize"] = (20, 5)
      if TheInterval == 'daily':
        GraphPlotter.subplot(1, 3, 1)
      elif TheInterval == 'weekly':
        GraphPlotter.subplot(1, 3, 2)
      else:
        GraphPlotter.subplot(1, 3, 3)
      GraphPlotter.plot(x, y,color='red')
      GraphPlotter.xticks(npy.arange(0, len(x), int(len(x)/4)), df['Date'][0:len(x):int(len(x)/4)])
      GraphPlotter.suptitle(f'Graph for Stock prices for {StoName}', fontsize='12')
      GraphPlotter.ylabel('Price')
      GraphPlotter.title(f'On {TheInterval} basis')
      GraphPlotter.xlabel('Time')
      GraphPlotter.grid(True)
      if TheInterval == 'monthly':
        # GraphPlotter.savefig('./q1/Plots/' + TypeOfStock + '/' + StoName + '.png')
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
  GraphPlottingFunction(df, TheStocksUsed,tempO)