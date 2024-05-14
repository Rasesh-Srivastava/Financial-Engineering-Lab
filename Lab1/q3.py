import math
sigma = 0.4
GivenTimeStamps = [0, 0.50, 1, 1.50, 3, 4.5]
S = 100
T = 5
r = 0.05
K = 105
def CheckTheArbitrageConditions(u, d, r, t):
  if d < math.exp(r*t) and math.exp(r*t) < u:
    return False
  else:
    return True
def TimeStampChecker(t):
  for i in GivenTimeStamps:
    if t * 0.25 == i:
      return True
  return False
PricesOfTheCallOption = []
PricesOfThePutOption = []
M = 20
t = T/M
d = math.exp(-sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)
NetInterestRate = math.exp(r*t) # R
u = math.exp(sigma*math.sqrt(t) + (r - 0.5*sigma*sigma)*t)
p = (NetInterestRate - d)/(u - d)
IsArbitrage = CheckTheArbitrageConditions(u, d, r, t)
if IsArbitrage:
    print(f"Arbitrage Opportunity exists for M = {M}")
    PricesOfThePutOption.append(-1)
    PricesOfTheCallOption.append(-1)
else:
    print(f"No arbitrage exists for M = {M}")
C = [[0 for i in range(M + 1)] for j in range(M + 1)]
P = [[0 for i in range(M + 1)] for j in range(M + 1)]
for i in range(0, M + 1):
    C[M][i] = max(0, S*math.pow(u, M - i)*math.pow(d, i) - K)
    P[M][i] = max(0, K - S*math.pow(u, M - i)*math.pow(d, i))
for j in range(M - 1, -1, -1):
    for i in range(0, j + 1):
        C[j][i] = (p*C[j + 1][i] + (1 - p)*C[j + 1][i + 1]) / NetInterestRate
        P[j][i] = (p*P[j + 1][i] + (1 - p)*P[j + 1][i + 1]) / NetInterestRate
for i in range(0, M + 1, 2):
    if TimeStampChecker(i):
        IntermediatePriceOfCallOption = []
        IntermediatePriceOfPutOption = []
        for j in range(0, i + 1):
            IntermediatePriceOfCallOption.append(C[i][j])
            IntermediatePriceOfPutOption.append(P[i][j])
        PricesOfTheCallOption.append(IntermediatePriceOfCallOption)
        PricesOfThePutOption.append(IntermediatePriceOfPutOption)
for IndexingVariable in range(0, len(GivenTimeStamps)):
  print(f"t = {GivenTimeStamps[IndexingVariable]}")
  print("Call Option\tPut Option")
  for j in range(len(PricesOfTheCallOption[IndexingVariable])):
    print(f"{PricesOfTheCallOption[IndexingVariable][j]:.2f}\t\t{PricesOfThePutOption[IndexingVariable][j]:.2f}")
  print()