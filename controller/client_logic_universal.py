from utils.constants import *
from utils.space import *
import math
from utils.misc import calc_move_with_gain


def calc_gain(user, physical_space, delta):
    return 1, 1, MIN_CUR_GAIN_R, 1

def update_user(user : UserInfo, physical_space : Space, delta : float):
    """
    Return new UserInfo and whether a RESET has done.
    All lengths are in meters(m).
    user.v : m/frame.
    user.w : rad/frame.
    delta is the frame time interval in seconds. You might need it at some point.
    """
    trans_gain, rot_gain, cur_gain_r, rot_dir = calc_gain(user, physical_space, delta)
    new_user = calc_move_with_gain(user, trans_gain, rot_gain, cur_gain_r, rot_dir)
    if physical_space.in_obstacle(new_user.x, new_user.y):
        return update_reset(user, physical_space, delta), True
    return new_user, False

def update_reset(user, physical_space, delta):
    user.angle = ( user.angle + math.pi ) % (2 * math.pi)
    return user