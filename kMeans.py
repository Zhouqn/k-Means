import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import kdj

kdj.creat_kdj_data()
kdj_data = pd.read_csv('stock_kdj.csv')


def euclidean_dist(vecA, vecB):
    """
    计算两个向量的欧式距离
    """
    return np.sqrt(np.sum(np.power(vecA - vecB, 2)))


def rand_cent(data_set, k):
    """
    随机生成k个点作为质心，其中质心均在整个数据数据的边界之内
    """
    n = data_set.shape[1]  # 获取数据的维度
    centroids = np.mat(np.zeros((k, n)))
    for j in range(n):
        minJ = np.min(data_set[:, j])
        rangeJ = np.max(data_set[:, j]) - minJ
        centroids[:, j] = minJ + rangeJ * np.random.rand(k, 1)
    # print('centroids = ')
    # print(centroids)
    return centroids


def kMeans(dataSet, k, distMeas=euclidean_dist, createCent=rand_cent):
    """
    k-Means聚类算法,返回最终的k各质心和点的分配结果
    """
    m = dataSet.shape[0]   # 获取样本数量
    clusterAssment = np.mat(np.zeros((m, 2)))
    # 1. 初始化k个质心
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = np.inf
            minIndex = -1
            # 2. 找出最近的质心
            for j in range(k):
                distJI = distMeas(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            # 3. 更新每一行样本所属的簇
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist**2
        # 4. 更新质心
        for cent in range(k):
            ptsCluster = dataSet[np.nonzero(clusterAssment[:, 0].A == cent)[0]]  # 获取给定簇的所有点
            centroids[cent, :] = np.mean(ptsCluster, axis=0)  # 沿矩阵列的方向求均值
    return centroids, clusterAssment


K = 3


def clustering():
    _kdj = kdj_data.iloc[:, 3:]
    X = np.array(_kdj)
    # myCentroids为簇质心
    my_centroids, clusterAssment = kMeans(X, K)
    # centroids = my_centroids.A # 将matrix转换为ndarray类型
    # 获取聚类后的样本所属的簇值，将matrix转换为ndarray
    y_kmeans = clusterAssment[:, 0].A[:, 0]
    kdj_centroids = pd.DataFrame(y_kmeans, columns=['簇'])
    kdj_centroids_data = pd.concat([pd.DataFrame(kdj_data), kdj_centroids], axis=1)
    kdj_centroids_data.to_csv('kdj_centroids_data.csv', index=False)
    show(X, y_kmeans)
    return kdj_centroids_data


def show(X, y_kmeans):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y_kmeans)
    plt.title('K-Means  k = ' + str(K))
    ax.set_xlabel('k')
    ax.set_ylabel('d')
    ax.set_zlabel('j')
    plt.show()

