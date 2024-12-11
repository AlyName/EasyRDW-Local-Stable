from utils.constants import *
from utils.space import *
import math

def calc_gain(user : UserInfo, physical_space : Space, delta : float):
    """
    Return three gains and the direction (+1 or -1) when cur_gain used. Implement your own logic here.
    All lengths are in meters(m).
    user.v : m/frame.
    user.w : rad/frame.
    delta is the frame time interval in seconds. You might need it at some point.
    """
    return MAX_TRANS_GAIN, MAX_ROT_GAIN, INF_CUR_GAIN_R, 1

def update_reset(user : UserInfo, physical_space : Space, delta : float):
    """
    Return new UserInfo when RESET. Implement your RESET logic here.
    """
    user.angle = ( user.angle + math.pi ) % (2 * math.pi)
    return user
