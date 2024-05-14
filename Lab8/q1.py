from scipy.stats import norm
from tabulate import tabulate
import pandas as pand
import math
import matplotlib.pyplot as GraphPlotter
import numpy as npy
def q1a():
  def HistVolt(bseORnse):
    TP = 1
    sList = []
    FN = ''
    if bseORnse == 'BSE':
        sList = ['RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'HINDUNILVR.BO', 'INFY.BO','KOTAKBANK.BO', 'ICICIBANK.BO', 'LT.BO', 'AXISBANK.BO', 'SBIN.BO','GOOGL', 'AAPL', 'AMZN', 'MSFT', 'NVDA', 'ADBE', 'NFLX', 'TSLA', 'ORCL', 'CSCO','Sensex']
        FN = 'bsedata1.csv'
    elif bseORnse == 'NSE':
        sList = ['RELIANCE.NS', 'TCS.NS', 'HINDUNILVR.NS', 'INFY.NS','KOTAKBANK.NS', 'ICICIBANK.NS', 'LT.NS', 'SBIN.NS', 'ITC.NS', 'ONGC.NS','NKE', 'BIDU', 'NVDA', 'KO', 'PYPL', 'SNAP', 'MCD', 'WMT', 'BABA', 'PEP','Nifty']
        FN = 'nsedata1.csv'
    df = pand.read_csv(FN)
    dfMon = df.groupby(pand.DatetimeIndex(df.Date).to_period('M')).nth(0)
    start_Index = 60 - TP
    dfRed = dfMon.iloc[start_Index :]
    dfRed.reset_index(inplace = True, drop = True) 
    Index_list = df.index[df['Date'] >= dfRed.iloc[0]['Date']].tolist()
    dfRed = df.iloc[Index_list[0] :]
    MyInfo = dfRed.set_index('Date')
    MyInfo = MyInfo.pct_change(fill_method=None)
    TabulationVar = []
    Volatil = []
    for sname in sList:
        returns = MyInfo[sname]
        x = returns.to_list()
        std = npy.nanstd(npy.array(x))
        Volatil.append(std * math.sqrt(252))
    for i in range(len(Volatil)):
        TabulationVar.append([i + 1, sList[i], Volatil[i]])
    
    print(tabulate(TabulationVar, headers = ['Serial No.', 'Stock\'s Name', 'Historical Volatility']))

  print("Historical Volatility from last one month's data for BSE")
  HistVolt('BSE')
  print('\n')
  print("Historical Volatility from last one month's data for NSE")
  HistVolt('NSE')


def q1b():
  def OptionPriceCalc(x, t, T, K, r, sigma):
    if t == T:
        return max(0, x - K), max(0, K - x)
    d2 = ( math.log(x/K) + (r - 0.5 * sigma * sigma) * (T - t) ) / ( sigma * math.sqrt(T - t) )
    d1 = ( math.log(x/K) + (r + 0.5 * sigma * sigma) * (T - t) ) / ( sigma * math.sqrt(T - t) )
    PriceOfPutOption = K * math.exp( -r * (T - t) ) * norm.cdf(-d2) - x * norm.cdf(-d1)
    PriceOfCallOption = x * norm.cdf(d1) - K * math.exp( -r * (T - t) ) * norm.cdf(d2)
    return PriceOfCallOption, PriceOfPutOption

  def HistVolt(bseORnse):
    TP = 1
    sList = []
    FN = ''
    if bseORnse == 'BSE':
        sList = ['RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'HINDUNILVR.BO', 'INFY.BO','KOTAKBANK.BO', 'ICICIBANK.BO', 'LT.BO', 'AXISBANK.BO', 'SBIN.BO','GOOGL', 'AAPL', 'AMZN', 'MSFT', 'NVDA', 'ADBE', 'NFLX', 'TSLA', 'ORCL', 'CSCO','Sensex']
        FN = 'bsedata1.csv'
    else:
        sList = ['RELIANCE.NS', 'TCS.NS', 'HINDUNILVR.NS', 'INFY.NS','KOTAKBANK.NS', 'ICICIBANK.NS', 'LT.NS', 'SBIN.NS', 'ITC.NS', 'ONGC.NS','NKE', 'BIDU', 'NVDA', 'KO', 'PYPL', 'SNAP', 'MCD', 'WMT', 'BABA', 'PEP','Nifty']
        FN = 'nsedata1.csv'
    df = pand.read_csv(FN)
    dfMon = df.groupby(pand.DatetimeIndex(df.Date).to_period('M')).nth(0)
    start_Index = 60 - TP
    dfRed = dfMon.iloc[start_Index :]
    dfRed.reset_index(inplace = True, drop = True) 
    Index_list = df.index[df['Date'] >= dfRed.iloc[0]['Date']].tolist()
    dfRed = df.iloc[Index_list[0] :]
    MyInfo = dfRed.set_index('Date')
    MyInfo = MyInfo.pct_change(fill_method=None)
    Volatil = []
    TabulationVar = []
    for sname in sList:
        returns = MyInfo[sname]
        x = returns.to_list()
        std = npy.nanstd(npy.array(x))
        Volatil.append(std * math.sqrt(252))
    for i in range(len(Volatil)):
        TabulationVar.append([i + 1, sList[i], Volatil[i]])
    return Volatil

  def pComp(bseORnse):
    sList = []
    FN = ''
    if bseORnse == 'BSE':
        sList = ['RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'HINDUNILVR.BO', 'INFY.BO','KOTAKBANK.BO', 'ICICIBANK.BO', 'LT.BO', 'AXISBANK.BO', 'SBIN.BO','GOOGL', 'AAPL', 'AMZN', 'MSFT', 'NVDA', 'ADBE', 'NFLX', 'TSLA', 'ORCL', 'CSCO','Sensex']
        FN = 'bsedata1.csv'
    else:
        sList = ['RELIANCE.NS', 'TCS.NS', 'HINDUNILVR.NS', 'INFY.NS','KOTAKBANK.NS', 'ICICIBANK.NS', 'LT.NS', 'SBIN.NS', 'ITC.NS', 'ONGC.NS','NKE', 'BIDU', 'NVDA', 'KO', 'PYPL', 'SNAP', 'MCD', 'WMT', 'BABA', 'PEP','Nifty']
        FN = 'nsedata1.csv'
    df = pand.read_csv(FN)
    df['Date'] = pand.to_datetime(df['Date'])
    df = df.interpolate(method ='linear', limit_direction ='forward')
    r = 0.05
    T = 6/12
    sigma_list = HistVolt(bseORnse)
    for Index1 in range(len(sList)):
        TabulationVar = []
        print('\n')
        print(f"For the Stock: {sList[Index1]}")
        sigma = sigma_list[Index1]
        print("Historical Volatility from last one month's data =", sigma, "\n")
        S0 = df.iloc[len(df) - 1][sList[Index1]]
        for Index2 in range(5, 16):
            K = S0 * round(Index2 * 0.1, 2)
            call, put = OptionPriceCalc(S0, 0, T, K, r, sigma)
            TabulationVar.append([str(round(Index2 * 0.1, 2)) + "*S0", call, put])

        print(tabulate(TabulationVar, headers = ["Strike price (K)", "Price of Call Option", "Price of Put Option"]))

  pComp('BSE')
  pComp('NSE') 


q1a()
q1b()
def OptionPriceCalc(x, t, T, K, r, sigma):
  if t == T:
    return max(0, x - K), max(0, K - x)
  d2 = ( math.log(x/K) + (r - 0.5 * sigma * sigma) * (T - t) ) / ( sigma * math.sqrt(T - t) )
  d1 = ( math.log(x/K) + (r + 0.5 * sigma * sigma) * (T - t) ) / ( sigma * math.sqrt(T - t) )
  PriceOfPutOption = K * math.exp( -r * (T - t) ) * norm.cdf(-d2) - x * norm.cdf(-d1)
  PriceOfCallOption = x * norm.cdf(d1) - K * math.exp( -r * (T - t) ) * norm.cdf(d2)
  return PriceOfCallOption, PriceOfPutOption

def HistVolt(bseORnse, TP):
  sList = []
  FN = ''
  if bseORnse == 'BSE':
    sList = ['RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'HINDUNILVR.BO', 'INFY.BO','KOTAKBANK.BO', 'ICICIBANK.BO', 'LT.BO', 'AXISBANK.BO', 'SBIN.BO','GOOGL', 'AAPL', 'AMZN', 'MSFT', 'NVDA', 'ADBE', 'NFLX', 'TSLA', 'ORCL', 'CSCO','Sensex']
    FN = 'bsedata1.csv'
  elif bseORnse == 'NSE':
    sList = ['RELIANCE.NS', 'TCS.NS', 'HINDUNILVR.NS', 'INFY.NS','KOTAKBANK.NS', 'ICICIBANK.NS', 'LT.NS', 'SBIN.NS', 'ITC.NS', 'ONGC.NS','NKE', 'BIDU', 'NVDA', 'KO', 'PYPL', 'SNAP', 'MCD', 'WMT', 'BABA', 'PEP','Nifty']
    FN = 'nsedata1.csv'
  df = pand.read_csv(FN)
  dfMon = df.groupby(pand.DatetimeIndex(df.Date).to_period('M')).nth(0)
  start_Index = 60 - TP
  dfRed = dfMon.iloc[start_Index :]
  dfRed.reset_index(inplace = True, drop = True) 
  Index_list = df.index[df['Date'] >= dfRed.iloc[0]['Date']].tolist()
  dfRed = df.iloc[Index_list[0] :]
  MyInfo = dfRed.set_index('Date')
  MyInfo = MyInfo.pct_change(fill_method=None)
  TabulationVar = []
  Volatil = []
  for sname in sList:
    returns = MyInfo[sname]
    x = returns.to_list()
    std = npy.nanstd(npy.array(x))
    Volatil.append(std * math.sqrt(252))
  for i in range(len(Volatil)):
    TabulationVar.append([i + 1, sList[i], Volatil[i]])
  return Volatil

def pComp(bseORnse):
  sList = []
  FN = ''
  if bseORnse == 'BSE':
    sList = ['RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'HINDUNILVR.BO', 'INFY.BO','KOTAKBANK.BO', 'ICICIBANK.BO', 'LT.BO', 'AXISBANK.BO', 'SBIN.BO','GOOGL', 'AAPL', 'AMZN', 'MSFT', 'NVDA', 'ADBE', 'NFLX', 'TSLA', 'ORCL', 'CSCO','Sensex']
    FN = 'bsedata1.csv'
  elif bseORnse == 'NSE':
    sList = ['RELIANCE.NS', 'TCS.NS', 'HINDUNILVR.NS', 'INFY.NS','KOTAKBANK.NS', 'ICICIBANK.NS', 'LT.NS', 'SBIN.NS', 'ITC.NS', 'ONGC.NS','NKE', 'BIDU', 'NVDA', 'KO', 'PYPL', 'SNAP', 'MCD', 'WMT', 'BABA', 'PEP','Nifty']
    FN = 'nsedata1.csv'
  df = pand.read_csv(FN)
  df['Date'] = pand.to_datetime(df['Date'])
  df = df.interpolate(method ='linear', limit_direction ='forward')
  r = 0.05
  t = 0
  T = 6/12
  sigma_list = []
  TP = range(1, 61)
  for delta_t in range(1, 61):
    sigma_list.append(HistVolt(bseORnse, delta_t))
    
  for Index1 in range(len(sList)):
    print(f"For the Stock: {sList[Index1]}")
    GraphPlotter.rcParams["figure.figsize"] = (20, 10)
    S0 = df.iloc[len(df) - 1][sList[Index1]]
    PricesOfCallOption, PricesOfPutOption = npy.zeros((21, 60)), npy.zeros((21, 60))
    histoVolat = []
    for Index2 in range(60):
      sigma = sigma_list[Index2][Index1]
      histoVolat.append(sigma)
      A = [round(0.1 * i, 2) for i in range(5, 16)]
      for Index3 in range(len(A)):
        K = A[Index3] * S0
        call, put = OptionPriceCalc(S0, t, T, K, r, sigma)
        PricesOfCallOption[Index3][Index2] = call
        PricesOfPutOption[Index3][Index2] = put
    
    for i in range(len(A)):
      ax = GraphPlotter.subplot(2, 3, (i % 6) + 1)
      GraphPlotter.plot(TP, PricesOfCallOption[i],color = 'r')
      GraphPlotter.ylabel("Price of European Call Option")
      GraphPlotter.suptitle(f"Prices of European Call Option for the stock: {sList[Index1]}")
      GraphPlotter.xlabel("Length of the time period (in months)")
      ax.set_title(f"with K = {A[i]}*S0")
      if i == 5:
        # GraphPlotter.savefig('./Figures/' + sList[Index1] + '_call1.jpg')
        GraphPlotter.show() 
    # GraphPlotter.savefig('./Figures/' + sList[Index1] + '_call2.jpg')
    GraphPlotter.show()
    for i in range(len(A)):
      ax = GraphPlotter.subplot(2, 3, (i % 6) + 1)
      GraphPlotter.plot(TP, PricesOfPutOption[i],color = 'r')
      GraphPlotter.ylabel("Price of European Put Option")
      GraphPlotter.suptitle(f"Prices of European Put Option for the stock {sList[Index1]}")
      GraphPlotter.xlabel("Length of the time period (in months)")
      ax.set_title(f"with K = {A[i]}*S0")
      if i == 5:
        # GraphPlotter.savefig('./Figures/' + sList[Index1] + '_put1.jpg')
        GraphPlotter.show()
    # GraphPlotter.savefig('./Figures/' + sList[Index1] + '_put2.jpg')
    GraphPlotter.show()
    GraphPlotter.plot(TP, histoVolat,color = 'r')
    GraphPlotter.ylabel("Volatility")
    GraphPlotter.title(f"Historical Volatility versus time period for the stock: {sList[Index1]}")
    GraphPlotter.xlabel("Length of the time period (in months)")
    # GraphPlotter.savefig('./Figures/' + sList[Index1] + '_volatility.jpg')
    GraphPlotter.show()

pComp('BSE')
pComp('NSE')