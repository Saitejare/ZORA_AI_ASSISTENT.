from typing import TypedDict, Dict, Any


class MCPRequest(TypedDict):

    capability: str
    action: str
    parameters: Dict[str, Any]


class MCPResponse(TypedDict):

    success: bool
    result: Any