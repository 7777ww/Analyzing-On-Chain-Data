# Analyzing-On-Chain-Data
地址資料與價格資料用csv檔儲存。
Function包括兩個主要部分：數據檢索(RetrieveData.py)和數據計算分析(calulate.py)。首先從區塊鏈 API 獲取比特幣地址的交易數據，然後對這些數據進行分析和計算技術指標如 RSI、IRR 等。最後，將結果更新到目標數據表中。


RetrieveData.py

1. get_url(bitcoin_address, limit=5000)
功能: 構建用於請求比特幣地址交易數據的 API URL。
參數:
bitcoin_address: 比特幣地址。
limit: 請求的交易數量限制（默認為5000）。
返回: 構建的 API URL 字符串。
2. get_data(address)
功能: 根據比特幣地址請求並獲取交易數據。
參數:
address: 比特幣地址。
返回: 該地址的交易數據 DataFrame。如果交易數量超過5000，則提示並返回 None。
3. extract_address(address)
功能: 提取並返回比特幣地址交易數據中的所有唯一輸入地址。
參數:
address: 比特幣地址。
返回: 輸入地址列表。
4. check_and_added_address(address_list, target)
功能: 檢查輸入地址列表中的地址是否存在於目標 DataFrame 中，若不存在則添加。
參數:
address_list: 需要檢查的地址列表。
target: 目標 DataFrame。
返回: 更新後的目標 DataFrame。
5. read_data(count, target)
功能: 讀取目標 DataFrame 中指定行索引的交易數據 CSV 文件。
參數:
count: 計數，目標 DataFrame 中的行索引。
target: 目標 DataFrame，每一行記載每個地址的交易情況。
返回: 讀取的交易數據 DataFrame。如果文件不存在則返回 None。

calulate.py
1. rsi_index_V2(rsi, address, count, target)
功能: 分配 RSI 值給比特幣地址，並將交易結果分為買入和賣出兩類。
參數:
rsi: RSI 數據。
address: 比特幣地址數據。
count: 當前計數。
target: 目標 DataFrame。
返回: 分別包含 RSI 值的買入和賣出 DataFrame。
2. oversold_v2(rsi, address, count, target, column='', zone=30)
功能: 計算 RSI 低於指定閾值（超賣區域）的交易比例，並更新目標 DataFrame。
參數:
rsi: RSI 數據。
address: 比特幣地址數據。
count: 當前計數。
target: 目標 DataFrame。
column: 欲更新的列名稱。
zone: 超賣區域的 RSI 閾值（默認為 30）。
3. overbought_v2(rsi, address, count, target, column='', zone=70)
功能: 計算 RSI 高於指定閾值（超買區域）的交易比例，並更新目標 DataFrame。
參數:
rsi: RSI 數據。
address: 比特幣地址數據。
count: 當前計數。
target: 目標 DataFrame。
column: 欲更新的列名稱。
zone: 超買區域的 RSI 閾值（默認為 70）。
4. calculate_irr(address, current_price)
功能: 計算內部收益率（IRR）。
參數:
address: 比特幣地址數據。
current_price: 當前價格。
返回: IRR 值。
5. rsi_weight_average(rsi_buy)
功能: 計算 RSI 的加權平均值。
參數:
rsi_buy: RSI 買入數據。
返回: RSI 的加權平均值。
6. 計算加權RSI(rsi, address, count, target, period='')
功能: 計算並更新 RSI 的加權平均值。
參數:
rsi: RSI 數據。
address: 比特幣地址數據。
count: 當前計數。
target: 目標 DataFrame。
period: 期間標識。
返回: 分別包含 RSI 值的買入和賣出 DataFrame。
7. count_BandS(address, count, target)
功能: 計算買入和賣出的次數，並更新目標 DataFrame。
參數:
address: 比特幣地址數據。
count: 當前計數。
target: 目標 DataFrame。
返回: 買入和賣出的次數。
8. total_value(address, count, target)
功能: 計算買入和賣出的總值，並更新目標 DataFrame。
參數:
address: 比特幣地址數據。
count: 當前計數。
target: 目標 DataFrame。
返回: 買入和賣出的總值。
