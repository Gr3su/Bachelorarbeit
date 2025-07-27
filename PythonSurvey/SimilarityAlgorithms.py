import faiss
import numpy as np

from Utilities import MultivariateTimeSeries as mts

def faissL2Search(collection : mts, vector : int, k : int):
    index = faiss.IndexFlatL2(len(collection.multivariateTimeSeries[0]))
    index.add(collection[:vector] + collection[vector + 1:])

    squaredDistance, neighborIndexes = index.search(collection.multivariateTimeSeries[vector], k)
    neighborIndexes = neighborIndexes[0]
    neighborIndexes[neighborIndexes >= vector] += 1

    neighborLabels = np.zeros(len(collection.multivariateTimeSeries), dtype=int)
    neighborLabels[neighborIndexes] = 1
    return neighborLabels