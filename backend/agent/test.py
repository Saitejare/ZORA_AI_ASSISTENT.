from backend.agent.orchestrator import Orchestrator

o = Orchestrator()

print("Orchestrator Ready")

while True:

    command = input("\nYou: ")

    if command.lower() == "exit":
        break

    try:

        response = o.run(command)

        print("\nZORA:", response)

    except Exception as e:

        import traceback

        traceback.print_exc()