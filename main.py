import kMeans
from pre_data import run_pre

kdj_centroids_data = kMeans.clustering()

run_pre(kdj_centroids_data)
