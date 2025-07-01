from Utilities import TimeSeries as tss
from numpy.polynomial.polynomial import Polynomial as Pol

def linearApproximation(timeSeries : tss, segmentLength : int):
    if not isinstance(timeSeries, tss):
        raise TypeError(f"Erwarte ein TimeSeriesSegments Objekt, aber ein {type(timeSeries)} erhalten.")
    if not isinstance(segmentLength, int):
        raise TypeError(f"Erwarte ein int, aber ein {type(segmentLength)} erhalten.")
    
    compressedTimeSeries = []
    for i in timeSeries.segments:
        y_fits = []
        for j in range(0, timeSeries.timeSeries_length, segmentLength):
            # hier in der arbeit erwähnen dass die x werte keine Rolle spielen, außer dass sie den gleichen abstand haben, weil bei der datenauswahl gleichmäßige intervalle gewählt werden
            rightBoundary = j + segmentLength if j + segmentLength <= len(i) else len(i)
            # und hier erwähnen dass die Verfälschung vom letzten Segment keine Rolle spielt, weil es bei jeder Zeitreihe verfälscht wird
            p = Pol.fit(range(j, rightBoundary), i[j:rightBoundary], deg=1)
            y_fits.append(p(range(0, segmentLength, segmentLength - 1)))

        compressedTimeSeries.append(y_fits)
    return compressedTimeSeries

def polynomialApproximation(timeSeries : tss, segmentLength : int):
    if not isinstance(timeSeries, tss):
        raise TypeError(f"Erwarte ein TimeSeriesSegments Objekt, aber ein {type(timeSeries)} erhalten.")
    if not isinstance(segmentLength, int):
        raise TypeError(f"Erwarte ein int, aber ein {type(segmentLength)} erhalten.")
    
    