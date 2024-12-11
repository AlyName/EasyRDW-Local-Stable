import numpy as np
import math
from tqdm import tqdm, trange
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class UserInfo:
    """
    The representation of the user (position, angle, velocity and angular velocity).
    x, y: m
    angle: rad
    v: m/frame
    w: rad/frame
    """
    def __init__(self, x, y, angle, v, w, meter_per_px = 1):
        self.x = x * meter_per_px
        self.y = y * meter_per_px
        self.angle = angle
        self.v = v * meter_per_px
        self.w = w

class Space:
    """
    The representation of the physical space.
    We consider it as a polygon space with polygonal obstacles obstacle_list.
    Additionally, we record the position of the user (user_x, user_y), its angle (user_angle) and velocity (user_v) and angular velocity (user_w).
    All lengths are in meters (m).
    """
    def __init__(self, border, raw_obstacle_list, meter_per_px = 1):
        self.border= [(t['x']*meter_per_px,t['y']*meter_per_px) for t in border]
        self.obstacle_list = []
        for raw_obstacle in raw_obstacle_list:
            obstacle = [(t['x']*meter_per_px,t['y']*meter_per_px) for t in raw_obstacle]
            self.add_obstacle(obstacle)
        
    def add_obstacle(self, obstacle):
        self.obstacle_list.append(obstacle)

    def in_obstacle(self, x, y):
        if not Polygon(self.border).contains(Point(x,y)):
            return True
        for obstacle in self.obstacle_list:
            polygon = Polygon(obstacle)
            if polygon.contains(Point(x,y)):
                return True
        return False