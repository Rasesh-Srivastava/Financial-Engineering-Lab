import matplotlib.pyplot as GraphPlotter
from pandas import to_datetime
import numpy as npy
import warnings
warnings.filterwarnings("ignore")
import math
TypeOfStock = ['BSE', 'NSE']
TheStocksUsed = []
import pandas as pand
def GraphPlottingFunction(df1, df2, StoName, TheInterval, TypeOfStock):
  x = df1['Date'].to_list()
  y1 = df1[StoName].to_list()
  y2 = df2[StoName].to_list()
  GraphPlotter.rcParams["figure.figsize"] = (20, 5)
  if TheInterval == 'daily':
    GraphPlotter.subplot(1, 1, 1)
  elif TheInterval == 'weekly':
    GraphPlotter.subplot(1, 3, 2)
  else:
    GraphPlotter.subplot(1, 3, 3)
  GraphPlotter.plot(x, y1, color = 'green', label = 'Original Price')
  GraphPlotter.plot(x, y2, color = 'red', label = 'Predicted Price')
  GraphPlotter.xticks(npy.arange(0, len(x), int(len(x)/4)), df1['Date'][0:len(x):int(len(x)/4)],fontsize='8')
  GraphPlotter.suptitle(f'Graph for Stock prices for {StoName}', fontsize='12')
  GraphPlotter.ylabel('Price')
  GraphPlotter.title(f'On {TheInterval} basis')
  GraphPlotter.xlabel('Time')
  GraphPlotter.grid(True)
  GraphPlotter.legend()
  if TheInterval == 'daily':
    # GraphPlotter.savefig('./q4/Estimation_Plots/' + TypeOfStock + '/' + StoName + '.png')
    GraphPlotter.show()

def generate_path(df, TheStocksUsed, TypeOfStock):
  df = df.fillna(method ='bfill')
  interval = ['daily',]
  initial_df = df.copy()
  for StoName in TheStocksUsed:
    df = initial_df.copy()
    for TheInterval in interval:
      delta_t = 1/252
      df = initial_df.copy()
      if TheInterval == 'weekly':
        df['Day'] = (to_datetime(df['Date'])).dt.day_name()
        df = df.loc[df['Day'] == 'Monday']
        del df['Day']
        delta_t = 7/252
      elif TheInterval == 'monthly':
        df = df.groupby(pand.DatetimeIndex(df['Date']).to_period('M')).nth(0)
        delta_t = 30/252

      df_original = df.copy()
      trainingDataframe = df.loc[ df['Date'] <= '2022-12-31']
      predictedDataframe = df.loc[ df['Date'] > '2022-12-31']
      predictedDataframe.set_index('Date', inplace = True)
      x = npy.log(predictedDataframe[StoName]/predictedDataframe[StoName].shift(1))
      mean = npy.nanmean(npy.array(x)) 
      Variance = npy.nanvar(npy.array(x))
      MultiplyingFactor = 0
      if TheInterval == 'daily':
        MultiplyingFactor = 252
      elif TheInterval == 'weekly':
        MultiplyingFactor = 52
      else:
        MultiplyingFactor = 12
      
      mean *= MultiplyingFactor
      Variance *= (len(x) * MultiplyingFactor) / (len(x) - 1)
      mean += 0.5 * Variance
      npy.random.seed(40)
      S0 = trainingDataframe.iloc[len(trainingDataframe) - 1][StoName]
      for idx, row in predictedDataframe.iterrows():
        S = S0 * math.exp((mean - 0.5 * Variance) * delta_t + math.sqrt(Variance) * math.sqrt(delta_t) * npy.random.normal(0, 1))
        S0 = S
        row[StoName] = S

      predictedDataframe = trainingDataframe.append(predictedDataframe, ignore_index=True)
      GraphPlottingFunction(df_original, predictedDataframe, StoName, TheInterval, TypeOfStock)

for tempO in TypeOfStock:
  FileToBeRead = ""
  if tempO == 'BSE':
    TheStocksUsed = ['RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'HINDUNILVR.BO', 'INFY.BO','KOTAKBANK.BO', 'ICICIBANK.BO', 'LT.BO', 'AXISBANK.BO', 'SBIN.BO','GOOGL', 'AAPL', 'AMZN', 'MSFT', 'NVDA', 'ADBE', 'NFLX', 'TSLA', 'ORCL', 'CSCO','Sensex']
    FileToBeRead = "bsedata1.csv"
  else:
    TheStocksUsed = ['RELIANCE.NS', 'TCS.NS', 'HINDUNILVR.NS', 'INFY.NS','KOTAKBANK.NS', 'ICICIBANK.NS', 'LT.NS', 'SBIN.NS', 'ITC.NS', 'ONGC.NS','NKE', 'BIDU', 'NVDA', 'KO', 'PYPL', 'SNAP', 'MCD', 'WMT', 'BABA', 'PEP','Nifty']
    FileToBeRead = "nsedata1.csv"
  df = pand.read_csv(FileToBeRead)
  generate_path(df, TheStocksUsed, tempO)