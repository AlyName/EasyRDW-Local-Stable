import numpy as np
import math
from tqdm import tqdm, trange
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class UserInfo:
    """
    The representation of the user (position, angle, velocity and angular velocity).
    """
    def __init__(self, x, y, angle, v, w):
        self.x = x
        self.y = y
        self.angle = angle
        self.v = v
        self.w = w

class Space:
    """
    The representation of the physical space.
    We consider it as a polygon space with polygonal obstacles obstacle_list.
    Additionally, we record the position of the user (user_x, user_y), its angle (user_angle) and velocity (user_v) and angular velocity (user_w).
    """
    def __init__(self, border, raw_obstacle_list):
        self.border= [(t['x'],t['y']) for t in border]
        self.obstacle_list = []
        for raw_obstacle in raw_obstacle_list:
            obstacle = [(t['x'],t['y']) for t in raw_obstacle]
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