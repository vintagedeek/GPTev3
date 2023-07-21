# GPTev3 - Use GPT To Control ev3 And Complete Tasks
This project seeks to experiment with getting an ev3 to complete tasks without 
explicit programming using instructions from GPT via the OpenAI API. 

**NOTE**: Task: `task_follow_line_v2` seems to run without errors. Task 3 has errors.


# Approach
- Connect NetGear N150 wifi dongle to EV3.
- Run Flask API on same wifi network EV3 connected to.
- EV3 sends task and sensor reading to Flask API.
- Flask API hits OpenAI GPT API with task, sensor, readings, and function options.
- GPT selects the next function and function args.
- THe flask API passes the function and args to EV3, which executes the function.


# How To use

## Short Guide
See under the header First Time Using for more detailed instructions. Once everything is running,
you just need to change the `TASK` variable in the `.env` to whichever task you want the ev3
to complete (you can set tasks in the file `open_api_content.py`). Once that is all set, run
the flask API from your computer `ev3_robot_api.py` and then run `main.py` on the ev3. When adding
tasks to `open_api_content.py`, make sure to use the same task name in both `content_dict` and
`api_dict`. 


## First Time Using
- This project uses:
  - Lego Mindstorms EV3 (45544), Educator Vehicle build: http://robotsquare.com/2013/10/01/education-ev3-45544-instruction/
  - The EV3 MicroPython image
  - VS Code with the EV3 MicroPython extension
  - For more on VS Code and the EV3 MicroPython image, see https://pybricks.com/ev3-micropython/startinstall.html


- Run the following command to download the repository `git clone https://github.com/vintagedeek/GPTev3.git`


- Obtain OpenAI API key (you will be charged for API calls so monitor usage).


- Create the file `./.env` with the variables below. On windows call `ipconfig` in command prompt
  or PowerShell to get your IP address. In Linux you can use `ifconfig`.


```
OPENAI_API_KEY=<replace with your key>
PORT=<replace with your port>
IP_ADDRESS=<replace with your ip address>
TASK=<replace with a task listed under Supported Tasks in this README>
```

- When uploading this code to your ev3, the `./.env` file may not copy over. To address this, if you
  are using VS Code and the ev3 is connected you can right click the ev3 device under `EV3DEV Device Browser` and SSH into the ev3. From there you can change directories into `GPTev3` and create or
  copy in the `.env` file. **You may need to do this every time you change the `TASK` in the `./env`.**


- Connect your ev3 to the wifi network on which you will be running `ev3_robot_api.py`. To connect
  the ev3 to wifi you can use a Wifi dongle (e.g., NetGear N150 Wireless USB Adapter)


- Once the code is uploaded to the ev3, you can run `ev3_robot_api.py` to turn on the Flask API.
  Then navigate to `GPTev3` on the ev3 and select `main.py`. The ev3 will attempt to complete the
  task you entered for the variable `TASK` in the `./.env` file. 


- You can add tasks by adding them to the `content_dict` and `api_dict` in `./openai_api.content.py`.
  Make sure to use the same task name (key in the dicts) in both dictionaries. Currently `api_dict`
  gets information for a specific task via that task's key in `content_dict`. Considering moving
  this to a `json` file.


# Supported Tasks
The tasks are described in more detail in `./openai_api_content.py`. Feel free to tweak the messages
and functions as needed to accomplish your task. You may add new tasks to this file.


- **task_drive_forever**
  - This is effectively a test case to ensure that the ev3 is connected to the wifi network,
    posting requests to the Flask API in `ev3_robot_api.py`, and that the Flask API is 
    successfully getting a response from the OpenAI GPT API and communicating that response back
    to the ev3. 


- **task_follow_line**
  - Not working well.
  - GPT chooses functions that allow it to do line following on a track with a darker shade of tape
    on the left side of the track and a lighter shade of tape on the right side of the track.
  - Only method offered to GPT is DriverBase.drive()


- **task_follow_line_v2**
  - GPT chooses functions that allow it to do line following on a track with a darker shade of tape
    on the left side of the track and a lighter shade of tape on the right side of the track.
  - Only methods offered to GPT are DriverBase.straight() and DriverBase.turn().    


# Resources
- **Function Calling with OpenAI GPT API**: https://platform.openai.com/docs/guides/gpt/function-calling
- **PromptCraft Microsoft**: https://www.microsoft.com/en-us/research/uploads/prod/2023/02/ChatGPT___Robotics.pdf
  - Uses `temperature=0` for getting GPT to call functions: https://github.com/microsoft/PromptCraft-Robotics/blob/main/chatgpt_airsim/chatgpt_airsim.py


# FAQ

**I started `main.py` on the ev3 but the ev3 is not moving. The program isn't terminating (I see the arrow on the ev3's screen, but it doesn't move).**
- Make sure you are running `ev3_robot_api.py` on your computer before starting `main.py` on the ev3. Look for successful POST requests in the terminal.


- Ensure the ev3 is connected to the wifi network.


- Double check the ip address


**I changed the `TASK` variable in the `.env` file but the ev3 is still doing an old task.**
- The `.env` file may not copy over to the ev3 when you upload all of the code/files.
- To handle this in VS Code, connect ev3 to the computer via USB, find EV3Dev Device Browser
  on the bottom left side of the screen and connect the ev3.
- Once connected, right click the device and click to SSH into it.
- From there you can navigate to your program and manually copy the file over or just create the 
  `.env` manually using `vi .env`.


**GPT is not choosing functions or messing up the syntax**
- Per the docs, use models `gpt-3.5-turbo-0613` and `gpt-4-0613`. 
- These models were fine-tuned to determine when a function should be called.
- See **function calling**: https://platform.openai.com/docs/guides/gpt/function-calling