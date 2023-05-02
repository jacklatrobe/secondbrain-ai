## secondbrain: Second brain and theory of mind experiments with LLMs and LangChain
## File: app/human.py

from langchain.llms import OpenAI
import logging

def handle_query(query) -> str:
    return handle_response(input(query))

def handle_response(response) -> str:
    logging.info("Human Response: {}".format(response))
    return response