import csv

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from tqdm import trange
import matplotlib.pyplot as plt


def KMeans(x, k, no_of_iterations):
    cid = np.random.choice(len(x), k, replace=False)
    # choose random centroids
    centroids = x[cid, :]

    # distance between centroids and all the data points
    distances = cdist(x, centroids, 'euclidean')

    # Centroid with the minimum distance
    points = np.array([np.argmin(distance) for distance in distances])

    for times in trange(no_of_iterations):
        centroids = []
        for cid in range(k):
            # updating centroids by taking mean of cluster it belongs to
            temp_cent = np.mean(x[points == cid], axis=0)
            centroids.append(temp_cent)

        # updated centroids
        centroids = np.array(centroids)
        distances = cdist(x, centroids, 'euclidean')

        points = np.array([np.argmin(distance) for distance in distances])

    return points, centroids


def readPoints():
    points = []
    names = []
    with open('dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            # Complete appending point (row1, row2) to points list
            points.append((row[1], row[2]))
            names.append(row[0])
    return points, names


if __name__ == "__main__":
    # load data
    data, names = readPoints()
    # Use skikit learns PCA s
    pca = PCA(2)

    # transform the data aka fit the model with X and apply the dimensionality reduction on X
    df = pca.fit_transform(data)

    label, centroid = KMeans(df, 4, 1000)

    code_names = []
    for name in names:
        if name == 'A':
            code_names.append(0)
        if name == 'B':
            code_names.append(1)
        if name == 'C':
            code_names.append(2)
        if name == 'D':
            code_names.append(3)

    print(accuracy_score(label, code_names))

    u_labels = np.unique(label)
    for i in u_labels:
        # Complete the scatter plot
        plt.scatter(df[label == i, 0], df[label == i, 1], label=i)
    plt.scatter(centroid[:, 0], centroid[:, 1], color='black')
    plt.legend()
    plt.show()
