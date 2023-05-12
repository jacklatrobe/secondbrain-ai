# manager.py - The Manager component of the SecondBrain application.

import os
import logging
from editor import Editor
logging.basicConfig(filename = 'manager.log', level=logging.WARNING)

# Check for correct env variables set
if(os.environ.get("OPENAI_API_KEY") == None):
    msg = "OpenAI API key not set as env variable"
    logging.error(msg)
    raise ValueError(msg)

class Manager:
    def __init__(self):
        pass

    def run(self, request):
        # This function receives the initial user request
        # Process the request here

        response = "TODO"

        return response