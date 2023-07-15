from openai_api_content import api_dict
import ujson

def get_model_messages_functions(task):
    """
    Given an ev3 task, choose the pre-defined GPT model and the messages and
    functions to send to the GPT model. The GPT model will select the functions
    and function args based on the task and sensor readings.

    Parameters
    ----------
    task : str
        A task for the ev3 (e.g., "follow_line")
    
    Returns
    -------
    tuple[str, list, list]
        Element at index 0 is a str representing the GPT model.
        Element at index 1 is a list of messages for the GPT model.
        Element at index 2 is a list of functions for the GPT model to choose.
    """
    model = api_dict[task]["model"]
    messages = api_dict[task]["messages"]
    functions = api_dict[task]["functions"]
    return model, messages, functions


def get_function_and_args(response_message):
    """
    Returns the function and function arguments selected by GPT via the
    OpenAI Chat Completion API.

    Parameters
    ----------
    response_message : dict
        A dictionary that holds the GPT selected function and function args.
    
    Returns
    -------
    tuple[str, dict]
        A tuple whose 0th element is a string that represents the GPT-selected
        function. The 1st element is a dictionary whose keys are the selected
        functions parameters and whose values are GPT-selected args for those
        parameters.
    """
    gpt_selected_function = response_message["function_call"]["name"]
    function_args = ujson.loads(response_message["function_call"]["arguments"])
    return gpt_selected_function, function_args


def load_env(filename):
    """
    Get a dict of key=value pairs in a .env file.

    Parameters
    ----------
    filename : str
        Path to .env file.
    
    Returns
    -------
    dict
        A dict of key=value pairs in a .env file.
    """
    variables = {}
    with open(filename, "r") as file:
        for line in file.readlines():
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                variables[key] = value
    return variables


def write_logs(messages):
    """
    Write a log txt file that includes all messages sent between GPT and user.

    Parameters
    ----------
    messages : list
        A list of dicts where each dict identifies GPT (role = "system") versus
        the user (role = "user") and the message sent ("content").
    
    Returns
    None
    """
    with open("logs.txt", "w") as f:
        for dictionary in messages:
            for key, value in dictionary.items():
                f.write("{}: {}\n".format(key, value))
            f.write("\n")