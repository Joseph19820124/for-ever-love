from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.agents import Tool
from tools import add_numbers, multiply_numbers
from schema import MathInput
from typing import TypedDict

class AgentState(TypedDict):
    input: str
    output: str

tools = [
    Tool.from_function(
        name="add_numbers",
        description="Adds two integers",
        func=lambda x: add_numbers(MathInput.parse_raw(x)),
    ),
    Tool.from_function(
        name="multiply_numbers",
        description="Multiplies two integers",
        func=lambda x: multiply_numbers(MathInput.parse_raw(x)),
    )
]

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

def agent_executor(state: AgentState) -> AgentState:
    user_input = state['input']
    response = llm.invoke(f"User said: {user_input}. Use a tool if needed.")
    return {"input": user_input, "output": response.content}

builder = StateGraph(AgentState)
builder.add_node("agent", agent_executor)
builder.set_entry_point("agent")
builder.add_edge("agent", END)
graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"input": '{"a": 2, "b": 3}'})
    print(result)
