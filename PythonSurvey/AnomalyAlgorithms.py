from pyod.models.knn import KNN
from pyod.models.lof import LOF
from pyod.models.iforest import IForest
from pyod.models.mad import MAD
from Utilities import MultivariateTimeSeries as mts
import numpy as np

def knnDetection(multivariateTimeSeries : mts):
    detector = KNN()
    detector.fit(multivariateTimeSeries.multivariateTimeSeries)
    return detector.labels_

def lofDetection(multivariateTimeSeries : mts):
    detector = LOF()
    detector.fit(multivariateTimeSeries.multivariateTimeSeries)
    return detector.labels_

def isolationForestDetection(multivariateTimeSeries : mts):
    detector = IForest()
    detector.fit(multivariateTimeSeries.multivariateTimeSeries)
    return detector.labels_

def randomProjectionsDetection(multivariateTimeSeries : mts):
    scores = np.zeros(len(multivariateTimeSeries.multivariateTimeSeries))

    for i in range(50):
        randomVector = np.abs(np.random.randn(multivariateTimeSeries.timeSeriesLength))
        values = []
        for series in multivariateTimeSeries.multivariateTimeSeries:
            values.append([np.dot(series, randomVector)])
        detector = MAD()
        detector.fit(values)
        scores += detector.decision_scores_
    detector = MAD()
    detector.fit([[x] for x in scores])
    return detector.labels_