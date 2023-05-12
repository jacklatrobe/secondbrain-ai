from .confluence import SearchConfluenceTool, SaveConfluenceTool
from .human_prompts import HumanInputTool
# Import other tools as you add them
# from .tool_name import ToolNameFunction

tools = [
    SearchConfluenceTool,
    SaveConfluenceTool,
    HumanInputTool]

def tools():
    return tools

if __name__ == "__main__":
    tools()
