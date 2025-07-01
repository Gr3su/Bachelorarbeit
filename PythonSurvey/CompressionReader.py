import sys

from PythonSurvey.Utilities import TimeSeriesSegments as tss

def formatCheck(lines):
    if not lines:
        raise ValueError("Die Datei darf nicht leer sein.")
    for i in lines:
        if not i:
            raise ValueError("Die Datei darf keine Leerzeile enthalten.")
        if not isFloat(i):
            raise ValueError(f"Eine Zeile enthaelt keine Zahl, sondern folgendes: {i}")

def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    timeSeries = []
    for i in sys.argv:
        with open(i, "r") as f:
            lines = f.readlines()

        try:
            formatCheck(lines)
        except ValueError as e:
            print(e)
            break

        timeSeries.append([float(x) for x in lines])
    checkedTimeSeries = tss(timeSeries)

    for i in range(0,5):
        