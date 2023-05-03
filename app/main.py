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
from bs4 import BeautifulSoup
import human_prompts
import os
import re
import base64
import requests

os.environ["LANGCHAIN_HANDLER"] = "langchain"

def main() -> None:
    wikipedia = WikipediaAPIWrapper(top_k_results=2)
    googler = GoogleSerperAPIWrapper()
    weather = OpenWeatherMapAPIWrapper()
    llm = OpenAI(temperature=0)
    math_llm = LLMMathChain(llm=llm)
    tools = [
        Tool(
            name="Web Search",
            func=googler.run,
            description="Useful for searching Google to look up answers to questions, or information about other websites. Input should be a search query."
        ),
        Tool(
            name="Encyclopedia Search",
            func=wikipedia.run,
            description="Useful for searching an encyclopedia for information about historical events, places or famous people. Input should be a simple search query."
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
            description="As a last resort, this tool allows you to ask the human a specific question when additional context is required to answer a query"
        ),
        Tool(
            name="Search the knowledgebase",
            func=search_confluence,
            description="Use this tool first every time. Searches the private knowledgebase for articles or previous writings. Input should be a simple search query."
        )
        ## Additional tools here. Eg: Search Salesforce, Query JIRA, Interact with Pandas etc. etc.
    ]

    chat_llm = ChatOpenAI(temperature=0.1, max_tokens=500)
    chat_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent_chain = initialize_agent(tools, chat_llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory=chat_memory)

    continue_conversation = True
    while continue_conversation:
        try:
            print(agent_chain.run(input=human_prompts.handle_query("Your query: ")))
        except Exception as ex:
            print("Conversation ended: {}".format(ex))

def search_confluence(query) -> str:
    # Replace these variables with your own values
    atlassian_email = os.environ.get("CONFLUENCE_CLIENT_ID")
    api_token = os.environ.get("CONFLUENCE_API_KEY")
    your_site_name = os.environ.get("CONFLUENCE_SITE_NAME")

    # Encode the email and API token in base64 format
    credentials = "{atlassian_email}:{api_token}".format(atlassian_email=atlassian_email, api_token=api_token)
    encoded_credentials = base64.b64encode(bytes(credentials, 'UTF-8')).decode()

    # Set the base URL and the search query parameters
    base_url = f"https://{your_site_name}.atlassian.net/wiki/rest/api"
    search_endpoint = "/search"
    params = {
        "limit": 2,
        "cql": "title ~ '{query}' or text ~ '{query}'".format(query=query),
        #"space": "SNB",
    }

    # Set the headers, including the encoded credentials for authorization
    headers = {
        "Accept": "application/json",
        "Authorization": "Basic {encoded_credentials}".format(encoded_credentials=encoded_credentials)
    }

    # Make the GET request to the Confluence API
    response = requests.get(base_url + search_endpoint, headers=headers, params=params)

    # Check if the request was successful (HTTP status code 200) and build YAML response obj
    if response.status_code == 200:
        results = response.json()
        return_str = "Search Results:\n"
        for result in results["results"]:
            if "content" in result:
                if result["content"]["type"] == "page":
                    title = result["content"]["title"]
                    page_url = result["content"]["_links"]["self"]
                    params = {"expand": "body.storage"}
                    page_request = requests.get(page_url, headers=headers, params=params)
                    body_html = page_request.json()["body"]["storage"]["value"]
                    re_obj = re.compile(r'<ac.*?/>')
                    body_html = re_obj.sub("", body_html)
                    body_text = BeautifulSoup(body_html, "html.parser")
                    body_text = "\n".join(body_text.text.split("\n"))
                    summary_llm = OpenAI()
                    body_text = summary_llm("Clean up then summarise this text: {}".format(body_text))
                    result_str = " - title: {title}\n   body_text: '{body_text}'\n".format(title=title, body_text=body_text)
                    return_str = "{}{}".format(return_str, result_str)
        return return_str
    else:
        return "Request failed with status code {response_code}".format(response_code=response.status_code)


if __name__ == "__main__":
    main()
    