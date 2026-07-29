from backend.llm.service import LLMService
from backend.agent.validator import Validator
from backend.agent.executor import Executor
from backend.agent.response_generator import ResponseGenerator
from backend.agent.conversation_manager import ConversationManager


class Orchestrator:

    def __init__(self):
        self.llm = LLMService()
        self.validator = Validator()
        self.executor = Executor()
        self.response_generator = ResponseGenerator()
        self.conversation = ConversationManager()

    def run(self, user_input: str):

        # Store user message
        self.conversation.add_user_message(user_input)

        # Ask LLM for a command
        command = self.llm.generate_command(user_input)

        # Validate command
        self.validator.validate(command)

        # Execute command
        result = self.executor.execute(command)

        # Generate response
        response = self.response_generator.generate(result)

        # Store assistant response
        self.conversation.add_assistant_message(response)

        return response