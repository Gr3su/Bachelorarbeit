from pyod.models.knn import KNN
from pyod.models.lof import LOF
from pyod.models.iforest import IForest
from pyod.models.mad import MAD
from Utilities import MultivariateTimeSeries as mts
import numpy as np

def knnDetection(multivariateTimeSeries : mts):
    clf = KNN()
    clf.fit(multivariateTimeSeries.multivariateTimeSeries)
    return clf.labels_

def lofDetection(multivariateTimeSeries : mts):
    clf = LOF()
    clf.fit(multivariateTimeSeries.multivariateTimeSeries)
    return clf.labels_

def isolationForestDetection(multivariateTimeSeries : mts):
    clf = IForest()
    clf.fit(multivariateTimeSeries.multivariateTimeSeries)
    return clf.labels_

def randomProjectionsDetection(multivariateTimeSeries : mts):
    scores = np.zeros(len(multivariateTimeSeries.multivariateTimeSeries))

    for i in range(100):
        randomVector = np.random.randn(multivariateTimeSeries.timeSeriesLength)
        coeffs = []
        for series in multivariateTimeSeries.multivariateTimeSeries:
            coeffs.append([np.dot(series, randomVector)])
        clf = MAD()
        clf.fit(coeffs)
        scores += clf.decision_scores_
    clf = MAD()
    clf.fit([[x] for x in scores])
    return clf.labels_