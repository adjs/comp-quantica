#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import math
from sklearn import preprocessing
from sklearn import datasets
import matplotlib.pyplot as plt
import numpy as np

#plot iris dataset - find a better way
def plot_iris():
    samples, classes = load_iris(classes=[0,1], features=[0,1])
    samples = standardization(samples)
    samples = normalization(samples)
    
    x = samples[:, :1]
    y = samples[:, 1:]
    x = np.reshape(x, (len(x),))
    y = np.reshape(y, (len(y),))
    
    plt.figure(figsize=(5, 5))
    plt.scatter(x, y, c=classes[:100], cmap='viridis', marker='^')
    
    plt.savefig("test.svg", format="svg")
    
    plt.show()
    
#Standardize a dataset along any axis
#Center to the mean and component wise scale to unit variance
def standardization(X):
    return preprocessing.scale(X)

#Scale input vectors individually to unit norm (vector length)
def normalization(X, norm='l2'):
    return preprocessing.normalize(X, norm)

#Load iris dataset from sklearn
#This dataset contains: 3 classes, 50 samples per class, 4 features
def load_dataset(classes=None, features=None):
    iris = datasets.load_iris()
    
    #X contains only samples with features specified in "features"
    if features == None:
        X = iris.data
    else:
        X = iris.data[:, features]
    
    #y contains the target classes for each of the 150 samples
    y = iris.target
    
    #dictionary to set sample number
    X = {i : X[i] for i in range(len(X))}
    
    #remove dict pairs where whose class is not of interest
    if classes != None:
        for i in range(len(y)):
            if y[i] not in classes:
                del X[i]
    
    #list of samples whose class is in "classes"    
    X = [v for v in X.values()]
    
    #return sample, class
    return X, y

#Load a specific sample from iris dataset
def load_sample(number, preprocess=True):
    #classes 0 and 1
    classes = [0,1]
    #features 0 and 1
    features = [0,1]
    X, y = load_iris(classes=classes, features=features)
    
    if preprocess:
        X = standardization(X)
        X = normalization(X)
    
    return X[number], y[number]

def preprocess(X):
    X = standardization(X)
    X = normalization(X)
    
    return X
