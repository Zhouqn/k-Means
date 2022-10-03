import numpy as np
import pandas as pd
import tushare as ts
import time
pro = ts.pro_api('e7ae68d91d7782f40c685b08102c25d3563c58aa48f3120336a3f537')


# 读取SSE上交所 SZSE深交所的股票数据
stock_data_sse = pd.read_csv('tushare_stock_basic_SSE.csv')
stock_data_szse = pd.read_csv('tushare_stock_basic_SZSE.csv')


# 开始时间和结束时间 （取30天的日线行情）
s_date = '20190102'
e_date = '20190219'


def get_stock_data(sse, szse):
    """
    :param sse: 上交所的股票信息600只
    :param szse: 深交所的股票信息600只
    :return: 1200只股票股票数据的前三列（ts_code,symbol,name）信息
    """
    stock_data = pd.concat([sse, szse])
    data = stock_data.iloc[:, :3]
    return data


def get_daily_data(ts_code):
    """
    :param ts_code: 股票的ts_code
    :return: 开始时间到结束时间内的股票日线行情（这里是30天）
    """
    df = pro.daily(**{
        "ts_code": ts_code,
        "trade_date": "",
        "start_date": s_date,
        "end_date": e_date,
        "offset": "",
        "limit": ""
    }, fields=[
        "ts_code",
        "trade_date",
        "open",
        "high",
        "low",
        "close",
        "pre_close",
        "change",
        "pct_chg",
        "vol",
        "amount"
    ])
    return df


def take_the_data():
    """
    :return: 返回过滤后的1000只股票数据 以及 这1000只股票的30天日线行情
    """
    count = 0
    stock_data = pd.DataFrame(columns=['ts_code', 'symbol', 'name'])
    daily_data = pd.DataFrame(columns=['ts_code', 'high', 'low', 'close'])
    s_data = get_stock_data(stock_data_szse, stock_data_sse)
    for index, row in s_data.iterrows():
        print(count)
        # 取1000只股票
        if count == 1000:
            break
        name = row['name']
        # 包含ST的股票数据跳过
        if 'ST' in name:
            continue
        ts_code = row['ts_code']
        # 获取股票的日线行情
        data_1 = get_daily_data(ts_code)
        # 防止数据太快
        time.sleep(0.1)
        # 不足30天的股票数据跳过
        if data_1.shape[0] != 30:
            continue
        # 保存下来要用到的股票信息
        stock_data = stock_data.append(row)
        # 排序 按照trade_date交易日期正向排序
        data_1.sort_values(by=['trade_date'], ignore_index=True, inplace=True)
        daily_data = daily_data.append(data_1)
        count = count + 1
    # 存储将要用到的1000只股票数据
    stock_data.to_csv('stock_data.csv', index=False)
    # 存储1000只股票的30天日线行情
    daily_data.to_csv('daily_data.csv', index=False)
    # return stock_data, daily_data


# take_the_data()
