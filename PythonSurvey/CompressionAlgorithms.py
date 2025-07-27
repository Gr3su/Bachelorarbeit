from Utilities import MultivariateTimeSeries as mts
from numpy.polynomial.polynomial import Polynomial as Pol
from numpy.fft import fft
import numpy as np
import pywt

def checkParameters(multivariateTimeSeries : mts, intParameter : int):
    if not isinstance(multivariateTimeSeries, mts):
        raise TypeError(f"Erwarte ein TimeSeriesSegments Objekt, aber ein {type(multivariateTimeSeries)} erhalten.")
    if not isinstance(intParameter, int):
        raise TypeError(f"Erwarte ein int, aber ein {type(intParameter)} erhalten.")

def linearApproximation(multivariateTimeSeries : mts, segmentLength : int):
    checkParameters(multivariateTimeSeries, segmentLength)
    
    compressedMultivariateTimeSeries = []
    for i in multivariateTimeSeries.multivariateTimeSeries:
        y_fits = np.array([])
        for j in range(0, multivariateTimeSeries.timeSeriesLength, segmentLength):
            # hier in der arbeit erwähnen dass die x werte keine Rolle spielen, außer dass sie den gleichen abstand haben, weil bei der datenauswahl gleichmäßige intervalle gewählt werden
            rightBoundary = j + segmentLength if j + segmentLength <= len(i) else len(i)
            # und hier erwähnen dass die Verfälschung vom letzten Segment keine Rolle spielt, weil es bei jeder Zeitreihe verfälscht wird
            p = Pol.fit(range(0, segmentLength), i[j:rightBoundary], deg=1)
            y_fits = np.append(y_fits, p(range(0, segmentLength, segmentLength - 1)))

        compressedMultivariateTimeSeries.append(y_fits.astype(float).tolist())
    return compressedMultivariateTimeSeries

def polynomialApproximation(multivariateTimeSeries : mts, segmentLength : int):
    checkParameters(multivariateTimeSeries, segmentLength)

    compressedMultivariateTimeSeries = []
    for i in multivariateTimeSeries.multivariateTimeSeries:
        coefficients = np.array([])
        for j in range(0, multivariateTimeSeries.timeSeriesLength, segmentLength):
            rightBoundary = j + segmentLength if j + segmentLength <= len(i) else len(i)
            p = Pol.fit(range(0, segmentLength), i[j:rightBoundary], deg=3)
            coefficients = np.append(coefficients, p.convert().coef)
        
        compressedMultivariateTimeSeries.append(coefficients.astype(float).tolist())
    return compressedMultivariateTimeSeries

def dwtApproximation(multivariateTimeSeries : mts, iterations : int):
    checkParameters(multivariateTimeSeries, iterations)

    compressedMultivariateTimeSeries = []
    for i in multivariateTimeSeries.multivariateTimeSeries:
        data = i
        for j in range(0, iterations):
            coefApprox, coefDiff = pywt.dwt(data, 'db1')
            data = coefApprox
        compressedMultivariateTimeSeries.append(data.astype(float).tolist())
    return compressedMultivariateTimeSeries

def dftApproximation(multivariateTimeSeries : mts, keepPercentile : float):
    #checkParameters(multivariateTimeSeries, keepPercentile)

    compressedMultivariateTimeSeries = []
    for i in multivariateTimeSeries.multivariateTimeSeries:
        sp = fft(i)
        sp = sp[:len(sp) // 2]
        threshold = np.percentile(np.abs(sp), 100 - keepPercentile)
        sp[np.abs(sp) < threshold] = 0
        sp = np.abs(sp)
        
        compressedMultivariateTimeSeries.append(sp.astype(float).tolist())

    max_index = 0
    for i in compressedMultivariateTimeSeries:
        nonzeroIndex = np.nonzero(i)[0][-1].tolist()
        max_index = max(max_index, nonzeroIndex)
        
    if max_index != 0:
        compressedMultivariateTimeSeries = [arr[0:max_index+1] for arr in compressedMultivariateTimeSeries]

    return compressedMultivariateTimeSeries