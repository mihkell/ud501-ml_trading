import mc1p1.stocks as stocks
from mc1p1.mc1project1 import calc_sharp_ratio, myFunction, headerPrint
from scipy.optimize import minimize
import pandas as pd
import numpy as np


# s = stocks.stocks()
# s.get_data_to_csv("SPY")
# s.get_data_to_csv("GOOG")
# s.get_data_to_csv("AAPL")
# s.get_data_to_csv("GLD")
# s.get_data_to_csv("XOM")
#
spy = pd.read_csv("data/SPY.csv", index_col='Date', usecols=['Date', 'Adj Close']).rename(
    columns={'Adj Close': 'SPY'})
apple = pd.read_csv("data/AAPL.csv", index_col='Date', usecols=['Date', 'Adj Close']).rename(
    columns={'Adj Close': 'AAPL'})
google = pd.read_csv("data/GOOG.csv", index_col='Date', usecols=['Date', 'Adj Close']).rename(
    columns={'Adj Close': 'GOOG'})
gold = pd.read_csv("data/GLD.csv", index_col='Date', usecols=['Date', 'Adj Close']).rename(
    columns={'Adj Close': 'GLD'})
xom = pd.read_csv("data/XOM.csv", index_col='Date', usecols=['Date', 'Adj Close']).rename(
    columns={'Adj Close': 'XOM'})

df = spy.join(apple, how='inner')
df = df.join(google, how='inner')
df = df.join(gold, how='inner')
df = df.join(xom, how='inner')

def optimize():
    print('\033[94m Optimize \033[0m')
    constraints = ({'type': 'eq', 'fun': lambda inputs: 1 - np.sum(inputs)})
    return minimize(calc_sharp_wrapper,
                    np.array([0.3, 0.4, 0.2, 0.3]),
                    bounds=((0., 1.), (0., 1.), (0., 1.), (0., 1.)),
                    method='SLSQP',
                    constraints=constraints)


def calc_sharp_wrapper(values):
    allocations_list = get_allocation_list(values)

    allocations = pd.DataFrame(allocations_list)
    allocations.columns = [1, 0]
    allocations = allocations.set_index(1)
    allocations_list = allocations.transpose()

    sharp = calc_sharp_ratio(allocations_list=allocations_list, df=df, new_daily=True) * -1
    return sharp

def get_allocation_list(values):
    return [('AAPL', values[0]), ('GLD', values[1]), ('GOOG', values[2]), ('XOM', values[3])]

if __name__ == "__main__":
    ret = optimize()
    headerPrint("Opimization result")
    print(ret)
    myFunction(get_allocation_list(ret.x))
