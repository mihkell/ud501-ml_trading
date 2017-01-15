## http://quantsoftware.gatech.edu/MC1-Project-1-Test-Cases-spr2016

import pandas as pd
import math
import matplotlib.pyplot as plt

# print math.sqrt(252)*(0.001-0.0002) / 0.001
# Get Stocks.
import stocks

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
AAPL, GLD, GOOG, XOM, DAILY_RETURN, SPY, DATE = "AAPL", "GLD", "GOOG", "XOM", "DAILY_RETURN", "SPY", "Date"


def myFunction(allocations_list):
    s = stocks.stocks()
    s.get_data_to_csv("SPY")
    s.get_data_to_csv("GOOG")
    s.get_data_to_csv("AAPL")
    s.get_data_to_csv("GLD")
    s.get_data_to_csv("XOM")
    print('\033[94m My Function \033[0m')
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

    allocations = pd.DataFrame(allocations_list)
    allocations.columns = [1, 0]
    allocations = allocations.set_index(1)
    allocations_list = allocations.transpose()

    df = spy.join(apple, how='inner')
    df = df.join(google, how='inner')
    df = df.join(gold, how='inner')
    df = df.join(xom, how='inner')

    # headerPrint("First 3 values of dataframe")
    # print(df[:3])

    # headerPrint("Normalized values")
    df = df / df.ix[0, :].values
    # print(df[:3])

    headerPrint("Daily return")
    daily_return(allocations_list, df)
    print("wikis: " + str(0.000957366234238))
    print("       " + str(df[DAILY_RETURN].mean()))

    headerPrint("Cumulated return")
    cum_ret = cumulated_return(allocations_list, df)
    print("       " + str(cum_ret))

    headerPrint("Sharp Ratio")
    print("wikis: " + str(1.51819243641))
    print("       " + str(calc_sharp_ratio(allocations_list, df)))

    ax = df.plot(title="Portfolio")
    ax.set_ylabel("Normalized value")
    # plt.show()


def calc_sharp_ratio(allocations_list, df, new_daily=True):
    if df[0:1].sum().values[0] != len(allocations_list):
        df = df / df.ix[0, :].values
    if DAILY_RETURN not in df.columns or new_daily:
        daily_return(allocations_list, df)
    local_df = df[[AAPL, GLD, GOOG, XOM]]
    local_df = local_df * allocations_list.ix[0, :]
    local_df['TOTAL'] = local_df.sum(axis=1)
    sharp_ratio = math.sqrt(252) * df[DAILY_RETURN].mean() / df[DAILY_RETURN].std()
    return sharp_ratio


def daily_return(allocations_list, df):
    local_df = df[[AAPL, GLD, GOOG, XOM]]
    local_df = local_df * allocations_list.ix[0, :]
    local_df['TOTAL'] = local_df.sum(axis=1)
    df[DAILY_RETURN] = local_df['TOTAL'][1:] / local_df['TOTAL'].ix[:-1].values - 1
    df[DAILY_RETURN][0] = 0
    return df


def cumulated_return(allocations_list, df):
    columns_to_calculate_on = df[-1:]
    columns_to_calculate_on = columns_to_calculate_on.reset_index()
    columns_to_calculate_on = columns_to_calculate_on.drop('Date', axis=1)
    columns_to_calculate_on = columns_to_calculate_on.drop('SPY', 1)
    columns_to_calculate_on = columns_to_calculate_on.drop(DAILY_RETURN, 1)
    cumulative_return = columns_to_calculate_on * allocations_list
    cumulative_return = cumulative_return.sum(axis=1)
    print("wikis: " + str(0.255646784534))
    return cumulative_return.ix[0: 0:1].values[0] - 1


def headerPrint(string):
    print
    HEADER_COLOR = '\033[92m'
    END_COLOR = '\033[0m'
    print(HEADER_COLOR + string.upper() + END_COLOR)


if __name__ == "__main__":

    myFunction([('AAPL', 0.3), ('GLD', 0.4), ('GOOG', 0.2), ('XOM', 0.1)])

'''
d = {'one': pd.Series([11., 22., 33., 55], index=['a', 'b', 'c', 'd']),
     'two': pd.Series([14., 21., 32., 44.], index=['a', 'b', 'c', 'd'])}
df = pd.DataFrame(d)

d = {'one': pd.Series([0.8], index=['a', 'b', 'c', 'd']),
     'two': pd.Series([0.2], index=['a', 'b', 'c', 'd'])}

allocations = pd.DataFrame(d)

print('allocations:')
print(allocations)
normed = df / df.iloc[0]

print('normed:')
print(normed)

totals = normed * allocations
print("totals:")
print(totals)

print("Portfolio value:")
print(totals.sum(axis=1))
'''
