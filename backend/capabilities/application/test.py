from backend.capabilities.application.service import ApplicationService

service = ApplicationService()

tests = [
    ("launch", {"target": "chrome"}),
    ("is_running", {"target": "chrome"}),
    ("activate", {"target": "chrome"}),
    ("minimize", {"target": "chrome"}),
    ("maximize", {"target": "chrome"}),
]

for action, params in tests:

    print("=" * 70)
    print(f"Action : {action}")
    print(service.execute(action, params))