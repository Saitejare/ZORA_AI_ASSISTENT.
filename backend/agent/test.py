from backend.agent.orchestrator import Orchestrator

assistant = Orchestrator()

while True:

    query = input("\nYou: ")

    if query.lower() in ["exit", "quit"]:

        break

    reply = assistant.run(query)

    print("\nZORA:")
    print(reply)