import requests as rq
import json
import pandas as pd
from pandas import DataFrame as df

def get_url(bitcoin_address, limit=5000):
    """
    獲取比特幣地址的 API URL

    bitcoin_address: 比特幣地址
    limit: 請求的交易數量限制
    """
    base_url = "https://blockchain.info/rawaddr/"
    transactions = []
    offset = 0
    api_url = f"{base_url}{bitcoin_address}?limit={limit}&offset={offset}"
    return api_url

def get_data(address):
    """
    根據比特幣地址獲取數據

    address: 比特幣地址
    """
    timeout = 150
    try:
        # 獲取 URL
        x = get_url(address, limit=5000)
        print(x)
        # 進行 HTTP 請求
        x = rq.get(x, timeout=timeout)
        try:
            # 解析 JSON 數據
            x = json.loads(x.content)
            if x['n_tx'] < 5000:
                x = df(x['txs'])
                return x
            else:
                print('超過5000筆')
        except:
            print(x.content)
    except rq.exceptions.Timeout:
        print(f'請求超時，等待時間超過 {timeout} 秒')

def extract_address(address):
    """
    提取比特幣地址中的輸入地址列表

    address: 比特幣地址
    """
    # 獲取比特幣地址數據
    x = get_data(address)
    address_list = []

    # 提取輸入地址並添加到列表中
    for i in range(len(x)):
        y = x['inputs'][i][0]['prev_out']['addr']
        if y not in address_list:
            address_list.append(y)
    
    return address_list

def check_and_added_address(address_list, target):
    """
    檢查並添加新地址到目標 DataFrame

    address_list: 需要檢查的地址列表
    target: 目標 DataFrame
    """
    for address in address_list:
        # 檢查地址是否已存在於目標 DataFrame 中
        if address not in target['address'].values:
            df_addr = pd.DataFrame({'address': [address]})
            target = pd.concat([target, df_addr], ignore_index=True)
            print('加入成功')
        else:
            print('重複')
    
    return target

def read_data(count, target):

    """
    count: 計數，目標 DataFrame 中的行索引
    target: pd.DataFrame每一row記載每個地址的交易情況
    
    """
    try:
        if target.download[count]:
            path = f'data/{target.address[count]}.csv'
            x = pd.read_csv(path, index_col=0)
            return x
        else:
            return None
    except FileNotFoundError:
        print(f"文件不存在: {path}")
        return None
