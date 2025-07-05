import numpy as np

class MultivariateTimeSeries:
    def addTimeSeries(self, timeSeries):
        if not isinstance(timeSeries, np.ndarray):
            raise TypeError(f"Erwarte ein NumPy-Array, aber ein {type(timeSeries)} erhalten.")
        
        if len(timeSeries) != self.timeSeries_length:
            raise ValueError(f"Das Segment hat {len(timeSeries)} Element(e), muss aber {self.timeSeries_length} haben.")
        
        self.multivariateTimeSeries = np.append(self.multivariateTimeSeries, timeSeries)
    
    def __init__(self, timeSeries):
        if not isinstance(timeSeries, list):
            raise TypeError(f"Erwarte eine List, aber ein {type(timeSeries)} erhalten.")
        if not isinstance(timeSeries[0], np.ndarray):
            raise TypeError(f"Erwarte ein NumPy-Array, aber ein {type(timeSeries[0])} erhalten.")
        
        self.multivariateTimeSeries = np.array(timeSeries[0])
        self.timeSeries_length = len(timeSeries[0])
        for i in range(1,len(timeSeries)):
            self.addTimeSeries(timeSeries[i])

class CompressedTimeSeries:
    class segmentContainer:
        def __init__(self, segment, originalLength):
            if not isinstance(segment, list):
                raise TypeError(f"Erwarte eine List, aber ein {type(segment)} erhalten.")
            if not isinstance(originalLength, int):
                raise TypeError(f"Erwarte ein int, aber ein {type(originalLength)} erhalten.")
            
            self.segment = segment
            self.originalLength = originalLength

    def __init__(self, segment, originalLength):
        self.segments = [CompressedTimeSeries.segmentContainer(segment, originalLength)]
    
    def addSegment(self, segment, originalLength):
        self.segments.append(CompressedTimeSeries.segmentContainer(segment, originalLength))