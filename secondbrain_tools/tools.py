from .confluence import SearchConfluenceTool, SaveConfluenceTool
from .human_prompts import HumanInputTool
# Import other tools as you add them
# from .tool_name import ToolNameFunction

class SecondBrainTools:
    tools = [
        SearchConfluenceTool,
        SaveConfluenceTool,
        HumanInputTool]
