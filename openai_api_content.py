content_dict = {
    "task_drive_forever": {
        "sys_content": (
            "You are controlling an ev3 robot by choosing functions and their "
            "arguments based on input."
        ),
        "usr_content": (
            "The ev3 robot you are controlling has been placed in the middle of a "
            "room. You will use the ultrasonic sensor, which returns the distance "
            "to an object in mm, to navigate to the wall. The sensor outputs "
            "2000mm if nothing is in sight. The current ultrasonic sensor output "
            "is 2000mm. Choose a function and arguments for driving the robot "
            "toward the wall."            
        )
    },

    "task_follow_line": {
        "sys_content": (
            "You are controlling an ev3 robot by choosing functions and their "
            "arguments based on input. Your goal is to choose functions such "
            "that the ev3 follows a line using its color sensor."            
        ),
        "usr_content": (
            "You will be providing function calls to guide the ev3 robot you are "
            "controlling around a track. The track has blue tape on its left "
            "and white tape on the right. The color sensor returns a value of "
            "about 9 when over the blue tape and about 55 when over the white "
            "tape. The ev3 robot you are controlling has been placed in the "
            "middle of the track, so the sensor may be sensing some of the blue "
            "tape on the left and some of the white tape on the right. "
            "Use this information and the color sensor readings to guide the "
            "ev3 around the track until the human in the loop turns off the ev3."
        )
    },

    "task_follow_line_v2": {
        "sys_content": (
            "You are controlling an ev3 robot by choosing functions and their "
            "arguments based on input. Your goal is to choose functions such "
            "that the ev3 follows a line using its color sensor."            
        ),
        "usr_content": (
            "You will be providing function calls to guide the ev3 robot you are "
            "controlling around a track. The track has blue tape on its left "
            "and white tape on the right. The color sensor returns a value of "
            "about 9 when over the blue tape and about 55 when over the white "
            "tape. The ev3 robot you are controlling has been placed in the "
            "middle of the track, so the sensor may be sensing some of the blue "
            "tape on the left and some of the white tape on the right. "
            "Use this information and the color sensor readings to guide the "
            "ev3 around the track until the human in the loop turns off the ev3."
            "Note that it will take a few seconds for your instruction to reach "
            "the ev3, so be conservative with how fast and how far you move it."
            "I've noticed sometimes after giving a "
            "drive_straight_for_distance_then_stop instruction, you sometimes "
            "give an infinite series of turn_by_angle_then_stop instructions "
            "and the ev3 stops moving. For this task, if your last instruction "
            "was turn_by_angle_then_stop, then the next instruction must be "
            "drive_straight_for_distance_then_stop."
        )
    },

    "task_follow_line_v3": {
        "sys_content": (
            "You are controlling an ev3 robot by choosing functions and their "
            "arguments based on input. Your goal is to choose functions such "
            "that the ev3 follows a line using its color sensor."            
        ),
        "usr_content": (
            "You will be providing function calls to guide the ev3 robot you are "
            "controlling around a track using proportional line following. "
            "The track has blue tape on its left "
            "and white tape on the right. The color sensor returns a value of "
            "about 9 when over the blue tape and about 55 when over the white "
            "tape. The ev3 robot you are controlling has been placed in the "
            "middle of the track, so the sensor may be sensing some of the blue "
            "tape on the left and some of the white tape on the right. "
            "To accomplish the task of line following you will (1) remember the "
            "threshold value of 32 (the average of the intensities of the blue) "
            "and white tape); (2) you will compute a deviation, which is the "
            "threshold minus the color sensor reflection reading; "
            "(3) you will multiply the deviation by the PROPORTIONAL GAIN "
            "which we will set as 2.5; (4) the turn_rate you instruct the ev3 "
            "to use will be PROPORTIONAL GAIN * deviation. "
        )
    },
}

api_dict = {
    "task_drive_forever": {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system", 
                "content": content_dict["task_drive_forever"]["sys_content"]
            }, 
            {
                "role": "user", 
                "content": content_dict["task_drive_forever"]["usr_content"]
            }
        ],
        "functions": [
            {
                "name": "drive_ev3", 
                "description": "Move the ev3 forward at a particular speed and turn_rate.", 
                "parameters": {
                    "type": "object", 
                    "properties": {
                        "speed": {
                            "type": "integer", 
                            "description": "speed of the ev3 robot in mm/s"
                        }, 
                        "turn_rate": {
                            "type": "integer", 
                            "description": "turn rate of the ev3 robot in degrees per second"
                        }
                    }, 
                    "required": ["speed", "turn_rate"]
                }
            }
        ]
    },

    "task_follow_line": {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": content_dict["task_follow_line"]["sys_content"]}, 
            {"role": "user", "content": content_dict["task_follow_line"]["usr_content"]}
        ],
        "functions": [
            {
                "name": "drive_ev3", 
                "description": "Move the ev3 forward at a particular speed and turn_rate.", 
                "parameters": {
                    "type": "object", 
                    "properties": {
                        "speed": {
                            "type": "integer", 
                            "description": "speed of the ev3 robot in mm/s"
                        }, 
                        "turn_rate": {
                            "type": "integer", 
                            "description": "turn rate of the ev3 robot in degrees per second"
                        }
                    }, 
                    "required": ["speed", "turn_rate"]
                }
            }
        ]        
    },

    "task_follow_line_v2": {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": content_dict["task_follow_line_v2"]["sys_content"]}, 
            {"role": "user", "content": content_dict["task_follow_line_v2"]["usr_content"]}
        ],
        "functions": [
            {
                "name": "drive_straight_for_distance_then_stop", 
                "description": "Drives straight for a given distance in millimeters and then stops.", 
                "parameters": {
                    "type": "object", 
                    "properties": {
                        "distance": {
                            "type": "integer", 
                            "description": "Distance to travel in millimeters."
                        }
                    }, 
                    "required": ["distance"]
                }
            },
            {
                "name": "turn_by_angle_then_stop",
                "description": "Turns in place by a given angle in degrees and then stops. One full rotation corresponds to 360 degrees.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "angle": {
                            "type": "integer",
                            "description": "Angle to turn in degrees. One full rotation corresponds to 360 degrees."
                        }
                    },
                    "required": ["angle"]
                }
            }#,
            # {
            #     "name": "stop_ev3",
            #     "description": "Stops the robot by letting the motors spin freely.",
            #     "parameters": {
            #         "type": "object",
            #         "properties": {}
            #     }
            # }
        ]        
    },

    "task_follow_line_v3": {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": content_dict["task_follow_line_v3"]["sys_content"]}, 
            {"role": "user", "content": content_dict["task_follow_line_v3"]["usr_content"]}
        ],
        "functions": [
            {
                "name": "drive_ev3", 
                "description": "Move the ev3 forward at a particular speed and turn_rate.", 
                "parameters": {
                    "type": "object", 
                    "properties": {
                        "speed": {
                            "type": "integer", 
                            "description": "speed of the ev3 robot in mm/s"
                        }, 
                        "turn_rate": {
                            "type": "integer", 
                            "description": "turn rate of the ev3 robot in degrees per second"
                        }
                    }, 
                    "required": ["speed", "turn_rate"]
                }
            }
        ]        
    },
}