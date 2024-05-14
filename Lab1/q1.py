import math
sigma = 0.4
ValuesOfMtobeTaken = [1, 5, 10, 20, 50, 100, 200, 400]
S = 100
T = 5
r = 0.05
K = 105
def CheckTheArbitrageConditions(u, d, r, t):
  if d < math.exp(r*t) and math.exp(r*t) < u:
    return False
  else:
    return True

PricesOfTheCallOption = []
PricesOfThePutOption = []
for M in ValuesOfMtobeTaken:
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
        continue
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
    PricesOfTheCallOption.append(C[0][0])
    PricesOfThePutOption.append(P[0][0])

print()
for IndexingVariable in range(0, len(ValuesOfMtobeTaken)):
    print(f"M = {ValuesOfMtobeTaken[IndexingVariable]}\t\tCall Option = {PricesOfTheCallOption[IndexingVariable]:.5f}\t\tPut Option = {PricesOfThePutOption[IndexingVariable]:.5f}")