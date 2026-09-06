from backend.agent.conversation_manager import ConversationManager


class ConversationService:

    def __init__(self):
        self.manager = ConversationManager()

    def process(self, state):

        self.manager.add_user_message(
            state["user_input"]
        )

        state["messages"] = self.manager.get_history()

        return state