## secondbrain: Second brain and theory of mind experiments with LLMs and LangChain
## File: secondbrain_tools/telstra_website.py

import os
import re
import base64
import requests
import json
import logging
from bs4 import BeautifulSoup
from langchain import OpenAI
from langchain.agents import Tool

def search_telstra(query) -> str:
    # Set the base URL and the search query parameters
    base_url = f"https://tapi.telstra.com/presentation/v1/tcom/search/suggestions"
    params = {
        "query": "prepaid top up",
    }

    # Set the headers, including the encoded credentials for authorization
    headers = {
        "Accept": "application/json",
        "Accept-Language" : "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "source": "tcom"
    }

    # Make the GET request to the Confluence API
    response = requests.get(base_url, headers=headers, params=params)

    # Check if the request was successful (HTTP status code 200) and build YAML response obj
    if response.status_code == 200:
        print(response.json)
    else:
        logging.warn("Confluence search request failed with status code {response_code}".format(response_code=response.status_code))
        return "Request failed with status code {response_code}".format(response_code=response.status_code)


SearchTelstraTool = Tool(
    name = "Search Telstra.com.au",
    func = search_telstra,
    description="Useful for looking up plans, pricing or technical support information from the telstra public website"
)