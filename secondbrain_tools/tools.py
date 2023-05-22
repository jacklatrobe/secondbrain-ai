## secondbrain: Second brain and theory of mind experiments with LLMs and LangChain
## File: secondbrain_tools/main.py


from .confluence import SearchConfluenceTool, SaveConfluenceTool
from .human_prompts import HumanInputTool
# Import other tools as you add them
# from .tool_name import ToolNameFunction

class SecondBrainTools:
    tools = [
        SearchConfluenceTool,
        SaveConfluenceTool,
        HumanInputTool]
