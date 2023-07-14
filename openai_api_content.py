content_dict = {
    "task_drive_forever": {
        "sys_content": (
            "You are controlling a ev3 robot by choosing functions and their "
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
        "sys_content": (
            "You are controlling a ev3 robot by choosing functions and their "
            "arguments based on input."
        ),
        "usr_content": (
            "The ev3 robot you are controlling has been placed in the middle of a "
            "room. You will use the ultrasonic sensor, which returns the distance "
            "to an object in mm, to navigate to the wall. The sensor outputs "
            "2000mm if nothing is in sight. The current ultrasonic sensor output "
            "is 2000mm. Choose a function and arguments for driving the robot "
            "toward the wall."
        ),
        "messages": [
            {"role": "system", "content": "TO DO"}, 
            {"role": "user", "content": "TO DO"}
        ]        
    }
}