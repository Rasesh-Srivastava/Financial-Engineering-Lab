import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
import random
from datetime import datetime
i=0
def f(filename, option_type,i):
  plt.rcParams["figure.figsize"] = (13, 4)
  df = pd.read_csv(filename)
  x, call, put = [], [], []
  for index, row in df.iterrows():
    num = random.random()
    if num <= 0.25:
      x.append(row['Strike Price'])
      call.append(row['Call Price'])
      put.append(row['Put Price'])
  plt.subplot(1, 2, 1)
  plt.scatter(x, call, marker = '.')
  plt.xlabel('Strike price')
  plt.ylabel('Call Price')
  plt.title(f'Call vs Strike Price for ({option_type})')
  plt.subplot(1, 2, 2)
  plt.scatter(x, put, marker = '.')
  plt.xlabel('Strike price')
  plt.ylabel('Put Price')
  plt.title(f'Put vs Strike Price for ({option_type})')
  # plt.savefig(f'./q2/{i}.png')
  i+=1
  # plt.close()
  plt.show()
  x, call, put = [], [], []
  random.seed(53)
  for index, row in df.iterrows():
    num = random.random()
    # print(row)
    if num <= 0.05:
      d1 = datetime.strptime(row['Expiry'],  '%d-%m-%Y')
      d2 = datetime.strptime(row['Date'],  '%d-%m-%Y')
      delta = d1 - d2
      x.append(delta.days)
      call.append(row['Call Price'])
      put.append(row['Put Price'])
  plt.subplot(1, 2, 1)
  plt.scatter(x, call, marker = '.')
  plt.xlabel('Maturity (in days)')
  plt.ylabel('Call Price')
  plt.title('Call vs Maturity  ({})'.format(option_type))
  plt.subplot(1, 2, 2)
  plt.scatter(x, put, marker = '.')
  plt.xlabel('Maturity')
  plt.ylabel('Put')
  plt.title('Put vs Maturity for ({})'.format(option_type))
  # plt.savefig(f'./q2/{i}.png')
  i+=1
  # plt.close()
  plt.show()
  mpl.rcParams.update(mpl.rcParamsDefault)
  strike, maturity, call, put = [], [], [], []
  for index, row in df.iterrows():
    num = random.random()
    if num <= 0.25:
      strike.append(row['Strike Price'])
      d1 = datetime.strptime(row['Expiry'],  '%d-%m-%Y')
      d2 = datetime.strptime(row['Date'],  '%d-%m-%Y')
      delta = d1 - d2
      maturity.append(delta.days)
      call.append(row['Call Price'])
      put.append(row['Put Price'])
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.scatter(strike, maturity, call, marker = '.')
  ax.set_xlabel('K')
  ax.set_ylabel('Maturity')
  ax.set_zlabel('Call')
  ax.set_title('3D call- {}'.format(option_type))
  # plt.savefig(f'./q2/{i}.png')
  i+=1
  # plt.close()
  plt.show()
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.scatter(strike, maturity, put, marker = '.')
  ax.set_xlabel('K')
  ax.set_ylabel('Maturity')
  ax.set_zlabel('Put')
  ax.set_title('3D PUT for {}'.format(option_type))
  # plt.savefig(f'./q2/{i}.png')
  i+=1
  # plt.close()
  plt.show()
  return i
files = ['NIFTYoptiondata', 'stockoptiondata_HEROMOTOCO', 'stockoptiondata_RELIANCE', 'stockoptiondata_TATA_MOTORS', 'stockoptiondata_HDFC', 'stockoptiondata_BAJAJ_AUTO']
option_type = ['NSE Index', 'HEROMOTOCO.NS', 'RELIANCE.NS', 'TATAMOTORS.NS', 'HDFCBANK.NS', 'BAJAJ-AUTO.NS']
for index in range(len(files)):
  files[index] = './' + files[index] + '.csv'
  i=f(files[index], option_type[index],i)
  # print(i)