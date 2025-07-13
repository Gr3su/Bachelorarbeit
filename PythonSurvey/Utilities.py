import numpy as np

class MultivariateTimeSeries:
    def addTimeSeries(self, timeSeries):
        if not isinstance(timeSeries, list):
            raise TypeError(f"Erwarte eine List, aber ein {type(timeSeries)} erhalten.")
        
        if len(timeSeries) != self.timeSeriesLength:
            raise ValueError(f"Das Segment hat {len(timeSeries)} Element(e), muss aber {self.timeSeriesLength} haben.")
        
        self.multivariateTimeSeries.append(timeSeries)
    
    def __init__(self, timeSeries):
        if not isinstance(timeSeries, list):
            raise TypeError(f"Erwarte eine List, aber ein {type(timeSeries)} erhalten.")
        if not isinstance(timeSeries[0], list):
            raise TypeError(f"Erwarte eine List, aber ein {type(timeSeries[0])} erhalten.")
        
        self.multivariateTimeSeries = [timeSeries[0]]
        self.timeSeriesLength = len(timeSeries[0])
        for i in range(1,len(timeSeries)):
            self.addTimeSeries(timeSeries[i])