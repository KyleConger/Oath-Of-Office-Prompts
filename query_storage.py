import os
from dotenv import load_dotenv
load_dotenv()

class ChatTree:
    IssueCreator = {
        "temperature": 1,
        "max_tokens": 4090,
        "system": open('systemprompt.txt').read(),
        # "example_input1": "Pentagon considers reducing submarine patrols",
        # "example_output1": open('example_output1.txt').read(),
        # "example_input2": "Navy plans expanded Arctic operations",
        # "example_output2": open('example_output2.txt').read(),
        # "example_input3": "Russia defies nuclear treaty restrictions",
        # "example_output3": open('example_output3.txt').read(),
        # "example_input4": "U.S. considers expanding federal land drilling",
        # "example_output4": open('example_output4.txt').read(),
        "prompt": None
    }
    # EffectedTopics = {
    #     "temperature": 0,
    #     "max_tokens": 500,
    #     "system": "Respond with only the words from the following list that are effected: Russia, Europe, Poor, Middle Class, Rich, Defense Industry, Financial Industry, Immigrants, Nationalists, Youth, Environmentalists, Resources Industry, China, The Commonwealth, Technology Industry, Native Americans, The Economy, Average Tax Rate, Global Stability, Military Strength, The Environment, Crime, Civil Rights, Inflation, Unemployment",
    #     "prompt": None
    # }
    ApprovedTopics = {
        "temperature": 0.9,
        "max_tokens": 500,
        "system": open('topicprompt.txt').read(),
        "prompt": None
    }
    
    WhoseIssue = {
        "temperature": 0.9,
        "max_tokens": 1000,
        "system": open('whoseissues.txt').read(),
        "prompt": None
    }

