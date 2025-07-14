import sys, os

from Utilities import MultivariateTimeSeries as tss
import CompressionAlgorithms as comp
import AnomalyAlgorithms as anom
import numpy as np
import re

def formatCheck(lines):
    if not lines:
        raise ValueError("Die Datei darf nicht leer sein.")
    for i in lines:
        if not i:
            raise ValueError("Die Datei darf keine Leerzeile enthalten.")
        if not isFloatArray(i):
            raise ValueError(f"Eine Zeile enthaelt keine Zahl, sondern folgendes: {i}")

def isFloatArray(value):
    pattern = r'^(-?\d+(?:\.\d+)?)(,\s*-?\d+(?:\.\d+)?)*$'
    if re.fullmatch(pattern, value):
        return True
    return False
    
def writeFiles(paths : list[str], pathExtension, contents):
    for path, content in zip(paths, contents):
        newFileName = os.path.splitext(os.path.basename(path))[0] + ".csv"
        newPath = os.path.join(os.path.dirname(path), "../compressed/" + pathExtension, newFileName)

        os.makedirs(os.path.dirname(newPath), exist_ok=True)
        with open(newPath, 'w', encoding='utf-8') as f:
            f.write(str(content)[1:-1])

if __name__ == "__main__":
    full_paths = [os.path.join(sys.argv[1], filename) for filename in os.listdir(sys.argv[1])]
    full_paths = [path for path in full_paths if os.path.isfile(path)]

    timeSeries = []
    for path in full_paths:
        with open(path, "r") as f:
            lines = f.readlines()
            formatCheck(lines)

            timeSeries.append([float(x) for x in lines[0].strip().split(",")])

    checkedTimeSeries = tss(timeSeries)

    linTS = comp.linearApproximation(checkedTimeSeries, int(sys.argv[2]))
    writeFiles(full_paths, "linearApprox", linTS)
    polTS = comp.polynomialApproximation(checkedTimeSeries, int(sys.argv[3]))
    writeFiles(full_paths, "polyApprox", polTS)
    dwtTS = comp.dwtApproximation(checkedTimeSeries, int(sys.argv[4]))
    writeFiles(full_paths, "waveletApprox", dwtTS)
    dftTS = comp.dftApproximation(checkedTimeSeries, int(sys.argv[5]) if len(sys.argv) == 6 else 10)
    writeFiles(full_paths, "fourierApprox", dftTS)
    dftTS = list(np.abs(dftTS))
    results = ""

    for data, name in zip((checkedTimeSeries, tss(linTS), tss(polTS), tss(dwtTS), tss(dftTS)),
                    ("Original", "Linear Approx.", "Polynomial Approx.", "Discrete Wavelet Trans.", "Discrete Fourier Trans.")):
        results += f"{name} Data - Results\n"
        labels, time = anom.execCalcRuntime(anom.knnDetection, data)
        indexes = np.where(labels == 1)[0]
        results += f"knn Detection - Took {time}s to complete.\n\tIndixes:{indexes}\n"
        labels, time = anom.execCalcRuntime(anom.isolationForestDetection, data)
        indexes = np.where(labels == 1)[0]
        results += f"iForest Detection - Took {time}s to complete.\n\tIndixes:{indexes}\n"
        labels, time = anom.execCalcRuntime(anom.randomProjectionsDetection, data)
        indexes = np.where(labels == 1)[0]
        results += f"Random Projection Detection - Took {time}s to complete.\n\tIndixes:{indexes}\n\n\n"
    
    results = results.strip()

    resultsPath = sys.argv[1] + "../anomalyResults.txt"
    with open(resultsPath, 'w', encoding='utf-8') as f:
        f.write(results)
