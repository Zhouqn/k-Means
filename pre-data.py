import pandas
import pandas as pd
import numpy as np

kdj_centroids_data = pd.read_csv('kdj_centroids_data.csv')
daily_data = pd.read_csv('daily_data.csv')


def preStock():
    """
    预测涨跌
    :return: 1000只股票预测涨跌数组
    """
    pre_arr = []
    for index, row in kdj_centroids_data.iterrows():
        centroids = row['簇']
        if centroids == 0.0:
            pre_arr.append(-1)
        elif centroids == 1.0:
            pre_arr.append(1)
        else:
            pre_arr.append(0)
    return pre_arr


def calRiseOrFall():
    """
    实际涨跌
    :return: 1000只股票实际涨跌数组
    """
    res = []
    for i in range(1, 1001):
        n = i * 30
        rows = daily_data[n-4:n]
        close = np.array(rows.loc[:, 'close'])
        if close[3] > close[0]:
            res.append(1)
        elif close[3] == close[0]:
            res.append(0)
        else:
            res.append(-1)
    return res


p_arr = preStock()
pre = pd.DataFrame(p_arr, columns=['预测涨跌'])
arr = calRiseOrFall()
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
