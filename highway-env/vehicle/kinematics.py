import numpy as np
from collections import deque

class Vehicle:
    _collisions_enabled = True
    _length = 5.0
    _width = 2.0
    _default_speeds = [23, 25]
    _max_speed = 40

    def __init__(self, road, position, heading = 0, speed = 0):
        self.road = road
        self.position = np.array(position).astype('float')
        self.heading = heading
        self.speed = speed
        self.lane_index = self.road.network.get_closest_lane_index(self.position) if self.road else np.nan
        self.lane = self.road.network.get_lane(self.lane_index) if self.road else None
        self.action = {'steering': 0, 'acceleration': 0}
        self.crashed = False
        self.log = []
        self.history = deque(maxlen=30)

    @classmethod
    def make_on_lane(klass, road, lane_index, longitudinal, speed = 0):
        """
            Create a vehicle on a given lane at a longitudinal position.
        :param road: the road where the vehicle is driving
        :param lane_index: index of the lane where the vehicle is located
        :param longitudinal: longitudinal position along the lane
        :param speed: initial speed in [m/s]
        :return: A vehicle with at the specified position
        """
        lane = road.network.get_lane(lane_index)
        if speed is None:
            speed = lane.speed_limit
        return klass(road, lane.position(longitudinal, 0), lane.heading_at(longitudinal), speed)    

    def act(self, action = None):
        if action:
            self.action = action
    
    def step(self, dt):
        self.clip_actions()
        delta_f = self.action['steering']
        beta = np.arctan(1 / 2 * np.tan(delta_f))
        v = self.speed * np.array([np.cos(self.heading + beta),
                                   np.sin(self.heading + beta)])
        self.position += v * dt
        self.heading += self.speed * np.sin(beta) / (self.LENGTH / 2) * dt
        self.speed += self.action['acceleration'] * dt
        self.on_state_update()

    def clip_actions(self):
        if self.crashed:
            self.action['steering'] = 0
            self.action['acceleration'] = -1.0*self.speed
        self.action['steering'] = float(self.action['steering'])
        self.action['acceleration'] = float(self.action['acceleration'])
        if self.speed > self.MAX_SPEED:
            self.action['acceleration'] = min(self.action['acceleration'], 1.0 * (self.MAX_SPEED - self.speed))
        elif self.speed < -self.MAX_SPEED:
            self.action['acceleration'] = max(self.action['acceleration'], 1.0 * (self.MAX_SPEED - self.speed))
        
    def on_state_update(self):
        if self.road:
            self.lane_index = self.road.network.get_closest_lane_index(self.position)
            self.lane = self.road.network.get_lane(self.lane_index)
            if self.road.record_history:
                self.history.appendleft(self.create_from(self))