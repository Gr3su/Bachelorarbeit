from pyod.models.knn import KNN
from pyod.models.lof import LOF
from pyod.models.iforest import IForest
from Utilities import MultivariateTimeSeries as tss
from time import perf_counter

def knnDetection(multivariateTimeSeries : tss):
    clf = KNN()
    clf.fit(multivariateTimeSeries.multivariateTimeSeries)
    return clf.labels_

def lofDetectiob(multivariateTimeSeries : tss):
    clf = LOF()
    clf.fit(multivariateTimeSeries.multivariateTimeSeries)
    return clf.labels_

def isolationForestDetection(multivariateTimeSeries : tss):
    clf = IForest()
    clf.fit(multivariateTimeSeries.multivariateTimeSeries)
    return clf.labels_

def calcRuntime(func, *args):
    start = perf_counter()
    result = func(*args)
    end = perf_counter()
    return result, end - start