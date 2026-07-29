from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


# ==========================================================
# Request Types
# ==========================================================

class RequestType(str, Enum):
    CHAT = "chat"
    CAPABILITY = "capability"
    MEMORY = "memory"
    SYSTEM = "system"


# ==========================================================
# Execution Status
# ==========================================================

class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


# ==========================================================
# User Request
# ==========================================================

class UserRequest(BaseModel):
    text: str
    memory_context: str = ""


# ==========================================================
# Command
# ==========================================================

class Command(BaseModel):
    capability: str
    action: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# Execution Result
# ==========================================================

class ExecutionResult(BaseModel):
    status: ExecutionStatus
    message: str
    data: Optional[Any] = None


# ==========================================================
# Assistant Response
# ==========================================================

class AssistantResponse(BaseModel):
    success: bool
    response: str
    request_type: RequestType
    execution: Optional[ExecutionResult] = None