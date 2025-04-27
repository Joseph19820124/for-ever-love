
import os
import requests
from typing import List
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage

# 设置 API Key
os.environ["XAI_API_KEY"] = "your_api_key_here"

# 定义状态模型
class AgentState(BaseModel):
    messages: List[str]

# 模型调用节点
def call_model(state: AgentState) -> dict:
    api_key = os.getenv("XAI_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "grok-3",
        "prompt": state.messages[-1],
        "max_tokens": 150,
        "temperature": 0.8
    }
    response = requests.post("https://api.x.ai/v1/completions", headers=headers, json=data)
    result = response.json()
    return {"messages": [result["choices"][0]["text"]]}

# 工具定义
@tool
def search(query: str) -> str:
    return "搜索结果：示例内容"

tools = [search]
tool_executor = ToolExecutor(tools)

# 工具调用节点
def call_tool(state: AgentState) -> dict:
    last_message = state.messages[-1]
    tool_call = last_message.tool_calls[0]
    action = {
        "tool": tool_call["name"],
        "tool_input": tool_call["args"],
    }
    response = tool_executor.invoke(action)
    tool_message = ToolMessage(
        content=str(response),
        name=action["tool"],
        tool_call_id=tool_call["id"]
    )
    return {"messages": [tool_message]}

# 决策节点
def should_continue(state: AgentState) -> str:
    last_message = state.messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

# 构建图
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"continue": "action", "end": END})
workflow.add_edge("action", "agent")
app = workflow.compile()

# 运行示例
if __name__ == "__main__":
    initial_state = AgentState(messages=["你好，世界！"])
    result = app.invoke(initial_state)
    print(result)
