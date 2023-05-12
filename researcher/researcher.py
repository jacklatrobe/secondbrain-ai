# reseacher.py - The Reseacher component of the SecondBrain application.

from langchain import OpenAI, LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.utilities import WikipediaAPIWrapper
from langchain.utilities import OpenWeatherMapAPIWrapper
from langchain.utilities import GoogleSerperAPIWrapper
import os
import logging
logging.basicConfig(filename = 'manager.log', level=logging.WARNING)

# Check for correct env variables set
if(os.environ.get("OPENAI_API_KEY") == None):
    msg = "OpenAI API key not set as env variable"
    logging.error(msg)
    raise ValueError(msg)

def main() -> None:
    wikipedia = WikipediaAPIWrapper(top_k_results=2)
    googler = GoogleSerperAPIWrapper()
    weather = OpenWeatherMapAPIWrapper()
    llm = OpenAI(temperature=0.1, max_tokens=1000)
    math_llm = LLMMathChain.from_llm(llm)
    tools = [
        Tool(
            name="Web Search",
            func=googler.run,
            description="Useful for searching Google to look up information or answers to questions, or information about other websites. Input should be a search query."
        ),
        Tool(
            name="Encyclopedia Search",
            func=wikipedia.run,
            description="Useful for searching an encyclopedia for information about concepts, historical events, places or famous people. Input should be key words to search for."
        ),
        Tool(
            name="Weather Search",
            func=weather.run,
            description="Useful for when you need to search for the current weather in a specific location. The input for this tool must be in the format 'CITY, COUNTRY'."
        ),
        Tool(
            name="Calculator",
            func=math_llm.run,
            description="Useful for when you need to answer questions about math."
        ),
        confluence.SearchConfluenceTool,
        confluence.SaveConfluenceTool,
        ## Additional tools here. Eg: Search Salesforce, Query JIRA, Interact with Pandas etc. etc.
    ]

    chat_llm = ChatOpenAI(temperature=0.1, max_tokens=500, verbose=True)
    conv_summary_llm = OpenAI(max_tokens=500)
    chat_memory = ConversationSummaryMemory(llm=conv_summary_llm, memory_key="chat_history", return_messages=True)

    agent_chain = initialize_agent(tools, chat_llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory=chat_memory)

    continue_conversation = True
    while continue_conversation:
        try:
            print(agent_chain.run(input=human_prompts.handle_query("Your query: ")))
        except Exception as ex:
            print("Conversation ended: {}".format(ex))