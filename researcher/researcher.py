# reseacher.py - The Reseacher component of the SecondBrain application.

import os
from langchain import OpenAI, LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.utilities import WikipediaAPIWrapper
from langchain.utilities import OpenWeatherMapAPIWrapper
from langchain.utilities import GoogleSerperAPIWrapper
from secondbrain_tools.confluence import SearchConfluenceTool, SaveConfluenceTool
import logging

# Check for correct env variables set
if(os.environ.get("SERPER_API_KEY") == None):
    msg = "SERPER_API_KEY not set as env variable"
    logging.error(msg)
    raise ValueError(msg)
if(os.environ.get("OPENWEATHERMAP_API_KEY") == None):
    msg = "OPENWEATHERMAP_API_KEY not set as env variable"
    logging.error(msg)
    raise ValueError(msg)

class Researcher:
    def __init__(self, name):
        self.name = name
        wikipedia = WikipediaAPIWrapper(top_k_results=2)
        googler = GoogleSerperAPIWrapper()
        weather = OpenWeatherMapAPIWrapper()
        llm = OpenAI(temperature=0)
        math_llm = LLMMathChain.from_llm(llm)
        conv_summary_llm = OpenAI(temperature=0.5, max_tokens=500)
        
        self.chat_llm = ChatOpenAI(temperature=0.4, max_tokens=200)
        self.chat_memory = ConversationSummaryMemory(llm=conv_summary_llm, memory_key="chat_history", return_messages=True)
        self.tools = [
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
            SearchConfluenceTool,
            SaveConfluenceTool,
            ## Additional tools here. Eg: Search Salesforce, Query JIRA, Interact with Pandas etc. etc.
        ]
        self.agent = initialize_agent(self.tools, self.chat_llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory=self.chat_memory)
    
    def run(self, query) -> str:
        return self.agent.run(query)