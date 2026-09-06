from backend.services.conversation_service import ConversationService

service = ConversationService()

state = {
    "user_input": "Hello ZORA"
}

result = service.process(state)

print(result)