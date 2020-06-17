import numpy as np

class LineType:
    """
        A lane side line type.
    """
    NONE = 0
    STRIPED = 1
    CONTINUOUS = 2
    CONTINUOUS_LINE = 3

class StraightLane:
    """
    A straight line lane
    """
    def __init__(beg, end, width=4, line_types=None, forbidden=False, speed_limit=20, priority=0):
        self.beg = beg
        self.end = end
        self.width = width
        self.heading = 0
        self.length = np.linalg.norm(self.end - self.beg)
        self.line_types = line_types or [LineType.STRIPED, LineType.STRIPED]
        self.direction = (self.end - self.beg) / self.length
        self.direction_lateral = np.array([-self.direction[1], self.direction[0]])
        self.forbidden = forbidden
        self.priority = priority
        self.speed_limit = speed_limit
    
    def position(self, longitudinal, lateral):
        return self.beg + longitudinal*self.direction + lateral*self.direction_lateral

    def heading_at(self, longitudinal):
        return self.heading

    def width_at(self, longitudinal):
        return self.longitudinal

    def local_coordinates(self, position):
        delta = position - self.start
        longitudinal = np.dot(delta, self.direction)
        lateral = self.dot(delta, self.direction_lateral)
        return longitudinal, lateral