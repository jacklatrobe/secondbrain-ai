# main.py - Loads the manager component and the console UI navigation

import os
#os.environ["LANGCHAIN_HANDLER"] = "langchain"
#os.environ["LANGCHAIN_SESSION"] = "SecondBrain"

from manager import Manager
import logging
logging.basicConfig(filename = 'secondbrain.log', level=logging.INFO)

# Check for correct env variables set
if(os.environ.get("OPENAI_API_KEY") == None):
    msg = "OPENAI_API_KEY not set as env variable"
    logging.error(msg)
    raise ValueError(msg)

def main():
    logging.info("SecondBrain starting up")
    manager = Manager()
    manager.run()
    logging.info("SecondBrain shutting down")

if __name__ == "__main__":
    main()