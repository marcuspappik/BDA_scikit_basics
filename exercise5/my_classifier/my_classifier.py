import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from scipy import stats

class my_classifier(object):

    def fit(self, X, Y):
        return self


    def predict(self, X):
        random_results = self.predict_proba(X)
        return random_results[:,1] > 0.5


    def transform(self, X):
        return self.predict(X)


    def predict_proba(self, X):
        random_results = np.random.random(len(X))
        return np.c_[1-random_results, random_results]


class my_classifier2(object):

    def __init__(self):
        self.probability = 0


    def fit(self, X, Y):
        self.probability = (np.sum(Y==1))/len(Y)
        return self


    def predict(self, X):
        random_results = self.predict_proba(X)
        return random_results[:,1] > 0.5


    def transform(self, X):
        return self.predict(X)


    def predict_proba(self, X):
        mean = self.probability
        random_results = np.random.normal(0, 0.01, len(X))
        if(min(mean, 1-mean) < max(np.abs(random_results))):
            random_results = random_results * min(mean, 1-mean) / max(np.abs(random_results))
        random_results = random_results + mean
        return np.c_[1-random_results, random_results]
