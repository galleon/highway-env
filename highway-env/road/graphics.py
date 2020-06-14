import numpy as np
import pygame

from highway_env.road.lane import LineType
from highway_env.road.road import Road
from highway_env.vehicle.graphics import VehicleGraphics


class WorldSurface(pygame.Surface):
    _initial_scaling = 5.5
    _initial_centering = [0.5, 0.5]
    _scaling_factor = 1.3
    _moving_factor = 0.1

    def __init__(self, size, flags, surf):
        super().__init__(size, flags, surf)
        self.origin = np.array([0, 0])
        self.scaling = self._initial_scaling
        self.centering_position = self._initial_centering

    def pix(self, length):
        return int(length * self.scaling)

    def pos2pix(self, x, y):
        return self.pix(x - self.origin[0]), self.pix(y - self.origin[1])

    def vec2pix(self, vec):
        return self.pos2pix(vec[0], vec[1])

    def move_display_window_to(self, position):
        self.origin = position -np.array(
            [self.centering_position[0] * self.get_width()  / self.scaling,
             self.centering_position[1] * self.get_height() / self.scaling]
        )

    def handle_event(self, event):
        if event.type = pygame.KEYDOWN:
            if event.key == pygame.K_l:
                self.scaling *= 1 / self._scaling_factor
            if event.key == pygame.K_o:
                self.scaling *= self._scaling_factor            
            if event.key == pygame.K_m:
                self.centering_position[0] -= self._moving_factor
            if event.key == pygame.K_k:
                self.centering_position[0] += self._moving_factor

class LaneGraphics:
    _stripe_spacing = 5
    _stripe_length = 3
    _stripe_width = 0.3

    @classmethod
    def display(klass, lane, surface):
        stripes_count = int(2 * (surface.get_height() + surface.get_width()) / (klass._stripe_spacing * surface.scaling))
        s_origin, _ = lane.local_coordinates(surface.origin)
        s0 = (int(s_origin) // klass._stripe_spacing - stripes_count // 2) * klass._stripe_spacing
        for side in range(2):
            if lane.line_types[side] == LineType.STRIPED:
                klass.striped_line(lane, surface, stripes_count, s0, side)
            elif lane.line_types[side] == LineType.CONTINUOUS:
                klass.continuous_curve(lane, surface, stripes_count, s0, side)
            elif lane.line_types[side] == LineType.CONTINUOUS_LINE:
                klass.continuous_line(lane, surface, stripes_count, s0, side)

    @classmethod
    def striped_line(klass, lane, surface, stripes_count, longitudinal, side):
        """
            Draw a striped line on one side of a lane, on a surface.
        :param lane: the lane
        :param surface: the pygame surface
        :param stripes_count: the number of stripes to draw
        :param longitudinal: the longitudinal position of the first stripe [m]
        :param side: which side of the road to draw [0:left, 1:right]
        """
        starts = longitudinal + np.arange(stripes_count) * klass._stripe_spacing
        ends = longitudinal + np.arange(stripes_count) * klass._stripe_spacing + klass._stripe_length
        lats = [(side - 0.5) * lane.width_at(s) for s in starts]
        klass.draw_stripes(lane, surface, starts, ends, lats)


    @classmethod
    def continuous_line(klass, lane, surface, stripes_count, longitudinal, side):
        """
            Draw a continuous line on one side of a lane, on a surface.
        :param lane: the lane
        :param surface: the pygame surface
        :param stripes_count: the number of stripes that would be drawn if the line was striped
        :param longitudinal: the longitudinal position of the start of the line [m]
        :param side: which side of the road to draw [0:left, 1:right]
        """
        starts = [longitudinal + 0 * klass._stripe_spacing]
        ends = [longitudinal + stripes_count * klass._stripe_spacing + klass._stripe_length]
        lats = [(side - 0.5) * lane.width_at(s) for s in starts]
        klass.draw_stripes(lane, surface, starts, ends, lats)

    @classmethod
    def draw_stripes(klass, lane, surface, starts, ends, lats):
        """
            Draw a set of stripes along a lane.
        :param lane: the lane
        :param surface: the surface to draw on
        :param starts: a list of starting longitudinal positions for each stripe [m]
        :param ends: a list of ending longitudinal positions for each stripe [m]
        :param lats: a list of lateral positions for each stripe [m]
        """
        starts = np.clip(starts, 0, lane.length)
        ends = np.clip(ends, 0, lane.length)
        for k in range(len(starts)):
            if abs(starts[k] - ends[k]) > 0.5 * klass._stripe_length:
                pygame.draw.line(surface, surface.WHITE,
                                 (surface.vec2pix(lane.position(starts[k], lats[k]))),
                                 (surface.vec2pix(lane.position(ends[k], lats[k]))),
                                 max(surface.pix(klass.STRIPE_WIDTH), 1))

    @classmethod
    def draw_ground(klass, lane, surface, color, width, draw_surface = None):
        draw_surface = draw_surface or surface
        stripes_count = int(2 * (surface.get_height() + surface.get_width()) / (klass._stripe_spacing * surface.scaling))
        s_origin, _ = lane.local_coordinates(surface.origin)
        s0 = (int(s_origin) // klass._stripe_spacing - stripes_count // 2) * klass._stripe_spacing
        dots = []
        for side in range(2):
            longis = np.clip(s0 + np.arange(stripes_count) * klass._stripe_spacing, 0, lane.length)
            lats = [2 * (side - 0.5) * width for _ in longis]
            new_dots = [surface.vec2pix(lane.position(longi, lat)) for longi, lat in zip(longis, lats)]
            new_dots = reversed(new_dots) if side else new_dots
            dots.extend(new_dots)
        pygame.draw.polygon(draw_surface, color, dots, 0)


class RoadGraphics:
    """
        A visualization of a road lanes and vehicles.
    """
    @staticmethod
    def display(road, surface):
        """
            Display the road lanes on a surface.
        :param road: the road to be displayed
        :param surface: the pygame surface
        """
        surface.fill(surface.GREY)
        for _from in road.network.graph.keys():
            for _to in road.network.graph[_from].keys():
                for l in road.network.graph[_from][_to]:
                    LaneGraphics.display(l, surface)

    @staticmethod
    def display_traffic(road, surface, simulation_frequency = 15, offscreen = False):
        """
            Display the road vehicles on a surface.
        :param road: the road to be displayed
        :param surface: the pygame surface
        :param simulation_frequency: simulation frequency
        :param offscreen: render without displaying on a screen
        """
        if road.record_history:
            for v in road.vehicles:
                VehicleGraphics.display_history(v, surface, simulation=simulation_frequency, offscreen=offscreen)
        for v in road.vehicles:
            VehicleGraphics.display(v, surface, offscreen=offscreen)