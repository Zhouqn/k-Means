import numpy as np
import pandas as pd
# import data

# n = 9
stock_num = 1000  # 1000条股票数据
day_num = 6  # 计算x天的kdj值

# data.take_the_data()


def get_rsv(data_30):
    """
    获取rsv值
    :return: 返回计算出来的rsv值
    """
    rsv_arr = []
    for i in range(day_num):
        rows = data_30[i:i+9]
        # print(rows)
        high = max(rows['high'])
        low = min(rows['low'])
        last_row = rows[-1:]
        close = np.array(last_row['close'])[0]
        cal = ((close - low) / (high - low)) * 100
        rsv_arr.append(cal)
    return rsv_arr


def get_value(arr):
    res = []
    val = 50
    for i in range(day_num):
        if i > 0:
            val = res[i-1]
        cal = (2 / 3) * val + (1 / 3) * arr[i]
        res.append(cal)
    return res


def get_j(k_arr, d_arr):
    j_arr = []
    for i in range(day_num):
        cal = 3 * k_arr[i] - 2 * d_arr[i]
        j_arr.append(cal)
    return j_arr


# 计算KDJ指标
def calculate(daily_data_file):
    daily_data = pd.read_csv(daily_data_file)
    kdj = []
    for i in range(stock_num):
        n = i*30
        # 每次拿出一只股票的30天数据
        data_30 = daily_data[n: n+30]
        # 用30天的数据计算股票最后一天的RSV以及KDJ值
        rsv_arr = get_rsv(data_30)
        k_arr = get_value(rsv_arr)
        d_arr = get_value(k_arr)
        j_arr = get_j(k_arr, d_arr)
        index = day_num-1
        # 30天计算出19天的kdj指标，取出最后一天的kdj指标
        kdj.append([k_arr[index], d_arr[index], j_arr[index]])
    return kdj


def creat_kdj_data(stock_data_file, daily_data_file):
    kdj_data = pd.DataFrame(calculate(daily_data_file), columns=['k', 'd', 'j'])
    # 拼接股票数据和kdj指标
    stock_data = pd.read_csv(stock_data_file)
    stock_kdj = pd.concat([stock_data, kdj_data], axis=1)
    stock_kdj.to_csv('stock_kdj.csv', index=False)
    return stock_kdj


# creat_kdj_data()
