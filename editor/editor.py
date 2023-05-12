# editor.py - The Editor component of the SecondBrain application.

from langchain import OpenAI
from langchain.agents import Tool
from researcher import Researcher
import os
import logging
logging.basicConfig(filename = 'manager.log', level=logging.WARNING)

# Check for correct env variables set
if(os.environ.get("OPENAI_API_KEY") == None):
    msg = "OpenAI API key not set as env variable"
    logging.error(msg)
    raise ValueError(msg)

class Editor:
    def __init__(self, editor):
        self.editor = editor

    def run(query) -> None:
        # Initialize a single researcher
        researcher = Researcher()

        # Initialize editor agent
        llm = OpenAI(temperature=0, max_tokens=1000)
        tools = [
            Tool(
                name="Intermediate Answer",
                func=researcher,
                description="useful for when you need to ask with search"
            ),
        ]

        # Initialize a single researcher
        researcher = Researcher()
        response = researcher.run(query)

        print(response)
