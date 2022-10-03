import typing

import pandas as pd
import numpy as np
import kdj
from collections import defaultdict

_kdj_centroids_data = pd.read_csv('kdj_centroids_data.csv')
daily_data = pd.read_csv('daily_data.csv')
KDJ_DAY_NUM = 9  # kdj是固定使用前9天的数据计算当天的kdj值


def pre_stock(kdj_centroids_data, a, b):
    """
    预测涨跌
    :a : 代表买入信号的簇
    :b : 代表卖出信号的簇
    :return: 1000只股票预测涨跌数组
    """
    pre_arr = []
    for index, row in kdj_centroids_data.iterrows():
        centroids = row['簇']
        if centroids == b:
            pre_arr.append(-1)
        elif centroids == a:
            pre_arr.append(1)
        else:
            pre_arr.append(0)
    return pre_arr


def cal_rise_or_fall(pre_day_num):
    """
    实际涨跌
    :return: 1000只股票实际涨跌数组
    """
    res = []
    for i in range(0, 1000):
        n = i * 30
        kdj_start_index = n + KDJ_DAY_NUM + kdj.day_num - 2
        rows = daily_data[kdj_start_index:kdj_start_index + pre_day_num + 1]
        close = np.array(rows.loc[:, 'close'])
        if close[3] > close[0]:
            res.append(1)
        elif close[3] == close[0]:
            res.append(0)
        else:
            res.append(-1)
    return res


def kdj_centroids(kdj_centroids_data_file: str) -> (pd.DataFrame, typing.Dict[int, list]):
    """
    处理kdj聚类的结果
    """
    kdj_centroids_data = pd.read_csv(kdj_centroids_data_file)
    j_dict = defaultdict(list)
    for _, row in kdj_centroids_data.iterrows():
        j_dict[row["簇"]].append(round(row["j"], 2))
    for k, v in j_dict.items():
        print(f"簇 {k}:\n{v}")
    return kdj_centroids_data, j_dict


def run_pre(kdj_centroids_data: pd.DataFrame, a, b, pre_day_num):
    """
    a: 代表买入信号的簇
    b: 代表卖出信号的簇
    pre_day_num: 要预测后续几天的趋势
    """
    p_arr = pre_stock(kdj_centroids_data, a, b)
    pre = pd.DataFrame(p_arr, columns=['预测涨跌'])
    arr = cal_rise_or_fall(pre_day_num)
    real_rise_or_fall = pd.DataFrame(arr, columns=['实际涨跌'])
    test_result = pd.concat([kdj_centroids_data, pre, real_rise_or_fall], axis=1)
    test_result.to_csv('result.csv', index=False)
    num = 0
    rose = 0
    for j in range(1000):
        if p_arr[j] == 1 or p_arr[j] == -1:
            num += 1
            if arr[j] == p_arr[j]:
                rose += 1
    probability2 = rose / num * 100
    print('probability2 = ', probability2)
    return probability2
