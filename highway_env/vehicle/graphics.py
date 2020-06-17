import numpy as np
import pygame

#from highway_env.vehicle.dynamics import BicycleVehicle
from highway_env.vehicle.kinematics import Vehicle
#from highway_env.vehicle.behavior import IDMVehicle, LinearVehicle


class VehicleGraphics:
    _red = (255, 100, 100)
    _green = (50, 200, 0)
    _blue = (100, 200, 255)
    _yellow = (200, 200, 0)
    _black = (60, 60, 60)
    _purple = (200, 0, 150)
    _default_color = _yellow
    _ego_color = _green

    @classmethod
    def display(klass, vehicle, surface, transparent = False, offscreen = False, label = False):
        """
            Display a vehicle on a pygame surface.
            The vehicle is represented as a colored rotated rectangle.
        :param vehicle: the vehicle to be drawn
        :param surface: the surface to draw the vehicle on
        :param transparent: whether the vehicle should be drawn slightly transparent
        :param offscreen: whether the rendering should be done offscreen or not
        :param label: whether a text label should be rendered
        """
        v = vehicle
        tire_length, tire_width = 1, 0.3

        # Vehicle rectangle
        length = v._length + 2 * tire_length
        vehicle_surface = pygame.Surface((surface.pix(length), surface.pix(length)), pygame.SRCALPHA)  # per-pixel alpha
        rect = (surface.pix(tire_length), surface.pix(length / 2 - v.WIDTH / 2), surface.pix(v.LENGTH), surface.pix(v.WIDTH))
        pygame.draw.rect(vehicle_surface, klass.get_color(v, transparent), rect, 0)
        pygame.draw.rect(vehicle_surface, klass._black, rect, 1)

        # Tires
        if type(vehicle) in [Vehicle, BicycleVehicle]:
            tire_positions = [[surface.pix(tire_length), surface.pix(length / 2 - v.WIDTH / 2)],
                              [surface.pix(tire_length), surface.pix(length / 2 + v.WIDTH / 2)],
                              [surface.pix(length - tire_length), surface.pix(length / 2 - v.WIDTH / 2)],
                              [surface.pix(length - tire_length), surface.pix(length / 2 + v.WIDTH / 2)]]
            tire_angles = [0, 0, v.action["steering"], v.action["steering"]]
            for tire_position, tire_angle in zip(tire_positions, tire_angles):
                tire_surface = pygame.Surface((surface.pix(tire_length), surface.pix(tire_length)), pygame.SRCALPHA)
                rect = (0, surface.pix(tire_length/2-tire_width/2), surface.pix(tire_length), surface.pix(tire_width))
                pygame.draw.rect(tire_surface, cls.BLACK, rect, 0)
                cls.blit_rotate(vehicle_surface, tire_surface, tire_position, np.rad2deg(-tire_angle))

        # Centered rotation
        h = v.heading if abs(v.heading) > 2 * np.pi / 180 else 0
        position = [*surface.pos2pix(v.position[0], v.position[1])]
        if not offscreen:  # convert_alpha throws errors in offscreen mode TODO() Explain why
            vehicle_surface = pygame.Surface.convert_alpha(vehicle_surface)
        cls.blit_rotate(surface, vehicle_surface, position, np.rad2deg(-h))

        # Label
        if label:
            font = pygame.font.Font(None, 15)
            text = "#{}".format(id(v) % 1000)
            text = font.render(text, 1, (10, 10, 10), (255, 255, 255))
            surface.blit(text, position)