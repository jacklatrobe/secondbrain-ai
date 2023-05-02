## secondbrain: Second brain and theory of mind experiments with LLMs and LangChain
## File: secondbrain/main.py

from langchain import OpenAI, LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.utilities import WikipediaAPIWrapper
from langchain.utilities import OpenWeatherMapAPIWrapper
from langchain.utilities import GoogleSerperAPIWrapper
import human_prompts
import os
os.environ["LANGCHAIN_HANDLER"] = "langchain"

def main():
    wikipedia = WikipediaAPIWrapper(top_k_results=2)
    googler = GoogleSerperAPIWrapper()
    weather = OpenWeatherMapAPIWrapper()
    llm = OpenAI(temperature=0)
    math_llm = LLMMathChain(llm=llm)
    tools = [
        Tool(
            name="Web Search",
            func=googler.run,
            description="A low-cost Google Search API. Useful for when you need to answer questions about current events or look up other websites. Input should be a search query."
        ),
        Tool(
            name="Encyclopedia Search",
            func=wikipedia.run,
            description="Useful for searching for encyclopedia articles about people, places, concepts and historical events. This tool takes key words or search terms as an input."
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
        Tool(
            name="Ask a human",
            func=human_prompts.handle_query,
            description="Useful for asking the human user questions or for any additional information about their query"
        )
    ]

    llm = ChatOpenAI(temperature=0.2, verbose=True, max_tokens=750)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

    continue_conversation = True
    while continue_conversation:
        try:
            print(agent_chain.run(input=human_prompts.handle_query("Query: ")))
        except Exception as ex:
            print("Conversation ended: {}".format(ex))

if __name__ == "__main__":
    main()
    