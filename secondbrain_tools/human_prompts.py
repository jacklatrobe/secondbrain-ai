## secondbrain: Second brain and theory of mind experiments with LLMs and LangChain
## File: app/human.py

from langchain.agents import Tool

def handle_query(query) -> str:
    return handle_response(input("{}\n> ".format(query)))

def handle_response(response) -> str:
    return response

def main(query) -> str:
    return handle_query(query)

HumanInputTool = Tool(
    name = "Ask a human",
    func = main,
    description="Useful for asking a human for additional information or direction when researching an answer."
)