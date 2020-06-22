import numpy as np

from highway_env.road.lane import LineType, StraightLane

class RoadNetwork:

    def __init__(self):
        self.graph = {}

    def add_lane(self, beg, end, lane):
        if beg not in self.graph:
            self.graph[beg] = {}
        if end not in self.graph[beg]:
            self.graph[beg][end] = []
        self.graph[beg][end].append(lane)

    @staticmethod
    def straight_road_network(lanes=4, length=10000, angle=0):
        rn = RoadNetwork()
        for lane in range(lanes):
            beg = np.array([0     , lane * StraightLane.DEFAULT_WIDTH])
            end = np.array([length, lane * StraightLane.DEFAULT_WIDTH])
            rot = np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]])
            rn.add_lane("0", "1", StraightLane(beg, end, line_types=line_types))
        return rn

class Road:
    
    def __init__(self, network, vehicles, recording=False):
        self.network = network
        self.vehicles = vehicles or []
        self.recording = recording

    def act(self):
        for v in self.vehicles:
            v.act()

    def step(self, dt):
        for v in self.vehicles:
            v.step(dt)

        # check collision between vehicles
        for v in self.vehicles:
            for o in self.vehicles:
                v.check_collision(o)