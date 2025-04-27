
import os
import requests
from typing import List
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langchain_core.tools import Tool
from langchain_core.messages import ToolMessage

# 设置 API Key
os.environ["XAI_API_KEY"] = "your-xai-api-key"

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
def search(query: str) -> str:
    return f"搜索结果：你搜索了 {query}"

tools = [
    Tool(
        name="search",
        func=search,
        description="用于搜索信息的工具"
    )
]

# 工具调用节点
def call_tool(state: AgentState) -> dict:
    last_message = state.messages[-1]
    if "搜索" in last_message:
        response = search(last_message)
        return {"messages": [response]}
    else:
        return {"messages": ["未调用工具，继续流程。"]}

# 决策节点
def should_continue(state: AgentState) -> str:
    last_message = state.messages[-1]
    if "搜索" in last_message:
        return "continue"
    else:
        return "end"

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
    initial_state = AgentState(messages=["搜索LangGraph的资料"])
    result = app.invoke(initial_state)
    print(result)
