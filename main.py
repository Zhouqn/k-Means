import kMeans
from pre_data import run_pre, kdj_centroids
from collections import defaultdict

if __name__ == '__main__':
    kMeans.clustering()

    kdj_centroids_data, j_dict = kdj_centroids('kdj_centroids_data.csv')
    a = int(input("输入你认为是涨的簇："))
    b = int(input("输入你认为是跌的簇："))
    pre_day_num = int(input("输入要预测的天数："))

    run_pre(kdj_centroids_data, a, b, pre_day_num)
