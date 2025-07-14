from pyod.models.knn import KNN
from pyod.models.lof import LOF
from pyod.models.iforest import IForest
from pyod.models.mad import MAD
from Utilities import MultivariateTimeSeries as tss
from time import perf_counter
import numpy as np

def knnDetection(multivariateTimeSeries : tss):
    clf = KNN()
    clf.fit(multivariateTimeSeries.multivariateTimeSeries)
    return clf.labels_

def lofDetection(multivariateTimeSeries : tss):
    clf = LOF()
    clf.fit(multivariateTimeSeries.multivariateTimeSeries)
    return clf.labels_

def isolationForestDetection(multivariateTimeSeries : tss):
    clf = IForest()
    clf.fit(multivariateTimeSeries.multivariateTimeSeries)
    return clf.labels_

def randomProjectionsDetection(multivariateTimeSeries : tss):
    scores = np.zeros(len(multivariateTimeSeries.multivariateTimeSeries))

    for i in range(100):
        randomVector = np.random.randn(multivariateTimeSeries.timeSeriesLength)
        coeffs = []
        for series in multivariateTimeSeries.multivariateTimeSeries:
            coeffs.append([np.dot(series, randomVector)])
        clf = MAD()
        clf.fit(coeffs)
        scores += clf.labels_
    clf = MAD()
    clf.fit([[x] for x in scores])
    return clf.labels_



def execCalcRuntime(func, *args):
    start = perf_counter()
    result = func(*args)
    end = perf_counter()
    return result, end - start