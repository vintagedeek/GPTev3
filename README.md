# GPT EV3
Goal: EV3 to complete tasks using instructions from GPT.


# Approach
- Connect NetGear N150 wifi dongle to EV3.
- Run Flask API on same wifi network EV3 connected to.
- EV3 sends task and sensor reading to Flask API.
- Flask API hits OpenAI GPT API with task, sensor, readings, and function options.
- GPT selects the next function and function args.
- THe flask API passes the function and args to EV3, which executes the function.


# How To use
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
  copy in the `.env` file.


- Connect your ev3 to the wifi network on which you will be running `ev3_robot_api.py`. To connect
  the ev3 to wifi you can use a Wifi dongle (e.g., NetGear N150 Wireless USB Adapter)


- Once the code is uploaded to the ev3, you can run `ev3_robot_api.py` to turn on the Flask API.
  Then navigate to `GPTev3` on the ev3 and select `main.py`. The ev3 will attempt to complete the
  task you entered for the variable `TASK` in the `./.env` file. 


# Supported Tasks
The tasks are described in more detail in `./openai_api_content.py`. Feel free to tweak the messages
and functions as needed to accomplish your task. You may add new tasks to this file.


- **task_drive_forever**
  - This is effectively a test case to ensure that the ev3 is connected to the wifi network,
    posting requests to the Flask API in `ev3_robot_api.py`, and that the Flask API is 
    successfully getting a response from the OpenAI GPT API and communicating that response back
    to the ev3. 


- **task_follow_line** (TODO!)
  - GPT chooses functions that allow it to do line following on a track with a darker shade of tape
    on the left side of the track and a lighter shade of tape on the right side of the track.
     
