# GPT EV3
Goal: EV3 to complete tasks using instructions from GPT.

# Approach
- Connect NetGear N150 wifi dongle to EV3.
- Run Flask API on same wifi network EV3 connected to.
- EV3 sends task and sensor reading to Flask API.
- Flask API hits OpenAI GPT API with task, sensor, readings, and function options.
- GPT selects the next function and function args.
- THe flask API passes the function and args to EV3, which executes the function.