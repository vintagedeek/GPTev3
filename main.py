#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import urequests
import utime
import ujson
from utils import (
    get_model_messages_functions, 
    get_function_and_args, 
    load_env,
    write_logs
)
# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

def main(ip_address, port, task):
    """
    Hit the ev3_robot_api Flask API with information that ev3_robot_api passes
    to the OpenAI GPT API. The information passed to ev3_robot_api should
    include a specific task and sensor readings relevant to the task.

    Parameters
    ----------
    ip_address : str
        The ip address of the server running ev3_robot_api.py 
        (e.g., "xxx.xxx.x.xxx").
    port : str
        The port being used to run ev3_robot_api.py at the provided ip_address.
    task : str
        A specific task for which GPT will select functions to help ev3
        complete it's task (e.g., "task_drive_forever"). The tasks are stored
        in the var api_dict in ./openai_api_content.py.
    
    Returns
    -------
    None
    """
    ev3 = EV3Brick()
    small_motor = Motor(Port.A) # for lifting/pushing
    left_motor = Motor(Port.B)
    left_motor.reset_angle(0)
    right_motor = Motor(Port.C)
    right_motor.reset_angle(0)
    touch_sensor = TouchSensor(Port.S1)
    gyro_sensor = GyroSensor(Port.S2)
    gyro_sensor.reset_angle(0) 
    ultra_sonic_sensor = UltrasonicSensor(Port.S4) # measures distance with soundwaves
    color_sensor = ColorSensor(Port.S3)
    WHEEL_DIAMETER = 55.5 
    AXEL_TRACK = 110 # distance from center of left tire to center of right tire
    robot = DriveBase(
        left_motor, 
        right_motor, 
        wheel_diameter=WHEEL_DIAMETER, 
        axle_track=AXEL_TRACK
    )
    # Values in function_dict are DriverBase methods called by GPT. The GPT API
    # call returns the str key in this dict used to call the corresonding method. 
    function_dict = {
        "drive_ev3": robot.drive,
        "drive_straight_for_distance_then_stop": robot.straight,
        "turn_by_angle_then_stop": robot.turn,
        "stop_ev3": robot.stop
    }

    model, messages, functions = get_model_messages_functions(
        task=task
    )
    logs = []    
    ev3.speaker.say("Getting instructions from GPT")
    response_logs = []
    while True:
        url = "http://{}:{}/ask".format(ip_address, port)
        data= {
            "task": task,
            "model": model,
            "messages": messages,
            "functions": functions
        }
        response = urequests.post(url, json=data) 
        response_dict = response.json()  
        response_logs.append(response_dict) 
        response_message = response.json()["choices"][0]["message"]
        if response_message.get("function_call"):
            gpt_selected_function, function_args = get_function_and_args(response_message)
            robot_action = function_dict[gpt_selected_function]
            robot_action(*function_args.values())
            kwarg_names = ", ".join(key for key in function_args.keys())
            kwarg_values = ", ".join(str(value) for value in function_args.values())
            color_sensor_reading = color_sensor.reflection()
            ultra_sonic_sensor_reading = ultra_sonic_sensor.distance()
            gyro_sensor_reading = gyro_sensor.angle()
            left_motor_angle = left_motor.angle()
            right_motor_angle = right_motor.angle()
            # TODO: these messages to openai_api_content.py (eventually json) and customize.
            # For function message, see "Function calling" at https://platform.openai.com/docs/guides/gpt/function-calling
            messages += [
                {
                    "role": "function",
                    "name": gpt_selected_function,
                    "content": "The ev3 called the function with the args you just provided. The color sensor returned {}. The ultrasonic sensor returned {} millimeters. The gyro sensor returned {} degrees. The left motor.angle() returned {} degrees and the right motor.angle() returned {} degrees. Now select a function and its args to help the ev3 complete the task called {}.".format(color_sensor_reading, ultra_sonic_sensor_reading, gyro_sensor_reading, left_motor_angle, right_motor_angle, task)
                }
            ]
        else:
            logs.append({"role": "ev3_robot_api", "content": "No function selected."})

        write_logs(messages, logs)
        with open("response_logs.json", "w") as f:
            ujson.dump(response_logs, f)
        wait(1200) # Reduce POST requests to OpenAI API
        

if __name__ == "__main__":
    # Had to ssh into ev3 and manually copy in .env (wasn't copying over)
    env_vars = load_env('.env')
    IP_ADDRESS = env_vars["IP_ADDRESS"] 
    PORT = env_vars["PORT"]
    TASK = env_vars["TASK"]
    main(IP_ADDRESS, PORT, TASK)