import os
import yfinance as yf
import pandas as pand

folders = ['BSE','Non_BSE','NSE', 'Non_NSE']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

stocksInBSEindex = ['RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'HINDUNILVR.BO', 'INFY.BO','KOTAKBANK.BO', 'ICICIBANK.BO', 'LT.BO', 'AXISBANK.BO', 'SBIN.BO']
stocksNotInBSEindex = ['GOOGL', 'AAPL', 'AMZN', 'MSFT', 'NVDA', 'ADBE', 'NFLX', 'TSLA', 'ORCL', 'CSCO']
stocksInNSEindex = ['RELIANCE.NS', 'TCS.NS', 'HINDUNILVR.NS', 'INFY.NS','KOTAKBANK.NS', 'ICICIBANK.NS', 'LT.NS', 'SBIN.NS', 'ITC.NS', 'ONGC.NS']
stocksNotInNSEindex = ['NKE', 'BIDU', 'NVDA', 'KO', 'PYPL', 'SNAP', 'MCD', 'WMT', 'BABA', 'PEP']

StartDate = '2019-01-01'
EndDate = '2023-12-31'

def ObtainStockPrices():
    def SaveDataInFile(ticker, folder):
        stock_data = yf.download(ticker, StartDate, EndDate)
        stock_data.reset_index(inplace=True)
        stock_data.to_csv(f'{folder}/{ticker.replace(".", "_")}.csv', index=False)

    for stock in stocksInBSEindex:
        SaveDataInFile(stock,'BSE')

    for stock in stocksNotInBSEindex:
        SaveDataInFile(stock,'Non_BSE')

    for stock in stocksInNSEindex:
        SaveDataInFile(stock, 'NSE')

    for stock in stocksNotInNSEindex:
        SaveDataInFile(stock, 'Non_NSE')

nse_data = yf.download('^NSEI', StartDate, EndDate)
nse_data.reset_index('Date',inplace=True)
nse_data.to_csv('NSE/Nifty.csv', index=False)
bse_data = yf.download('^BSESN', StartDate, EndDate)
bse_data.reset_index('Date',inplace=True)
bse_data.to_csv('BSE/Sensex.csv', index=False)

def FetchDataFromWeb(bse_or_nse,bse_data,nse_data,stocksInBSEindex,stocksNotInBSEindex,stocksInNSEindex,stocksNotInNSEindex):
    if bse_or_nse == 'BSE':
        df = pand.DataFrame({'Date': bse_data['Date']})
        for stock in stocksInBSEindex:
            stock_data = pand.read_csv(f'BSE/{stock.replace(".", "_")}.csv')
            df[stock.replace(".", "_")] = stock_data['Open'].pct_change()

        for stock in stocksNotInBSEindex:
            stock_data = pand.read_csv(f'Non_BSE/{stock.replace(".","_")}.csv')
            df[stock.replace(".","_")] = stock_data['Open'].pct_change()

        bse_data = pand.read_csv('BSE/Sensex.csv')
        df['Sensex'] = nse_data['Open'].pct_change()
        df.to_csv('bsedata1.csv', index=False)
    else:
        df = pand.DataFrame({'Date': nse_data['Date']})
        for stock in stocksInNSEindex:
            stock_data = pand.read_csv(f'NSE/{stock.replace(".", "_")}.csv')
            df[stock.replace(".", "_")] = stock_data['Open'].pct_change()

        for stock in stocksNotInNSEindex:
            stock_data = pand.read_csv(f'Non_NSE/{stock.replace(".", "_")}.csv')
            df[stock.replace(".", "_")] = stock_data['Open'].pct_change()

        nse_data = pand.read_csv('NSE/Nifty.csv')
        df['Nifty'] = nse_data['Open'].pct_change()
        df.to_csv('nsedata1.csv', index=False)

ObtainStockPrices()
FetchDataFromWeb("BSE",bse_data,nse_data,stocksInBSEindex,stocksNotInBSEindex,stocksInNSEindex,stocksNotInNSEindex)
FetchDataFromWeb("NSE",bse_data,nse_data,stocksInBSEindex,stocksNotInBSEindex,stocksInNSEindex,stocksNotInNSEindex)