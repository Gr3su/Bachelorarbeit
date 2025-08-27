import sys, os

from Utilities import MultivariateTimeSeries as mts
from Utilities import execCalcRuntime
import CompressionAlgorithms as comp
import AnomalyAlgorithms as anom
import SimilarityAlgorithms as sim
import numpy as np

def formatCheck(lines):
    if not lines:
        raise ValueError("Die Datei darf nicht leer sein.")
    for i in lines:
        if not i:
            raise ValueError("Die Datei darf keine Leerzeile enthalten.")
        if not isFloatArray(i):
            raise ValueError(f"Eine Zeile enthaelt keine Zahl, sondern folgendes: {i}")

def isFloatArray(value : str):
    try:
        [float(i) for i in value.split(", ")]
        return True
    except:
        return False
    
    
def writeFiles(paths : list[str], pathExtension, contents):
    for path, content in zip(paths, contents):
        newFileName = os.path.splitext(os.path.basename(path))[0] + ".csv"
        newPath = os.path.join(os.path.dirname(path), "../compressed/" + pathExtension, newFileName)

        os.makedirs(os.path.dirname(newPath), exist_ok=True)
        with open(newPath, 'w', encoding='utf-8') as f:
            f.write(str(content)[1:-1])

def computeClassificationMetrics(original, toCompare):
    tp = np.sum((original == 1) & (toCompare == 1))
    tn = np.sum((original == 0) & (toCompare == 0))
    fp = np.sum((original == 0) & (toCompare == 1))
    fn = np.sum((original == 1) & (toCompare == 0))

    return tp, tn, fp, fn

if __name__ == "__main__":
    # Holen aller echten Dateien
    full_paths = [os.path.join(sys.argv[1], filename) for filename in os.listdir(sys.argv[1])]
    full_paths = [path for path in full_paths if os.path.isfile(path)]

    # Einlesen jeder Datei und zum validieren in MultivariateTimeSeries Objekt stecken 
    timeSeries = []
    for path in full_paths:
        with open(path, "r") as f:
            lines = f.readlines()
            formatCheck(lines)

            timeSeries.append([float(x) for x in lines[0].strip().split(",")])

    checkedTimeSeries = mts(timeSeries)

    # Komprimieren und speichern der Kompressionen
    linTS = comp.linearApproximation(checkedTimeSeries, int(sys.argv[2]))
    writeFiles(full_paths, "linearApprox", linTS)
    polTS = comp.polynomialApproximation(checkedTimeSeries, int(sys.argv[3]))
    writeFiles(full_paths, "polyApprox", polTS)
    dftTS = comp.dftApproximation(checkedTimeSeries, float(sys.argv[4]))
    writeFiles(full_paths, "fourierApprox", dftTS)
    dwtTS = comp.dwtApproximation(checkedTimeSeries, int(sys.argv[5]))
    writeFiles(full_paths, "waveletApprox", dwtTS)
    results = ""

    # Anomalieerkennung und Erstellung / Speicherung von Ergebnisdatei
    originalResults = {}
    chosenVector = -1
    for i, (data, name) in enumerate(zip((checkedTimeSeries, mts(linTS), mts(polTS), mts(dwtTS), mts(dftTS)),
                    ("Original", "Linear Approx.", "Polynomial Approx.", "Discrete Wavelet Trans.", "Discrete Fourier Trans."))):
        results += f"{name} Data - Results\n"

        # knn
        detection = "knn"
        labels, time = execCalcRuntime(anom.knnDetection, data)
        results += f"knn Detection - Took {time}s to complete.\n"
        try:
            files = sorted([int(os.path.splitext(os.path.basename(full_paths[i]))[0]) for i in np.where(labels == 1)[0]])
        except:
            files = [os.path.splitext(os.path.basename(full_paths[i]))[0] for i in np.where(labels == 1)[0]]
        files = ", ".join([str(x) for x in files])
        
        if i == 0:
            originalResults[detection] = labels
            results += files + "\n"
        else:
            tp, tn, fp, fn = computeClassificationMetrics(originalResults[detection], labels)
            results += f"{{{tp}}} {{{tn}}} {{{fp}}} {{{fn}}} {{{(tn + tp) / (tn + tp + fn + fp):.2f}}} {{{tp/(tp+fp) if tp +fp != 0 else 0.00:.2f}}}\n"
            results += f"True positive: {tp}\nTrue negative: {tn}\nFalse positive:{fp}\nFalse negative: {fn}\nAccuracy: {(tn + tp) / (tn + tp + fn + fp)}\nPrecision: {tp/(tp+fp) if tp +fp != 0 else 0}\n{files}\n\n\n"

        # iForest
        detection = "iForest"
        labels, time = execCalcRuntime(anom.isolationForestDetection, data)
        results += f"iForest Detection - Took {time}s to complete.\n"
        try:
            files = sorted([int(os.path.splitext(os.path.basename(full_paths[i]))[0]) for i in np.where(labels == 1)[0]])
        except:
            files = [os.path.splitext(os.path.basename(full_paths[i]))[0] for i in np.where(labels == 1)[0]]
        files = ", ".join([str(x) for x in files])

        if i == 0:
            originalResults[detection] = labels
            results += files + "\n"
        else:
            tp, tn, fp, fn = computeClassificationMetrics(originalResults[detection], labels)
            results += f"{{{tp}}} {{{tn}}} {{{fp}}} {{{fn}}} {{{(tn + tp) / (tn + tp + fn + fp):.2f}}} {{{tp/(tp+fp) if tp +fp != 0 else 0.00:.2f}}}\n"
            results += f"True positive: {tp}\nTrue negative: {tn}\nFalse positive:{fp}\nFalse negative: {fn}\nAccuracy: {(tn + tp) / (tn + tp + fn + fp)}\nPrecision: {tp/(tp+fp) if tp +fp != 0 else 0}\n{files}\n\n\n"

        # Random Projection
        detection = "randomP"
        labels, time = execCalcRuntime(anom.randomProjectionsDetection, data)
        results += f"Random Projection Detection - Took {time}s to complete.\n"
        try:
            files = sorted([int(os.path.splitext(os.path.basename(full_paths[i]))[0]) for i in np.where(labels == 1)[0]])
        except:
            files = [os.path.splitext(os.path.basename(full_paths[i]))[0] for i in np.where(labels == 1)[0]]
        files = ", ".join([str(x) for x in files])

        if i == 0:
            originalResults[detection] = labels
            results += files + "\n"
        else:
            tp, tn, fp, fn = computeClassificationMetrics(originalResults[detection], labels)
            results += f"{{{tp}}} {{{tn}}} {{{fp}}} {{{fn}}} {{{(tn + tp) / (tn + tp + fn + fp):.2f}}} {{{tp/(tp+fp) if tp +fp != 0 else 0.00:.2f}}}\n"
            results += f"True positive: {tp}\nTrue negative: {tn}\nFalse positive:{fp}\nFalse negative: {fn}\nAccuracy: {(tn + tp) / (tn + tp + fn + fp)}\nPrecision: {tp/(tp+fp) if tp +fp != 0 else 0}\n{files}\n\n\n"
        
        # Similarity Search
        detection = "similarity"
        k = 100
        if i == 0:
            chosenVector = np.random.randint(0, len(data.multivariateTimeSeries))
            labels, time = execCalcRuntime(sim.faissL2Search, data, chosenVector, k)
            originalResults[detection] = labels
        else:
            labels, time = execCalcRuntime(sim.faissL2Search, data, chosenVector, k)
            tp, tn, fp, fn = computeClassificationMetrics(originalResults[detection], labels)
        results += f"Similarity Search with k={k} - Took {time}s to complete.\n"
        try:
            files = sorted([int(os.path.splitext(os.path.basename(full_paths[i]))[0]) for i in np.where(labels == 1)[0]])
        except:
            files = [os.path.splitext(os.path.basename(full_paths[i]))[0] for i in np.where(labels == 1)[0]]
        files = ", ".join([str(x) for x in files])

        if i == 0:
            results += files + "\n\n\n"
        else:
            results += f"{{{tp}}} {{{tn}}} {{{fp}}} {{{fn}}} {{{(tn + tp) / (tn + tp + fn + fp):.2f}}} {{{tp/(tp+fp) if tp +fp != 0 else 0.00:.2f}}}\n"
            results += f"True positive: {tp}\nTrue negative: {tn}\nFalse positive:{fp}\nFalse negative: {fn}\nAccuracy: {(tn + tp) / (tn + tp + fn + fp)}\nPrecision: {tp/(tp+fp) if tp +fp != 0 else 0}\n{files}\n\n\n"
        
    results = results.strip()

    resultsPath = sys.argv[1] + "../anomalyResults.txt"
    with open(resultsPath, 'w', encoding='utf-8') as f:
        f.write(results)
