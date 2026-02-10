import os
from typing import Annotated, TypedDict, Literal
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

from langchain_openai import ChatOpenAI
from mcp_server.src.server import mcp # Importing the MCP instance for direct tool binding

load_dotenv()

# 1. State Definition
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Setup Brain & Tools
llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = mcp.get_tools() # Automatically pulls tools from your MCP Server
llm_with_tools = llm.bind_tools(tools)

# 3. Nodes
def assistant(state: AgentState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# 4. Industrial Logic: Routing
def route_tools(state: AgentState) -> Literal["tools", "human_review", "__end__"]:
    msg = state["messages"][-1]
    if not msg.tool_calls:
        return "__end__"
    
    # HITL Logic: If placing an order, move to review instead of auto-executing
    for call in msg.tool_calls:
        if call["name"] == "place_secure_order":
            return "human_review"
    return "tools"

def human_review(state: AgentState):
    """This node acts as a break point for the UI to show a 'Confirm' button."""
    pass

# 5. Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("assistant", assistant)
workflow.add_node("tools", ToolNode(tools))
workflow.add_node("human_review", human_review)

workflow.add_edge(START, "assistant")
workflow.add_conditional_edges("assistant", route_tools)
workflow.add_edge("tools", "assistant")
workflow.add_edge("human_review", "tools") # Only moves to tools after human resumes

graph = workflow.compile(checkpointer=MemorySaver())