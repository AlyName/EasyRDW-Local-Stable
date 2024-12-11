import asyncio
import websockets
import json
# from client_logic import update_user, update_reset
from utils.constants import *
from utils.space import *
import math
import argparse
import importlib.util
import os
from utils.misc import calc_move_with_gain

import time

meter_per_px = 5/200

def import_function_from_file(file_name, function_name):
    if not os.path.exists(file_name):
        return None

    spec = importlib.util.spec_from_file_location("temp_module", file_name)
    if spec is None:
        return None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if function_name in dir(module):
        function = getattr(module, function_name)
        return function
    else:
        return None

file_s = ""
is_universal = False



async def user_loop(websocket, path):
    all_time = 0
    calc_time = 0
    nn=0
    r_time = time.time()
    calc_gain = None
    update_user = None
    update_reset = None
    if is_universal:
        update_user = import_function_from_file(file_s, "update_user")
        update_reset = import_function_from_file(file_s, "update_reset")
    else:
        calc_gain = import_function_from_file(file_s, "calc_gain")
        update_reset = import_function_from_file(file_s, "update_reset")
    
    while True:
        data = await websocket.recv()
        data = json.loads(data)
        print(data)
        if data["type"] == "start":
            physical_space = Space(data["physical"]["border"], data["physical"]["obstacle_list"], meter_per_px)
            message = json.dumps({"type": "start"})
            await websocket.send(message)
        elif data["type"] == "running":
            user = UserInfo(data["physical"]["user_x"], data["physical"]["user_y"], data["physical"]["user_direction"], data["user_v"], data["user_w"], meter_per_px)
            delta_t = data["delta_t"]
            need_reset = data["need_reset"]
            if need_reset:
                user = update_reset(user, physical_space, delta_t)
                message = json.dumps({"type": "running", "user_x": user.x / meter_per_px, "user_y": user.y / meter_per_px, "user_direction": user.angle, "reset": True})
            else:
                has_reset=False
                if is_universal:
                    user, has_reset = update_user(user, physical_space, delta_t)
                    message = json.dumps({"type": "running", "user_x": user.x / meter_per_px, "user_y": user.y / meter_per_px, "user_direction": user.angle, "reset": has_reset})
                else:
                    trans_gain, rot_gain, cur_gain_r, cur_direction = calc_gain(user, physical_space, delta_t)
                    message = json.dumps({"type": "running-gain", "trans_gain": trans_gain, "rot_gain": rot_gain, "cur_gain": cur_gain_r*(cur_direction)/abs(cur_direction), "reset": has_reset})

            n_time = time.time()
            await websocket.send(message)
            calc_time += time.time() - n_time
            nn+=1
            
        elif data["type"] == "end":
            message = json.dumps({"type": "end"})
            await websocket.send(message)
            all_time = time.time() - r_time
            print("All time: ", all_time, "Calc time: ", calc_time, "Calc time per frame: ", calc_time/nn)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--universal',help='Enable universal interface',default=False,action='store_true')
    parser.add_argument('-f','--file',default='controller/client_logic.py')
    args = parser.parse_args()

    file_s=args.file
    is_universal=args.universal
    start_server = websockets.serve(user_loop, "localhost", 8765)
    
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
