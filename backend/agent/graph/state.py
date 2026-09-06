from typing import TypedDict, Annotated, Any
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    user_input: str
    messages: Annotated[list, add_messages]
    context: dict[str, Any]
    memory: list[str]
    command: dict[str, Any]
    selected_tool: str
    execution_result: dict[str, Any]
    reflection: dict[str, Any]
    response: str
    error: str | None