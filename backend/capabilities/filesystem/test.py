from backend.capabilities.filesystem.service import FileSystemService


fs = FileSystemService()

tests = [
    ("create_folder", {"path": "AI"}),
    ("create_file", {"path": "AI/test.txt"}),
    ("write_file", {"path": "AI/test.txt", "content": "Hello ZORA"}),
    ("read_file", {"path": "AI/test.txt"}),
    ("append_file", {"path": "AI/test.txt", "content": "\nSecond Line"}),
    ("read_file", {"path": "AI/test.txt"}),
    ("list_folder", {"path": "AI"}),
    ("rename_file", {
        "source": "AI/test.txt",
        "destination": "AI/notes.txt"
    }),
    ("copy_file", {
        "source": "AI/notes.txt",
        "destination": "AI/copy.txt"
    }),
    ("search_file", {
        "root": ".",
        "filename": "notes"
    }),
]

for action, params in tests:

    print("=" * 60)
    print(action)

    result = fs.execute(action, params)

    print(result)