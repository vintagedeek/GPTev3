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
    while True:
        try:
            url = "http://{}:{}/ask".format(ip_address, port)
            data= {
                "task": task,
                "model": model,
                "messages": messages,
                "functions": functions
            }
            robot.stop()
            response = urequests.post(url, json=data)
            response_message = response.json()["choices"][0]["message"]
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
            # To move these messages to openai_api_content.py and customize.
            messages += [
                {
                    "role": "assistant",
                    "content": "To help the ev3 achieve the task called {}, I chose the function {} with keyword args {} whose values were {}, respectively.".format(task, gpt_selected_function, kwarg_names, kwarg_values)
                },
                # {
                #     "role": "user",
                #     "content": "The ev3 called the function with the args you just provided. The color sensor returned {}. The ultrasonic sensor returned {} millimeters. The gyro sensor returned {} degrees. The left motor.angle() returned {} degrees and the right motor.angle() returned {} degrees. Now select a function and its args to help the ev3 complete the task called {}.".format(color_sensor_reading, ultra_sonic_sensor_reading, gyro_sensor_reading, left_motor_angle, right_motor_angle, task)
                # },
                {
                    "role": "user",
                    "content": "The ev3 called the function with the args you just provided. The color sensor returned {}. Now, compute the turn_rate, which is (32 - {}) * 2.5. Pass that value as the turn rate to ev3 to complete task {}. I recommend you pass a speed of 40.".format(color_sensor_reading, color_sensor_reading, task)                    
                }
            ]

        except:
            logs.append({"role": "ev3_robot_api", "content": "OpenAI API POST request failed."})
            write_logs(messages, logs)
            pass


if __name__ == "__main__":
    # had to ssh into ev3 and manually copy in .env (wasn't copying over)
    env_vars = load_env('.env')
    IP_ADDRESS = env_vars["IP_ADDRESS"] 
    PORT = env_vars["PORT"]
    TASK = env_vars["TASK"]
    main(IP_ADDRESS, PORT, TASK)