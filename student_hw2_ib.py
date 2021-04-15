from ib_insync import *
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
#import statsmodels
import statsmodels.api as sm
#from statsmodels.tsa.stattools import coint, adfuller
#from statsmodels import regression,stats
import math
import datetime
import statsmodels.formula.api as smf
from datetime import date, time, datetime, timedelta
#from xml.etree import ElementTree as ET
#from IPython.core.debugger import set_trace
import seaborn as sns
import random
from ta import add_all_ta_features
from ta.utils import dropna
from ta.trend import *
import json
from os import listdir, remove
import time

ib=IB()
ib.disconnect()
ib.connect('127.0.0.1',7497, clientId= 34)

def get_weight(x,y):
    x1 = sm.add_constant(x)
    model = sm.OLS(y,x1)
    results = model.fit()
    hedge_ratio = results.params[0]
    weight = float(hedge_ratio/(1+hedge_ratio))
    return weight

def get_everyday(startdate,enddate):
    start = str(startdate)
    end = str(enddate)
    startyear = int(start[0:4])
    startmonth = int(start[4:6])
    startday = int(start[6:8])
    endyear = int(end[0:4])
    endmonth = int(end[4:6])
    endday = int(end[6:8])
    everyday = []
    if startyear == endyear:
        for i in range(startmonth,endmonth+1):
            if i == 1 or i==3 or i==5 or i==7 or i==8 or i==10 or i==12:
                for j in range(1,32):
                    everyday.append(str(startyear*10000+i*100+j))
            if i == 2:
                for j in range(1,29):
                    everyday.append(str(startyear*10000+i*100+j))
            if i == 4 or i==6 or i==9 or i==11:
                for j in range(1,31):
                    everyday.append(str(startyear*10000+i*100+j))
    elif endyear-startyear == 1:
        for j in range(startmonth,13):
            if j == 1 or j==3 or j==5 or j==7 or j==8 or j==10 or j==12:
                for k in range(1,32):
                    everyday.append(str(startyear*10000+j*100+k))
            if j == 2:
                for k in range(1,29):
                    everyday.append(str(startyear*10000+j*100+k))
            if j == 4 or j==6 or j==9 or j==11:
                for k in range(1,31):
                    everyday.append(str(startyear*10000+j*100+k))
        for j in range(1,endmonth+1):
            if j == 1 or j==3 or j==5 or j==7 or j==8 or j==10 or j==12:
                for k in range(1,32):
                    everyday.append(str(startyear*10000+j*100+k))
            if j == 2:
                for k in range(1,29):
                    everyday.append(str(startyear*10000+j*100+k))
            if j == 4 or j==6 or j==9 or j==11:
                for k in range(1,31):
                    everyday.append(str(startyear*10000+j*100+k))
    elif endyear-startyear == 2:
        for j in range(startmonth,13):
            if j == 1 or j==3 or j==5 or j==7 or j==8 or j==10 or j==12:
                for k in range(1,32):
                    everyday.append(str(startyear*10000+j*100+k))
            if j == 2:
                for k in range(1,29):
                    everyday.append(str(startyear*10000+j*100+k))
            if j == 4 or j==6 or j==9 or j==11:
                for k in range(1,31):
                    everyday.append(str(startyear*10000+j*100+k))
        for j in range(1,13):
            if j == 1 or j==3 or j==5 or j==7 or j==8 or j==10 or j==12:
                for k in range(1,32):
                    everyday.append(str((startyear+1)*10000+j*100+k))
            if j == 2:
                for k in range(1,29):
                    everyday.append(str((startyear+1)*10000+j*100+k))
            if j == 4 or j==6 or j==9 or j==11:
                for k in range(1,31):
                    everyday.append(str((startyear+1)*10000+j*100+k))
        for j in range(1,endmonth+1):
            if j == 1 or j==3 or j==5 or j==7 or j==8 or j==10 or j==12:
                for k in range(1,32):
                    everyday.append(str(endyear*10000+j*100+k))
            if j == 2:
                for k in range(1,29):
                    everyday.append(str(endyear*10000+j*100+k))
            if j == 4 or j==6 or j==9 or j==11:
                for k in range(1,31):
                    everyday.append(str(endyear*10000+j*100+k))
    elif endyear-startyear == 2:
        for j in range(startmonth,13):
            if j == 1 or j==3 or j==5 or j==7 or j==8 or j==10 or j==12:
                for k in range(1,32):
                    everyday.append(str(startyear*10000+j*100+k))
            if j == 2:
                for k in range(1,29):
                    everyday.append(str(startyear*10000+j*100+k))
            if j == 4 or j==6 or j==9 or j==11:
                for k in range(1,31):
                    everyday.append(str(startyear*10000+j*100+k))
        for j in range(1,13):
            if j == 1 or j==3 or j==5 or j==7 or j==8 or j==10 or j==12:
                for k in range(1,32):
                    everyday.append(str((startyear+1)*10000+j*100+k))
            if j == 2:
                for k in range(1,29):
                    everyday.append(str((startyear+1)*10000+j*100+k))
            if j == 4 or j==6 or j==9 or j==11:
                for k in range(1,31):
                    everyday.append(str((startyear+1)*10000+j*100+k))
        for j in range(1,endmonth+1):
            if j == 1 or j==3 or j==5 or j==7 or j==8 or j==10 or j==12:
                for k in range(1,32):
                    everyday.append(str(endyear*10000+j*100+k))
            if j == 2:
                for k in range(1,29):
                    everyday.append(str(endyear*10000+j*100+k))
            if j == 4 or j==6 or j==9 or j==11:
                for k in range(1,31):
                    everyday.append(str(endyear*10000+j*100+k))
    return everyday

def get_data(contract, history, freq, side, endDate):
    bar = ib.reqHistoricalData(
        contract,
        endDateTime=endDate,
        durationStr=history,
        barSizeSetting=freq,
        whatToShow=side,
        useRTH=True,
        formatDate=1)
    # use util in ib-insync to convert bar data into pandas dataframe
    df = util.df(bar)
    # return df
    return df


def get_data_live(contract, history, freq, side, endDate=''):
    bar = ib.reqHistoricalData(
        contract,
        endDateTime=endDate,
        durationStr=history,
        barSizeSetting=freq,
        whatToShow=side,
        useRTH=True,
        formatDate=1)

    # use util in ib-insync to convert bar data into pandas dataframe
    df = util.df(bar)
    # return df
    return df

# define a function to get IB data. endDate is the last date of the historical data


#define two trading tickers
ticker1 = "IVV"
ticker2 = "DOW"
contract1 = Contract(symbol=ticker1, secType='STK', exchange='SMART', currency='USD')
contract2 = Contract(symbol=ticker2, secType='STK', exchange='SMART', currency='USD')
ib.qualifyContracts(contract1)
ib.qualifyContracts(contract2)
while True:
    # If the app finds a file named 'currency_pair.txt' in the current directory, enter this code block.
    if 'rolling_window.txt' in listdir():

        # Code goes here...
        file = open('rolling_window.txt', 'r')
        js = file.read()
        parameters = json.loads(js)
        file.close()
        remove('rolling_window.txt')
        #需要修改input参数的格式 读出来这几个参数
        startdate = parameters['startdate']
        enddate = parameters['enddate']
        history = parameters['lookback_period']
        ##新加
        AccountEquity = parameters['AccountEquity']

        print('187 done')
        #加上一行 ‘23：59：59’
        freq = '1 day'
        side = 'Trades'
        backtestdaylist = get_everyday(startdate,enddate)
        print(backtestdaylist)
        z_score = []
        hedge_ratio = []
        w1 = []
        print('195 done')
        i = 0
        position1 = 0
        position2 = 0
        order1 = 0
        order2 = 0
        neworder1 = []
        neworder2 = []
        orderprice1 = []
        orderprice2 = []
        AccountEquityList = []
        asset = 0
        assetlist = []
        position1list = []
        position2list = []
        for testday in backtestdaylist:
            i = i+1
            endDate = str(testday) + ' ' + '23:59:59'
            df1 = get_data(contract1, history, freq, side, endDate)
            df2 = get_data(contract2, history, freq, side, endDate)
            df1[ticker1 + '_log'] = df1['close'].apply(lambda x: math.log(x))
            df2[ticker2 + '_log'] = df2['close'].apply(lambda x: math.log(x))
            slope, intercept, r_value, p_value, std_err = stats.linregress(df2[ticker2 + '_log'], df1[ticker1 + '_log'])
            df1['W'] = df1[ticker1 + '_log'] - slope * df2[ticker2 + '_log']
            price1 = df1['close'].values
            price2 = df2['close'].values
            #zscore = (df1['W'].tail(1)-df1['W'].mean())/np.std(df1['W'])
            mu = df1['W'].mean()
            sigma = np.std(df1['W'])
            wlist = df1['W'].values
            w = wlist[-1]
            zscore = (w - mu) / sigma
            z_score.append(zscore)
            hedge_ratio.append(slope)
            w1.append(1 / (1 + slope))
            price_1 = price1[-1]
            price_2 = price2[-1]
            if i>2:
                z2 = z_score[-2]
                z1 = z_score[-1]
                if position1 == 0:
                    if abs(z2) < 1 and abs(z1) > 1:
                        weight = w1[-1]
                        order1 = int(AccountEquity * weight / price_1)
                        order2 = int(-1*AccountEquity * (1 - weight) / price_2)
                        neworder1.append(order1)
                        neworder2.append(order2)
                        orderprice1.append(price_1)
                        orderprice2.append(price_2)
                        position1 = order1 * price_1
                        position2 = order2 * price_2
                        AccountEquity = AccountEquity - position1 - position2
                        AccountEquityList.append(AccountEquity)
                        position1list.append(position1)
                        position2list.append(position2)
                    else:
                        neworder1.append(0)
                        neworder2.append(0)
                        AccountEquityList.append(AccountEquity)
                        position1list.append(0)
                        position2list.append(0)
                        orderprice1.append(0)
                        orderprice2.append(0)
                elif position1 != 0:
                    position1 = order1 * price_1
                    position2 = order2 * price_2
                    if abs(z2) > 0.6 and abs(z1) < 0.6:
                        AccountEquity = AccountEquity + position1 + position2
                        position1 = 0
                        position2 = 0
                        neworder1.append(-1 * order1)
                        neworder2.append(-1 * order2)
                        AccountEquityList.append(AccountEquity)
                        position1list.append(0)
                        position2list.append(0)
                        orderprice1.append(price_1)
                        orderprice2.append(price_2)
                    else:
                        neworder1.append(0)
                        neworder2.append(0)
                        AccountEquityList.append(AccountEquity)
                        position1list.append(position1)
                        position2list.append(position2)
                        orderprice1.append(0)
                        orderprice2.append(0)
                asset = position1 + position2 + AccountEquity
                assetlist.append(asset)
            print(i)
        hedge = pd.DataFrame({'Date':backtestdaylist,'hedge_ratio':hedge_ratio})
        hedge.to_csv('hedge_ratio.csv')
        z = pd.DataFrame({'Date': backtestdaylist, 'z_score': z_score})
        z.to_csv('z_score.csv')
        trade_blotter = pd.DataFrame(
            {'Date':backtestdaylist[2:],'IVV_Order': neworder1, 'IVV_Price': orderprice1, 'IVV_Position': position1list, 'DOW_Order': neworder2,
             'DOW_Price': orderprice2, 'DOW_Position': position2list, 'Account_Equity': AccountEquityList})
        trade_blotter['Asset'] = trade_blotter['IVV_Position']+trade_blotter['DOW_Position']+trade_blotter['Account_Equity']
        trade_blotter.to_csv('trade_blotter.csv')
        pass
    if 'live_trade.txt' in listdir():
        #同上，需要调整input的格式
        history = parameters['lookback_period']
        AcountEquity = parameters['AccountEquity']
        remove('live_trade.txt')
        time_now = time.strftime("%H%M", time.localtime())  # UTC+8 and I want this algo work every 10am EST
        if time_now == "23:01":

            ####live trading algo####
            #####       the reason that these things all put into the time function is that:
            #####    Everyday, the ticker's market data will get refreshed so that  we use
            #####    90-day rolling window for the live trading. This is an example of GS vs.MS.
            freq = '1 day'
            side = 'Trades'
            ticker1 = "IVV"
            ticker2 = "DOW"
            contract1 = Contract(symbol=ticker1, secType='STK', exchange='SMART', currency='USD')
            ib.qualifyContracts(contract1)
            contract2 = Contract(symbol=ticker2, secType='STK', exchange='SMART', currency='USD')
            ib.qualifyContracts(contract1)
            df1 = get_data_live(contract1, history, freq, side)
            df2 = get_data_live(contract2, history, freq, side)
            df1_log = np.log(df1['close'])
            df2_log = np.log(df2['close'])
            log_diff1 = list(df2_log - df1_log)
            mean1 = np.mean(log_diff1)
            std1 = np.std(log_diff1)
            weight1 = get_weight(df1_log, df2_log)
            if abs(log_diff1[-1]) >= 1 and abs(log_diff1[-2]) < 1:
                if ib.position == 0:
                    [ticker1] = ib.reqTickers(contract1)
                    contract_price1 = ticker1.marketPrice()
                    [ticker2] = ib.reqTickers(contract2)
                    contract_price2 = ticker2.marketPrice()
                    orders1 = int(AcountEquity * weight1 / contract_price1)
                    orders2 = int(AcountEquity * (1 - weight1) / contract_price2)
                    ib.placeOrders(contract1, orders1)
                    ib.placeOrders(contract2, -orders2)
            if abs(log_diff1[-1]) == mean1 and abs(log_diff1[-2]) > mean1:
                if ib.position != 0:
                    ib.placeOrders(contract1, -orders1)
                    ib.placeOrders(contract2, orders2)
                    [ticker1] = ib.reqTickers(contract1)
                    contract_price1 = ticker1.marketPrice()
                    [ticker2] = ib.reqTickers(contract2)
                    contract_price2 = ticker2.marketPrice()
                    AcountEquity = orders1 * contract_price1 + orders2 * contract_price2
            ####live trading algo####
            print(AcountEquity)
            time.sleep(61)
print("done")

