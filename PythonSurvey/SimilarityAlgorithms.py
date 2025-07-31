import faiss
import numpy as np

from Utilities import MultivariateTimeSeries as mts

def faissL2Search(collection : mts, vector : int, k : int):
    index = faiss.IndexFlatL2(len(collection.multivariateTimeSeries[0]))
    index.add(np.array(collection.multivariateTimeSeries[:vector] + collection.multivariateTimeSeries[vector + 1:]))

    squaredDistance, neighborIndexes = index.search(np.array([collection.multivariateTimeSeries[vector]]), k)
    neighborIndexes = neighborIndexes[0]
    neighborIndexes[neighborIndexes >= vector] += 1

    neighborLabels = np.zeros(len(collection.multivariateTimeSeries), dtype=int)
    neighborLabels[neighborIndexes] = 1
    return neighborLabels