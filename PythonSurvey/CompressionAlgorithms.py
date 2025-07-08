from Utilities import MultivariateTimeSeries as tss
from numpy.polynomial.polynomial import Polynomial as Pol
from numpy.fft import fft
from numpy import abs
import pywt

def checkParameters(multivariateTimeSeries : tss, intParameter : int):
    if not isinstance(multivariateTimeSeries, tss):
        raise TypeError(f"Erwarte ein TimeSeriesSegments Objekt, aber ein {type(multivariateTimeSeries)} erhalten.")
    if not isinstance(intParameter, int):
        raise TypeError(f"Erwarte ein int, aber ein {type(intParameter)} erhalten.")

def linearApproximation(multivariateTimeSeries : tss, segmentLength : int):
    checkParameters(multivariateTimeSeries, segmentLength)
    
    compressedMultivariateTimeSeries = []
    for i in multivariateTimeSeries.multivariateTimeSeries:
        y_fits = []
        for j in range(0, multivariateTimeSeries.timeSeries_length, segmentLength):
            # hier in der arbeit erwähnen dass die x werte keine Rolle spielen, außer dass sie den gleichen abstand haben, weil bei der datenauswahl gleichmäßige intervalle gewählt werden
            rightBoundary = j + segmentLength if j + segmentLength <= len(i) else len(i)
            # und hier erwähnen dass die Verfälschung vom letzten Segment keine Rolle spielt, weil es bei jeder Zeitreihe verfälscht wird
            p = Pol.fit(range(j, rightBoundary), i[j:rightBoundary], deg=1)
            y_fits.append(p(range(0, segmentLength, segmentLength - 1)))

        compressedMultivariateTimeSeries.append(y_fits)
    return compressedMultivariateTimeSeries

def polynomialApproximation(multivariateTimeSeries : tss, segmentLength : int):
    checkParameters(multivariateTimeSeries, segmentLength)

    compressedMultivariateTimeSeries = []
    for i in multivariateTimeSeries.multivariateTimeSeries:
        coefficients = []
        for j in range(0, multivariateTimeSeries.timeSeries_length, segmentLength):
            rightBoundary = j + segmentLength if j + segmentLength <= len(i) else len(i)
            p = Pol.fit(range(j, rightBoundary), i[j:rightBoundary], deg=3)
            coefficients.append(p.convert().coef)
        
        compressedMultivariateTimeSeries.append(coefficients)
    return compressedMultivariateTimeSeries

def dwtApproximation(multivariateTimeSeries : tss, iterations : int):
    checkParameters(multivariateTimeSeries, iterations)

    compressedMultivariateTimeSeries = []
    for i in multivariateTimeSeries.multivariateTimeSeries:
        data = i
        for j in range(0, iterations):
            coefApprox, coefDiff = pywt.dwt(data, 'db1')
            data = coefApprox
        compressedMultivariateTimeSeries.append(data)
    return compressedMultivariateTimeSeries

def dftApproximation(multivariateTimeSeries : tss, threshold : int):
    checkParameters(multivariateTimeSeries, threshold)

    compressedMultivariateTimeSeries = []
    for i in multivariateTimeSeries.multivariateTimeSeries:
        freq = len(i)
        sp = fft(i)
        sp[abs(sp) < threshold] = 0
        compressedMultivariateTimeSeries.append(sp)
    return compressedMultivariateTimeSeries