from backend.capabilities.system.service import SystemService


system = SystemService()


tests = [
    ("system_info", {}),
    ("current_time", {}),
    ("battery", {}),
    ("get_volume", {}),
    ("get_brightness", {}),
    ("clipboard_set", {
        "text": "Hello from ZORA"
    }),
    ("clipboard_get", {}),
]


for action, params in tests:

    print("=" * 60)
    print(action)

    result = system.execute(action, params)

    print(result)