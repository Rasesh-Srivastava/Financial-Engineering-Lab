import math
import pandas as pand
import matplotlib.pyplot as GraphPlotter
import numpy as npy
def indexMarketPortfolio():
    def SML_Graph(M, C, mu_rf, mu_market, risk_market):
        beta_k = npy.linspace(-1, 1, 2000)
        mu_k = mu_rf + (mu_market - mu_rf) * beta_k
        GraphPlotter.plot(beta_k, mu_k,color='r')
        print("Equation of Security Market Line is:")
        print("mu = {:.2f} beta + {:.2f}".format(mu_market - mu_rf, mu_rf))
        GraphPlotter.ylabel("Mean Return")
        GraphPlotter.title('Security Market Line for all the 10 assets')
        GraphPlotter.xlabel("Beta")
        GraphPlotter.grid(True)
        GraphPlotter.show()

    def WeightCalculator(M, C, mu):
        C_inverse = npy.linalg.inv(C)
        u = [1 for i in range(len(M))]
        p = [[1, u @ C_inverse @ npy.transpose(M)], [mu, M @ C_inverse @ npy.transpose(M)]]
        q = [[u @ C_inverse @ npy.transpose(u), 1], [M @ C_inverse @ npy.transpose(u), mu]]
        r = [[u @ C_inverse @ npy.transpose(u), u @ C_inverse @ npy.transpose(M)],
             [M @ C_inverse @ npy.transpose(u), M @ C_inverse @ npy.transpose(M)]]

        det_p, det_q, det_r = npy.linalg.det(p), npy.linalg.det(q), npy.linalg.det(r)
        det_p /= det_r
        det_q /= det_r
        w = det_p * (u @ C_inverse) + det_q * (M @ C_inverse)
        return w

    def FindTheEfficientFrontier(M, C, mu_rf):
        returns = npy.linspace(-2, 5, num=2000)
        u = npy.array([1 for i in range(len(M))])
        risk = []
        for mu in returns:
            w = WeightCalculator(M, C, mu)
            sigma = math.sqrt(w @ C @ npy.transpose(w))
            risk.append(sigma)

        weight_min_var = u @ npy.linalg.inv(C) / (u @ npy.linalg.inv(C) @ npy.transpose(u))
        mu_min_var = weight_min_var @ npy.transpose(M)
        risk_min_var = math.sqrt(weight_min_var @ C @ npy.transpose(weight_min_var))
        returns_plot1, risk_plot1, returns_plot2, risk_plot2 = [], [], [], []
        for i in range(len(returns)):
            if returns[i] >= mu_min_var:
                returns_plot1.append(returns[i])
                risk_plot1.append(risk[i])
            else:
                returns_plot2.append(returns[i])
                risk_plot2.append(risk[i])

        market_portfolio_weights = (M - mu_rf * u) @ npy.linalg.inv(C) / ((M - mu_rf * u) @ npy.linalg.inv(C) @ npy.transpose(u))
        mu_market = market_portfolio_weights @ npy.transpose(M)
        risk_market = math.sqrt(market_portfolio_weights @ C @ npy.transpose(market_portfolio_weights))
        GraphPlotter.plot(risk_plot1, returns_plot1, color='red', label='Efficient frontier')
        GraphPlotter.plot(risk_plot2, returns_plot2, color='green')
        GraphPlotter.xlabel("Risk (sigma)")
        GraphPlotter.ylabel("Returns")
        GraphPlotter.title("Minimum Variance Curve and Efficient Frontier")
        GraphPlotter.plot(risk_market, mu_market, color='blue', marker='o')
        GraphPlotter.annotate('Market Portfolio (' + str(round(risk_market, 4)) + ', ' + str(round(mu_market, 4)) + ')',
                     xy=(risk_market, mu_market), xytext=(0.012, 0.8))
        GraphPlotter.plot(risk_min_var, mu_min_var, color='blue', marker='o')
        GraphPlotter.annotate('Minimum Variance Portfolio (' + str(round(risk_min_var, 4)) + ', ' + str(round(mu_min_var, 4)) + ')',
                     xy=(risk_min_var, mu_min_var), xytext=(risk_min_var, -0.6))
        GraphPlotter.legend()
        GraphPlotter.grid(True)
        GraphPlotter.show()
        print("Market Portfolio Weights = ", market_portfolio_weights)
        print("Return = ", mu_market)
        print("Risk = ", risk_market * 100, " %")
        return mu_market, risk_market

    def CML_Graph(M, C, mu_rf, mu_market, risk_market):
        returns = npy.linspace(-2, 5, num=2000)
        u = npy.array([1 for i in range(len(M))])
        risk = []
        for mu in returns:
            w = WeightCalculator(M, C, mu)
            sigma = math.sqrt(w @ C @ npy.transpose(w))
            risk.append(sigma)
        returns_cml = []
        risk_cml = npy.linspace(0, 0.25, num=2000)
        for i in risk_cml:
            returns_cml.append(mu_rf + (mu_market - mu_rf) * i / risk_market)

        slope, intercept = (mu_market - mu_rf) / risk_market, mu_rf
        print("\nEquation of Capital Market Line is:")
        print("y = {:.4f} x + {:.4f}\n".format(slope, intercept))
        GraphPlotter.plot(risk_market, mu_market, color='green', marker='o')
        GraphPlotter.annotate('Market Portfolio (' + str(round(risk_market, 4)) + ', ' + str(round(mu_market, 4)) + ')', xy=(risk_market, mu_market), xytext=(0.012, 0.8))
        GraphPlotter.plot(risk, returns, label='Minimum Variance Line')
        GraphPlotter.plot(risk_cml, returns_cml, label='CML')
        GraphPlotter.ylabel("Returns")
        GraphPlotter.title("Capital Market Line with Minimum Variance Line")
        GraphPlotter.xlabel("Risk (sigma)")
        GraphPlotter.grid(True)
        GraphPlotter.legend()
        GraphPlotter.show()

        GraphPlotter.plot(risk_cml, returns_cml)
        GraphPlotter.ylabel("Returns")
        GraphPlotter.title("Capital Market Line")
        GraphPlotter.xlabel("Risk (sigma)")
        GraphPlotter.grid(True)
        GraphPlotter.show()
    
    def ComputeMarketPortfolio(filename):
        df = pand.read_csv(filename)
        df.set_index('Date', inplace=True)
        DailyReturns = (df['Open'] - df['Close']) / df['Open']
        DailyReturns = npy.array(DailyReturns)
        df = pand.DataFrame(npy.transpose(DailyReturns))
        M, sigma = npy.mean(df, axis=0) * len(df) / 5, df.std()
        mu_market = M[0]
        risk_market = sigma[0]
        print("Market return \t=", mu_market)
        print("Market risk \t=", risk_market * 100, "%")
        return mu_market, risk_market
    
    def RunAccordingToStockType(nameOfTheStock, type, mu_market_index, risk_market_index):
        DailyReturns = []
        for i in range(len(nameOfTheStock)):
            filename = './' + type + '/' + nameOfTheStock[i] + '.csv'
            df = pand.read_csv(filename)
            df.set_index('Date', inplace=True)
            df = df.pct_change()
            DailyReturns.append(df['Open'])

        DailyReturns = npy.array(DailyReturns)
        df = pand.DataFrame(npy.transpose(DailyReturns), columns=nameOfTheStock)
        M = npy.mean(df, axis=0) * len(df) / 5
        C = df.cov()
        mu_market, risk_market = FindTheEfficientFrontier(M, C, 0.05)
        CML_Graph(M, C, 0.05, mu_market, risk_market)
        if type == 'BSE' or type == 'NSE':
            SML_Graph(M, C, 0.05, mu_market_index, risk_market_index)
        else:
            SML_Graph(M, C, 0.05, mu_market, risk_market)

    print("Market portfolio for BSE using Index")
    mu_market_BSE, risk_market_BSE = ComputeMarketPortfolio('./BSE/Sensex.csv')
    print()
    print()
    print("Market portfolio for NSE using Index")
    mu_market_NSE, risk_market_NSE = ComputeMarketPortfolio('./NSE/Nifty.csv')
    print()
    print()
    print("10 stocks from the BSE Index")
    nameOfTheStock = ['RELIANCE_BO', 'TCS_BO', 'HDFCBANK_BO', 'HINDUNILVR_BO', 'INFY_BO','KOTAKBANK_BO', 'ICICIBANK_BO', 'LT_BO', 'AXISBANK_BO', 'SBIN_BO']
    RunAccordingToStockType(nameOfTheStock, 'BSE', mu_market_BSE, risk_market_BSE)
    print()
    print()
    print("10 stocks from the NSE Index")
    nameOfTheStock = ['RELIANCE_NS', 'TCS_NS', 'HINDUNILVR_NS', 'INFY_NS','KOTAKBANK_NS', 'ICICIBANK_NS', 'LT_NS', 'SBIN_NS', 'ITC_NS', 'ONGC_NS']
    RunAccordingToStockType(nameOfTheStock, 'NSE', mu_market_NSE, risk_market_NSE)
    print()
    print()
    print("10 stocks not from the BSE Index")
    nameOfTheStock = ['GOOGL', 'AAPL', 'AMZN', 'MSFT', 'NVDA', 'ADBE', 'NFLX', 'TSLA', 'ORCL', 'CSCO']
    RunAccordingToStockType(nameOfTheStock, 'Non_BSE', mu_market_NSE, risk_market_NSE)
    print()
    print()
    print("10 stocks not from the NSE Index")
    print()
    nameOfTheStock = ['NKE', 'BIDU', 'NVDA', 'KO', 'PYPL', 'SNAP', 'MCD', 'WMT', 'BABA', 'PEP']
    RunAccordingToStockType(nameOfTheStock, 'Non_NSE', mu_market_NSE, risk_market_NSE)

def capmANDsml():
    def FindBeta(nameOfTheStock, indexedFilename, BSEorNSE_index):
        df = pand.read_csv(indexedFilename)
        df.set_index('Date', inplace=True)
        DailyReturns = (df['Open'] - df['Close']) / df['Open']
        DailyReturns_stocks = []
        for i in range(len(nameOfTheStock)):
            if BSEorNSE_index == 'Non_BSE':
                filename = './Non_BSE/' + nameOfTheStock[i] + '.csv'
            elif BSEorNSE_index == 'Non_NSE':
                filename = './Non_NSE/' + nameOfTheStock[i] + '.csv'
            else:
                filename = './' + BSEorNSE_index[:3] + '/' + nameOfTheStock[i] + '.csv'
            df_stocks = pand.read_csv(filename)
            df_stocks.set_index('Date', inplace=True)
            DailyReturns_stocks.append((df_stocks['Open'] - df_stocks['Close']) / df_stocks['Open'])

        arrayBeta = []
        for i in range(len(nameOfTheStock)):
            df_combined = pand.concat([DailyReturns_stocks[i], DailyReturns], axis=1, keys=[nameOfTheStock[i], BSEorNSE_index])
            C = df_combined.cov()
            beta = C[BSEorNSE_index][nameOfTheStock[i]] / C[BSEorNSE_index][BSEorNSE_index]
            arrayBeta.append(beta)

        return arrayBeta

    def RunAccordingToStockType(nameOfTheStock, type, mu_market_index, risk_market_index, beta):
        DailyReturns = []
        mu_rf = 0.05
        for i in range(len(nameOfTheStock)):
            filename = './' + type + '/' + nameOfTheStock[i] + '.csv'
            df = pand.read_csv(filename)
            df.set_index('Date', inplace=True)
            df = df.pct_change()
            DailyReturns.append(df['Open'])

        DailyReturns = npy.array(DailyReturns)
        df = pand.DataFrame(npy.transpose(DailyReturns), columns=nameOfTheStock)
        M = npy.mean(df, axis=0) * len(df) / 5
        C = df.cov()
        print()
        print()
        print("Stock's Name\t\t\tActual Return\t\tExpected Return")
        print()
        for i in range(len(M)):
            print("{}\t\t\t{:.12f}\t\t{:.12f}".format(nameOfTheStock[i], M[i], beta[i] * (mu_market_index - mu_rf) + mu_rf))

    def ComputeMarketPortfolio(filename):
        df = pand.read_csv(filename)
        df.set_index('Date', inplace=True)
        DailyReturns = (df['Open'] - df['Close']) / df['Open']
        DailyReturns = npy.array(DailyReturns)
        df = pand.DataFrame(npy.transpose(DailyReturns))
        M, sigma = npy.mean(df, axis=0) * len(df) / 5, df.std()
        mu_market = M[0]
        risk_market = sigma[0]
        return mu_market, risk_market
    
    print("Inference about stocks taken from BSE")
    stocks_name_BSE = ['RELIANCE_BO', 'TCS_BO', 'HDFCBANK_BO', 'HINDUNILVR_BO', 'INFY_BO','KOTAKBANK_BO', 'ICICIBANK_BO', 'LT_BO', 'AXISBANK_BO', 'SBIN_BO']
    beta_BSE = FindBeta(stocks_name_BSE, './BSE/Sensex.csv', 'BSE Index')
    mu_market_BSE, risk_market_BSE = ComputeMarketPortfolio('./BSE/Sensex.csv')
    RunAccordingToStockType(stocks_name_BSE, 'BSE', mu_market_BSE, risk_market_BSE, beta_BSE)
    print()
    print()
    print("Inference about stocks taken from NSE  ")
    stocks_name_NSE = ['RELIANCE_NS', 'TCS_NS', 'HINDUNILVR_NS', 'INFY_NS','KOTAKBANK_NS', 'ICICIBANK_NS', 'LT_NS', 'SBIN_NS', 'ITC_NS', 'ONGC_NS']
    beta_NSE = FindBeta(stocks_name_NSE, './NSE/Nifty.csv', 'NSE Index')
    mu_market_NSE, risk_market_NSE = ComputeMarketPortfolio('./NSE/Nifty.csv')
    RunAccordingToStockType(stocks_name_NSE, 'NSE', mu_market_NSE, risk_market_NSE, beta_NSE) 
    print()
    print()
    print("Inference about stocks not taken from BSE index with index taken from BSE values")
    stocks_name_non = ['GOOGL', 'AAPL', 'AMZN', 'MSFT', 'NVDA', 'ADBE', 'NFLX', 'TSLA', 'ORCL', 'CSCO']
    beta_non_index_BSE = FindBeta(stocks_name_non, './BSE/Sensex.csv', 'Non_BSE')
    RunAccordingToStockType(stocks_name_non, 'Non_BSE', mu_market_BSE, risk_market_BSE, beta_non_index_BSE) 
    print()
    print()
    print("Inference about stocks not taken from NSE index with index taken from NSE values")
    stocks_name_non_nse = ['NKE', 'BIDU', 'NVDA', 'KO', 'PYPL', 'SNAP', 'MCD', 'WMT', 'BABA', 'PEP']
    beta_non_index_NSE = FindBeta(stocks_name_non_nse, './NSE/Nifty.csv', 'Non_NSE')
    RunAccordingToStockType(stocks_name_non_nse, 'Non_NSE', mu_market_NSE, risk_market_NSE, beta_non_index_NSE) 


def FindBeta(nameOfTheStock, indexedFilename, BSEorNSE_index):
  df = pand.read_csv(indexedFilename)
  df.set_index('Date', inplace=True)
  DailyReturns = (df['Open'] - df['Close'])/df['Open']
  DailyReturns_stocks = []
  for i in range(len(nameOfTheStock)):
    if BSEorNSE_index == 'Non_BSE':
      filename = './Non_BSE/' + nameOfTheStock[i] + '.csv'
    elif BSEorNSE_index == 'Non_NSE':
      filename = './Non_NSE/' + nameOfTheStock[i] + '.csv'
    else:
      filename = './' + BSEorNSE_index[:3] + '/' + nameOfTheStock[i] + '.csv'
    df_stocks = pand.read_csv(filename)
    df_stocks.set_index('Date', inplace=True)
    DailyReturns_stocks.append((df_stocks['Open'] - df_stocks['Close'])/df_stocks['Open'])

  arrayBeta = []
  for i in range(len(nameOfTheStock)):
    df_combined = pand.concat([DailyReturns_stocks[i], DailyReturns], axis = 1, keys = [nameOfTheStock[i], BSEorNSE_index])
    C = df_combined.cov()
    beta = C[BSEorNSE_index][nameOfTheStock[i]]/C[BSEorNSE_index][BSEorNSE_index]
    arrayBeta.append(beta)

  return arrayBeta


indexMarketPortfolio()
print()
capmANDsml()
print()
print("Beta for securities in BSE")
stocks_name_BSE = ['RELIANCE_BO', 'TCS_BO', 'HDFCBANK_BO', 'HINDUNILVR_BO', 'INFY_BO','KOTAKBANK_BO', 'ICICIBANK_BO', 'LT_BO', 'AXISBANK_BO', 'SBIN_BO']
beta_BSE = FindBeta(stocks_name_BSE, './BSE/Sensex.csv', 'BSE Index')
for i in range(len(beta_BSE)):
    print("{}\t\t=\t\t{}".format(stocks_name_BSE[i], beta_BSE[i]))

print()
print()
print("Beta for securities in NSE")
stocks_name_NSE = ['RELIANCE_NS', 'TCS_NS', 'HINDUNILVR_NS', 'INFY_NS','KOTAKBANK_NS', 'ICICIBANK_NS', 'LT_NS', 'SBIN_NS', 'ITC_NS', 'ONGC_NS']
beta_NSE = FindBeta(stocks_name_NSE, './NSE/Nifty.csv', 'NSE Index')
for i in range(len(beta_NSE)):
    print("{}\t\t=\t\t{}".format(stocks_name_NSE[i], beta_NSE[i]))

print()
print()
print("Beta for securities not in BSE using BSE Index")
stocks_name_non = ['GOOGL', 'AAPL', 'AMZN', 'MSFT', 'NVDA', 'ADBE', 'NFLX', 'TSLA', 'ORCL', 'CSCO']
beta_non_BSE = FindBeta(stocks_name_non, './BSE/Sensex.csv', 'Non_BSE')
for i in range(len(beta_non_BSE)):
    print("{}\t\t=\t\t{}".format(stocks_name_non[i], beta_non_BSE[i]))

print()
print()
print("Beta for securities not in NSE using NSE Index")
stocks_name_non = ['NKE', 'BIDU', 'NVDA', 'KO', 'PYPL', 'SNAP', 'MCD', 'WMT', 'BABA', 'PEP']
beta_non_NSE = FindBeta(stocks_name_non, './NSE/Nifty.csv', 'Non_NSE')
for i in range(len(beta_non_NSE)):
    print("{}\t\t=\t\t{}".format(stocks_name_non[i], beta_non_NSE[i]))