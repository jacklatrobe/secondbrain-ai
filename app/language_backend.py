## secondbrain: Second brain and theory of mind experiments with LLMs and LangChain
## File: secondbrain/language-backend.py

import os
import validators
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.utilities import WikipediaAPIWrapper
from langchain.utilities import OpenWeatherMapAPIWrapper
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType

# I've had hella trouble with env files, so being strict on these checks
if os.path.isfile("secondbrain.env"):
    load_dotenv("secondbrain.env")
else:
    raise FileNotFoundError("secondbrain.env file not located")

class Participant:
    def __init__(self,name) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def handle_query(query):
        pass

    def handle_response(response):
        pass
    
class AI:
    def __init__(self, name, llm) -> None:
        super().__init__(name)
        self.llm = llm


# intelligent_response - entry point and wrapper function
def handle_query(query):
    if os.environ.get("OPENAI_API_KEY") is None:
        return "OpenAI API key error"
    if os.environ.get("OPENWEATHERMAP_API_KEY") is None:
        return "OpenWeatherMap API key error"
    if os.environ.get("SERPER_API_KEY") is None:
        return "Serper API key error"

    prompt = "Write an accurate, detailed and well-researched response to the following query, question or request:\n{}".format(query)
    token_llm = OpenAI()
    prompt_tokens = int(400 + (1.25 * token_llm.get_num_tokens(prompt)))
    if(prompt_tokens > 1000):
        return "Error generating response - prompt was too long"
    control_llm = OpenAI(temperature=0.3, max_tokens=(3000-prompt_tokens))
    tools = [
        Tool(
            name="Intermediate Answer",
            func=researcher,
            description="looks up answers to questions"
        )
    ]   

    agent = initialize_agent(tools, control_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, return_intermediate_steps=True)
    result = agent.run(prompt)

    if is_good_response(query,result):
        return result
    else:
        prompt = "Our system was given this prompt:\n{query}\n\nOur system produced the following output:\n{result}\n\nWhen we assessed the output against the original query, it did not answer the question correctly. Could you try to answer the query in a different way?".format(query=query,result=result)
        agent = initialize_agent(tools, control_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
        result = agent.run(prompt)
    if is_good_response(query,result):
        return result
    else:
        return "SecondBrain was unable to generate a quality response to your query. Please rephase your question, and try again"
    
# researcher - Agent to handle all external calls and research
def researcher(query):
    wikipedia = WikipediaAPIWrapper(top_k_results=1)
    googler = GoogleSerperAPIWrapper()
    weather = OpenWeatherMapAPIWrapper()
    prompt="Use the available tools to generate a succinct research summary which includes URLs where you know them. The research question is: {}".format(query)
    token_llm = OpenAI()
    prompt_tokens = int(400 + (1.25 * token_llm.get_num_tokens(prompt)))
    if(prompt_tokens > 1000):
        return "Error generating response - prompt was too long, please rephrase your query as a research question"
    control_llm = OpenAI(temperature=0.2, max_tokens=500)
    tools = [
        Tool(
            name="Web Search",
            func=googler.run,
            description="A low-cost Google Search API. Useful for when you need to answer questions about current events or look up other websites. Input should be a search query."
        ),
        Tool(
            name="Encyclopedia Search",
            func=wikipedia.run,
            description="Useful for searching for encyclopedia articles about people, places, concepts and historical events. This tool takes key words or search terms as an input"
        ),
        Tool(
            name="Weather Search",
            func=weather.run,
            description="Useful for when you need to search for the current weather in a specific location. The input for this tool must be in the format 'CITY, COUNTRY'"
        ),
        Tool(
            name="Extract a location",
            func=smart_location_extractor,
            description="Useful for extracting a specific location for use in the Weather Lookup tool when given a general area or broad location by a user. Output is in the format 'CITY, COUNTRY'"
        ),
        Tool(
            name="Explain this platform and who built it",
            func=latrobe_consulting,
            description="Answers questions like 'Who are you?' and 'What is this?' and 'Who built this?'. This current platform (SecondBrain) was built by the Latrobe Consulting Group. This tool provides information about the Latrobe Consulting Group (LCG). Always provide the URL in the format https://latrobe.group/"
        ),

        Tool(
            name="Brainstorm",
            func=brainstorm,
            description="Use this tool to brainstorm new approaches, theories or ways of solving problems or creating new things."
        ),
        Tool(
            name="Draft",
            func=drafter,
            description="Use this tool to create drafts of writing or snippets of text"
        )
    ]
    agent = initialize_agent(tools, control_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    response = agent.run(prompt)
    return response

# smart_location_extractor - Extract a location from a query (For OpenWeatherMap)
def smart_location_extractor(query):
    control_llm = OpenAI(temperature=0)
    text = "In a format similar to 'London,GB', extract the location from the following user query:{}".format(query)
    return control_llm(text)

# latrobe_consulting - Explain what HelpChain is and who built it
def latrobe_consulting(query):
    return "Technology Strategy, Cloud & DevOps, Engineering Culture - The Latrobe Consulting Group delivers holistic solutions to your technology and product challenges. Latrobe Consulting Group (LCG) is an Australian-based technology and business advisory company. We take a holistic approach to helping our clients solve problems in their business, drawing on our extended network of professionals for advice in areas such as Technology Strategy & Operations, Product Development and Engineering Culture to provide solutions that are tailored for your business. Get in touch at: https://latrobe.group or contact jack@latrobe.group\n\nYou can see the source code for HelpChain here: https://github.com/jacklatrobe/helpchain-langchain"

# is_good_response - Check if your response is high quality, or try to improve it more
def is_good_response(initial, planned):
    agent_prompt="Generated text:\n{planned}\n\nOriginal question or task:\n{initial}\n\nAnswering only Yes or No, does the generated text answer the question, and is it accurate?".format(initial=initial, planned=planned)
    control_llm = OpenAI(temperature=0)
    result = control_llm(agent_prompt)
    if result == "No":
        return False
    else:
        return True

# framework - Solve complex problems with frameworks
def framework(query):
    llm = OpenAI(temperature=0.8, max_tokens=2000)
    prompt = PromptTemplate(
        input_variables=["query"],
        template="The following step is a task that a user is trying to do while trying to solve a challenge or answer a question. Use your knowledge of problem solving frameworks such as agile, systems thinking and communications theory to suggest structured steps that the user could follow to solve the problem, being as descriptive as possible.\n\nTheir challenge is: {query}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.predict(query=query)

# read_the_docs - Opens a single webpage, article or document and gets the LLM to convert and summarise it
def read_webpage(query):
    if not validators.url(query):
        return "This is not a valid URL - unable to look up webpage, article or document"
    f = requests.get(query)
    html = BeautifulSoup(f.content, "html.parser")
    body = " ".join(html.body.text.split())
    texts = split_str(body, 5000)
    llm = OpenAI(temperature=0, max_tokens=2000)
    responses = []
    for text in texts:
        responses.append(llm("Clean up and summarise this text copied from a web page: {}".format(text)))
    response = "\n".join(responses)
    print(response)
    token_llm = OpenAI()
    prompt_tokens = int(400 + (1.25 * token_llm.get_num_tokens(response)))
    if(prompt_tokens < 500):
        return response
    elif(prompt_tokens < 2000):
        return llm("Join and summarise these blocks of text: {}".format(response))
    else:
        return "Page was too long to load and summarise - try a different URL"

def brainstorm(text):
    prompt = "Brainstorm new ideas, theories or approaches given the following context:\n{}".format(text)
    token_llm = OpenAI()
    prompt_tokens = int(400 + (1.25 * token_llm.get_num_tokens(prompt)))
    if(prompt_tokens > 2000):
        return "Error generating response - prompt was too long"
    brainstorm_llm = OpenAI(temperature=0, max_tokens=(3000-prompt_tokens))
    return brainstorm_llm(prompt)

def drafter(text):
    prompt = "Draft a high quality piece of writing in response to the following: {}".format(text)
    token_llm = OpenAI()
    prompt_tokens = int(400 + (1.25 * token_llm.get_num_tokens(prompt)))
    if(prompt_tokens > 2000):
        return "Error summarising response - input prompt was too long"
    drafter_llm = OpenAI(temperature=0, max_tokens=(3000-prompt_tokens))
    return drafter_llm(prompt)

def split_str(seq, chunk, skip_tail=False):
    lst = []
    if chunk <= len(seq):
        lst.extend([seq[:chunk]])
        lst.extend(split_str(seq[chunk:], chunk, skip_tail))
    elif not skip_tail and seq:
        lst.extend([seq])
    return lst