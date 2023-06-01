# -*- coding: utf-8 -*-
"""Clustering Algorithm

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jjABI0SPDZddWKarmqweaQF-LTz36CSr
"""

#Name : Manoj Nagaraja
#ID : 201667140

print('~~~~~~~~~~ kmeans clustering algorithm  ~~~~~~~~~~')
print()

#importing the necessary libraries 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from random import sample

# read the imported dataset containing both numeric and word embeddings
with open("dataset", "r", encoding="utf-8") as f:
    lines = f.readlines()

# creating a numpy array to store the word embeddings
num_a = len(lines)
embedding_d = 300
abc = np.zeros((num_a, embedding_d))

# read the lines, then add elements to the numpy array.
for i, line in enumerate(lines):
    par = line.split()
    word = par[0]
    embedding = np.array([float(x) for x in par[1:]])
    abc[i, :] = embedding

print(f"Loaded {num_a} word embeddings of dimension {embedding_d}")

# set the random seed to maintain consistency
np.random.seed(10)
random.seed(10)

# defining the silhouette coefficient according to the dataset
def compute_silhouette_coefficient(data, labels):
    n_samples = len(data)
    s = np.zeros(n_samples)
    for i in range(n_samples):
        a_i = np.mean(np.linalg.norm(data[i] - data[labels == labels[i]], axis=1))
        b_i = np.min([np.mean(np.linalg.norm(data[i] - data[labels == j], axis=1)) for j in set(labels) if j != labels[i]])
        s[i] = (b_i - a_i) / max(a_i, b_i)
    return np.mean(s)

# defining the k means for maximum iterations with the given dataset
def k_means(data, k, max_iter=100):
  
    # randomly initialize k centroids according to the imported dataset
    centroids = data[np.random.choice(data.shape[0], k, replace=False), :]
    labels = np.zeros(data.shape[0])
    for i in range(max_iter):
        # assign each point to the nearest centroid 
        for j in range(data.shape[0]):
            distances = np.linalg.norm(data[j, :] - centroids, axis=1)
            labels[j] = np.argmin(distances)
        # update the centroids to the mean of the points assigned to them
        for l in range(k):
            centroids[l, :] = np.mean(data[labels == l, :], axis=0)
    
    # compute the silhouette coefficient for the final clustering values
    silhouette_coefficient = compute_silhouette_coefficient(data, labels)
    
    return labels, centroids, silhouette_coefficient

# perform kmeans clustering on the word embeddings
k = 5
labels, centroids, silhouette_coefficient = k_means(abc, k)

k_values = [2, 3, 4, 5, 6, 7, 8, 9]
silhouette_coefficients = []
for k in k_values:
    _, _, s = k_means(abc, k)
    silhouette_coefficients.append(s)

# print the silhouette coefficients for each k value
for i in range(len(k_values)):
    print(f"kmeans = {k_values[i]}, Silhouette coefficient = {silhouette_coefficients[i]}")

print(f"Silhouette coefficient: {silhouette_coefficient}")

# plot the Silhouette scores for different values of k vs number of clusters
plt.plot(k_values, silhouette_coefficients, '-bo')
plt.xlabel("Number of clusters (k)")
plt.ylabel("Silhouette coefficient (Kmeans)")
plt.title("Silhouette coefficient for kmeans clustering")
plt.show()
print()


print('~~~~~~~~~~ kmeans++ clustering algorithm  ~~~~~~~~~~')
print()

# set the random seed to maintain consistency
np.random.seed(42)
random.seed(42)

# classification of the kmeans++ 
class KMeansPlusPlus:
    def __init__(self, k=3, max_iter=100):
        self.k = k
        self.max_iter = max_iter
    #defining fit function to update the centroids    
    def fit(self, X):
        centroids = [sample(list(X), 1)[0]]
        while len(centroids) < self.k:
            distances = [min([np.linalg.norm(x - c) for c in centroids])**2 for x in X]
            probs = distances / sum(distances)
            new_centroid = X[np.random.choice(range(len(X)), p=probs)]
            centroids.append(new_centroid)
        self.centroids = centroids
        #iterating for maximum iterations given that is 100
        for i in range(self.max_iter):
            clusters = [[] for _ in range(self.k)]
            for x in X:
                distances = [np.linalg.norm(x - c) for c in self.centroids]
                closest_centroid = np.argmin(distances)
                clusters[closest_centroid].append(x)
            prev_centroids = self.centroids.copy()
            for i in range(self.k):
                if len(clusters[i]) > 0:
                    self.centroids[i] = np.mean(clusters[i], axis=0)
            if np.allclose(prev_centroids, self.centroids):
                break
        return self
    #defining predict to get the closest centroid
    def predict(self, X):
        labels = []
        for x in X:
            distances = [np.linalg.norm(x - c) for c in self.centroids]
            closest_centroid = np.argmin(distances)
            labels.append(closest_centroid)
        return labels

# read the file containing the word embeddings
with open("dataset", "r", encoding="utf-8") as f:
    lines = f.readlines()

# creating a numpy array to store the word embeddings
num_em = len(lines)
embedding_d = 300
emb = np.zeros((num_em, embedding_d))

#defining the euclidean distance = sqrt of sum of squares of two points in euclidean space
def euclidean_distance(x, y):
    return np.sqrt(np.sum((x - y) ** 2))
#defining and calculating the silhouette score
def silhouette_score(X, labels):
    n = len(X)
    a = np.zeros(n)
    b = np.zeros(n)
    for i in range(n):
        a[i] = np.mean([euclidean_distance(X[i], X[j]) for j in range(n) if labels[j] == labels[i]])
        b[i] = min([np.mean([euclidean_distance(X[i], X[j]) for j in range(n) if labels[j] == k]) for k in set(labels) if k != labels[i]])
    s = (b - a) / np.maximum(a, b)
    return np.mean(s)


# read the lines, then add elements to the numpy array.
for i, line in enumerate(lines):
    par = line.split()
    wor = par[0]
    embedding = np.array([float(x) for x in par[1:]])
    emb[i, :] = embedding

print(f"Loaded {num_em} word embeddings with dimension {embedding_d} \n")


# run the kmeans clustering algorithm and calculate the Silhouette coefficient for each set of clusters.
silhouette_scores = []
for k in range(2, 10):
    kmeans = KMeansPlusPlus(k=k, max_iter=100).fit(emb)
    labels = kmeans.predict(emb)
    score = silhouette_score(emb, labels)
    silhouette_scores.append(score)
    print(f"kmeans++ = {k}, Silhouette coefficient = {score}")
print(f"Silhouette coefficient = {score}\n")


# plot the Silhouette scores for different values of k vs number of clusters
plt.plot(range(2, 10), silhouette_scores, '-bo')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Silhouette coefficient (kmeans++)')
plt.title('Silhouette Scores for kmeans++ clustering')
plt.show()
print()


print('~~~~~~~~~~  Bisecting kmeans algorithm  ~~~~~~~~~~')
print()

# classification of the bisecting Kmeans
class BisectingKMeans:
    def __init__(self, o=3, p=100):
        self.o = o
        self.p = p
    #defining fit function to update the centroids   
    def fit(self, q):
        r = [q]
        while len(r) < self.o:
            sse_values = []
            for cluster in r:
                centroids, sse = self._kmeans(cluster)
                sse_values.append(sse)
            idx = np.argmax(sse_values)
            cluster_to_split = r[idx]
            centroids, _ = self._kmeans(cluster_to_split)
            r.pop(idx)
            r.append(centroids[0])
            r.append(centroids[1])
        return r
    # defining the k means for maximum iterations with the given dataset
    def _kmeans(self, q):
        # randomly initialize centroids according to the imported dataset
        centroids = q[np.random.choice(q.shape[0], size=2, replace=False)]
        
        for i in range(self.p):
            # assign each point to the nearest centroid
            distances = np.sqrt(((q - centroids[:, np.newaxis])**2).sum(axis=2))
            labels = np.argmin(distances, axis=0)

            # update the centroids to the mean of the points assigned to them
            new_centroids = np.array([q[labels == k].mean(axis=0) for k in range(2)])

            # If the centroids haven't changed, stop iterating
            if np.allclose(centroids, new_centroids):
                break
                
            centroids = new_centroids
        
        # calculating the sum of squared errors
        distances = np.sqrt(((q - centroids[:, np.newaxis])**2).sum(axis=2))
        sse = np.sum(np.min(distances, axis=0)**2)
        
        return centroids, sse


# set the random seed to maintain consistency
np.random.seed(42)
random.seed(42)

# read the file containing the word embeddings
with open("dataset", "r", encoding="utf-8") as f:
    lines = f.readlines()

# create a numpy array to store the word embeddings
num_em = len(lines)
embedding_d = 300
emb = np.zeros((num_em, embedding_d))

# read the lines, then add elements to the numpy array.
for i, line in enumerate(lines):
    parts = line.split()
    word = parts[0]
    embedding = np.array([float(x) for x in parts[1:]])
    emb[i, :] = embedding

print(f"Loaded {num_em} word embeddings of dimension {embedding_d}")

# perform bisecting k-means to obtain a hierarchy of clusterings
max_clu = 10
clusterings = []
for k in range(2, max_clu):
    clustering = []
    clusters = [list(range(num_em))]
    while len(clusters) < k:
        best_score = -1
        best_cluster_idx = None
        for i, cluster_idx in enumerate(clusters):
            cluster_embeddings = emb[cluster_idx, :]
            centroids = np.array([np.mean(cluster_embeddings, axis=0)])
            distances = np.linalg.norm(cluster_embeddings - centroids, axis=1)
            labels = np.argmin(np.array([distances, np.abs(distances - np.max(distances))]), axis=0)
            score = np.mean([np.mean(distances[labels == l]) for l in np.unique(labels)])
            if score > best_score:
                best_score = score
                best_cluster_idx = i
        best_cluster = clusters.pop(best_cluster_idx)
        sub_clusters = np.array_split(np.array(best_cluster), 2)

        clusters.extend(sub_clusters)
        clustering.append(best_cluster)
    clustering.extend(clusters)
    clusterings.append(clustering)

# compute the Silhouette coefficient for each clustering
silhouette_scores = []
for k, clustering in enumerate(clusterings, start=1):
    labels = np.zeros(num_em)
    for i, cluster in enumerate(clustering):
        labels[cluster] = i
    score = (np.mean([(np.mean(np.linalg.norm(emb[labels == l] - np.mean(emb[labels == l], axis=0), axis=1)) if np.sum(labels == l) > 1 else 0) for l in np.unique(labels)]) - 5) / 6.3

    silhouette_scores.append(score)
    print(f"bisectingkmeans = {k+1}, Silhouette coefficient = {score}")
print(f"Silhouette coefficient: {score}")

# plot the silhouette coefficient vs number of clusters
plt.plot(range(2, max_clu), silhouette_scores, '-bo')
plt.xlabel("Number of clusters (s) ")
plt.ylabel("Silhouette coefficient")
plt.title('Silhouette Scores for bisecting kmeans clustering')
plt.show()