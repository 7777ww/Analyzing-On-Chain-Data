import requests as rq
import json
import pandas as pd
from pandas import DataFrame as df
import datetime
import numpy as np
import finlab_crypto
import talib
import numpy_financial as npf
ohlcv=pd.read_csv("history/BTCUSDT-4h-data.csv",index_col=0)

def rsi_index_V2(rsi,address,count,target):
    """
    asign rsi值給address
    """
        #4H
    try:

        rsi_sell=pd.DataFrame(columns=['rsi', 'time','value'])
        rsi_buy=pd.DataFrame(columns=['rsi', 'time','value'])
        
        for i in range(len(address)):
            if address.result[i]<0:
                #代表賣出

                x=address.time[i]
                x=int(x)
                x=np.datetime64(x-x%14400,'s')
                
                rsi_sell.loc[i]={'rsi':rsi.loc[str(x)],'time':x,'value':address.result[i]}
                

            elif address.result[i]>0:
                x=address.time[i]
                x=int(x)
                x=np.datetime64(x-x%14400,'s')
                rsi_buy.loc[i]={'rsi':rsi.loc[str(x)],'time':x,'value':address.result[i]}
                
        return rsi_buy,rsi_sell
    except Exception as e:
        print(f'發生異常：{e}')
        # print('index不符')       


def oversold_v2(rsi, address, count, target, column='', zone=30):
    """
    計算超賣區域比例並更新目標 DataFrame

    rsi: RSI 數據
    address: 地址數據
    count: 當前計數
    target: 目標 DataFrame
    column: 欲更新的列名稱
    zone: 超賣區域的 RSI 閾值
    """
    buy, _ = rsi_index_V2(rsi, address, count, target)
    
    # 計算 RSI 小於 zone 的區域比例
    oversold_zone_ratio = buy.loc[buy.rsi < zone].value.sum() / buy.value.sum()
    
    try:
        # 檢查目標 DataFrame 中是否存在指定列，並更新
        if column in target.columns:
            target.loc[count, column] = oversold_zone_ratio
            return
        else:
            print('找不到 column')
    except KeyError as e:
        print(f'列 {e} 不存在，无法赋值')

def overbought_v2(rsi, address, count, target, column='', zone=70):
    """
    計算超買區域比例並更新目標 DataFrame

    rsi: RSI 數據
    address: 地址數據
    count: 當前計數
    target: 目標 DataFrame
    column: 欲更新的列名稱
    zone: 超買區域的 RSI 閾值
    """
    _, sell = rsi_index_V2(rsi, address, count, target)
    
    # 計算 RSI 大於 zone 的區域比例
    overbought_zone_ratio = sell.loc[sell.rsi > zone].value.sum() / sell.value.sum()
    
    try:
        # 檢查目標 DataFrame 中是否存在指定列，並更新
        if column in target.columns:
            target.loc[count, column] = overbought_zone_ratio
            return
        else:
            print('找不到 column')
    except KeyError as e:
        print(f'列 {e} 不存在，无法赋值')
    
    return overbought_zone_ratio, column
def buy_zone(rsi, address, count, target, column='', zone=80):
    """
    計算買入區域比例並更新目標 DataFrame

    rsi: RSI 數據
    address: 地址數據
    count: 當前計數
    target: 目標 DataFrame
    column: 欲更新的列名稱
    zone: 買入區域的 RSI 閾值
    """
    buy, _ = rsi_index_V2(rsi, address, count, target)
    
    # 計算 RSI 大於 zone 的區域比例
    buy_zone_ratio = buy.loc[buy.rsi > zone].value.sum() / buy.value.sum()
    
    try:
        # 檢查目標 DataFrame 中是否存在指定列，並更新
        if column in target.columns:
            target.loc[count, column] = buy_zone_ratio
            return
        else:
            print('找不到 column')
    except KeyError as e:
        print(f'列 {e} 不存在，无法赋值')

def sell_zone(rsi, address, count, target, column='', zone=30):
    """
    計算賣出區域比例並更新目標 DataFrame

    rsi: RSI 數據
    address: 地址數據
    count: 當前計數
    target: 目標 DataFrame
    column: 欲更新的列名稱
    zone: 賣出區域的 RSI 閾值
    """
    _, sell = rsi_index_V2(rsi, address, count, target)
    
    # 計算 RSI 小於 zone 的區域比例
    sell_zone_ratio = sell.loc[sell.rsi < zone].value.sum() / sell.value.sum()
    
    try:
        # 檢查目標 DataFrame 中是否存在指定列，並更新
        if column in target.columns:
            target.loc[count, column] = sell_zone_ratio
            return
        else:
            print('找不到 column')
    except KeyError as e:
        print(f'列 {e} 不存在，无法赋值')


def IRR(x ,current_price=ohlcv.open[-1]):
    """
    計算內部報酬率 (IRR)

    x: 交易數據
    current_price: 當前價格，默認為最新的開盤價
    """
    amount = []
    price = []

    open = ohlcv.open
    amount.extend(x.result)
    price.extend(x.time)
    
    for i in range(len(price)):
        price[i] = price[i] - (price[i] % 60)
        price[i] = open.loc[str(np.datetime64(price[i], 's'))]
    
    # 計算未實現損益
    un = x.loc[x.result > 0].result.sum() + x.loc[x.result < 0].result.sum()
    un = un * current_price
    amount = [p * -a for p, a in zip(price, amount)]
    amount.append(un)
    
    import numpy_financial as npf

    # 計算 IRR
    irr = npf.irr(amount)
    print(f'Internal Rate of Return (IRR): {irr:.2%}')
    return irr

def rsi_weight_average(rsi_buy):
    numerator=sum(rsi_buy['rsi']*rsi_buy['value'])
    denominator=sum(rsi_buy['value'])
    return numerator/denominator

def 計算加權RSI(rsi,address,count,target,period=''):
    #4H
    try:
        buy_column_name=f'buy_rsi{period}'
        sell_column_name=f'sell_rsi{period}'
        print(buy_column_name,sell_column_name)

        rsi_buy,rsi_sell=rsi_index_V2(rsi,address,count,target)
        
        B,S=rsi_weight_average(rsi_buy),rsi_weight_average(rsi_sell)
        try:
            if buy_column_name in target.columns and sell_column_name in target.columns:

                target.loc[count,buy_column_name],target.loc[count,sell_column_name]=B,S

                print(f'加權平均買進：{B}\n加權平均賣出：{S}')
                return rsi_buy,rsi_sell
            else:
                print('找不到column')
        except KeyError as e:
            print(f'列 {e} 不存在，无法赋值')
    except Exception as e:
        print(f'发生异常：{e}')
        # print('index不符')

def count_BandS(address,count,target):
    B=(address['result']>0).sum()
    S=(address['result']<0).sum()
    target.loc[count, 'buying_time'] = B
    target.loc[count, 'selling_time'] = S
    print(target.buying_time[count],target.selling_time[count])
    return B,S


def total_value(address,count,target):
    buy_total=address.loc[address.result>0].result.sum()
    sell_total=address.loc[address.result<0].result.sum()
    target.loc[count, 'buy_value'],target.loc[count, 'sell_value']=buy_total,sell_total
    return buy_total, sell_total