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
    right_motor = Motor(Port.C)
    touch_sensor = TouchSensor(Port.S1)
    gyro_sensor = GyroSensor(Port.S2) 
    eyes = UltrasonicSensor(Port.S4) # measures distance with soundwaves
    color_sensor = ColorSensor(Port.S3)
    WHEEL_DIAMETER = 55.5 
    AXEL_TRACK = 110 # distance from center of left tire to center of right tire
    robot = DriveBase(
        left_motor, 
        right_motor, 
        wheel_diameter=WHEEL_DIAMETER, 
        axle_track=AXEL_TRACK
    )
    function_dict = {
        "drive_ev3": robot.drive,
        "drive_ev3_straight": robot.straight
    }

    model, messages, functions = get_model_messages_functions(
        task=task
    )    
    ev3.speaker.say("Getting instructions from GPT")
    while True:
        try:
            url = "http://{}:{}/ask".format(ip_address, port)
            data= {
                "task": task,
                "model": model,
                "messages": messages,
                "functions": functions
            }
            response = urequests.post(url, json=data)
            response_message = response.json()["choices"][0]["message"]
            gpt_selected_function, function_args = get_function_and_args(response_message)
            robot_action = function_dict[gpt_selected_function]
            robot_action(*function_args.values())
            kwarg_names = ", ".join(key for key in function_args.keys())
            kwarg_values = ", ".join(str(value) for value in function_args.values())
            color_sensor_reading = color_sensor.reflection()
            messages += [
                {
                    "role": "system",
                    "content": "To help the ev3 achieve the task called {}, I chose the function {} with keyword args {} whose values were {}, respectively.".format(task, gpt_selected_function, kwarg_names, kwarg_values)
                },
                {
                    "role": "user",
                    "content": "The ev3 called the function with the args you just provided. The color sensor returned {}. Now select a function and its args to help the ev3 complete the task called {}".format(color_sensor_reading, task)
                }
            ]
        except:
            write_logs(messages)


if __name__ == "__main__":
    # had to ssh into ev3 and manually copy in .env (wasn't copying over)
    env_vars = load_env('.env')
    IP_ADDRESS = env_vars["IP_ADDRESS"] 
    PORT = env_vars["PORT"]
    TASK = env_vars["TASK"]
    main(IP_ADDRESS, PORT, TASK)