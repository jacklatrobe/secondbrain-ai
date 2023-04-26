## secondbrain: Second brain and theory of mind experiments with LLMs and LangChain
## File: secondbrain/main.py

from datetime import datetime
import os
import sys

def main():
    if os.environ.get("OPENAI_API_KEY") is None:
        return "OpenAI API key error"
    if os.environ.get("OPENWEATHERMAP_API_KEY") is None:
        return "OpenWeatherMap API key error"
    if os.environ.get("SERPER_API_KEY") is None:
        return "Serper API key error"
    return 1

if __name__ == "__main__":
    main()