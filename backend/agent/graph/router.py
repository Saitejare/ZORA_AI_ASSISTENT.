from backend.agent.graph.state import AgentState


def should_continue(state: AgentState):
    if state.get("error"):
        return "response"

    return "context"