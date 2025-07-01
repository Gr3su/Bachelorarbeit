import numpy as np

class TimeSeriesSegments:
    def addSegment(self, segment):
        if not isinstance(segment, np.ndarray):
            raise TypeError(f"Erwarte ein NumPy-Array, aber ein {type(segment)} erhalten.")
        
        if len(segment) != self.segment_length:
            raise ValueError(f"Das Segment hat {len(segment)} Element(e), muss aber {self.segment_length} haben.")
        
        self.segments = np.append(self.segments, segment)
    
    def __init__(self, segments):
        if not isinstance(segments, list):
            raise TypeError(f"Erwarte eine Liste, aber ein {type(segments)} erhalten.")
        if not isinstance(segments[0], np.ndarray):
            raise TypeError(f"Erwarte ein NumPy-Array, aber ein {type(segments[0])} erhalten.")
        
        self.segments = np.array(segments[0])
        self.segment_length = len(segments[0])
        for i in range(1,len(segments)):
            self.addSegment(segments[i])

    