from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
import os

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def call_model(state):
    """The node that decides if we need a tool or a plain answer."""
    messages = state['messages']
    # We will bind tools to the model here in the next step
    response = llm.invoke(messages)
    return {"messages": [response]}

def execute_tools(state):
    """The node that actually runs the MCP server tools."""
    messages = state['messages']
    last_message = messages[-1]
    
    tool_outputs = []
    for tool_call in last_message.tool_calls:
        # Logic: This is where the Agent 'reaches out' to the MCP Server
        # For now, we return a placeholder to show the logic flow
        result = f"Successfully called {tool_call['name']}"
        tool_outputs.append(ToolMessage(tool_call_id=tool_call['id'], content=result))
    
    return {"messages": tool_outputs}