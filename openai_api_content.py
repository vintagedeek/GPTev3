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
    }
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
    }
}