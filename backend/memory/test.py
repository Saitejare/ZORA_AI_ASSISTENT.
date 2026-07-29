from backend.memory.service import MemoryService

memory = MemoryService()

print("=" * 50)
print("Testing Intelligent Memory")
print("=" * 50)

test_messages = [
    "Hello",
    "Good morning",
    "My name is Sai Teja.",
    "I study Artificial Intelligence and Machine Learning at Lendi Institute of Engineering and Technology.",
    "My favourite programming language is Python.",
    "I use Visual Studio Code.",
    "Thank you.",
]

print("\nSaving memories...\n")

for message in test_messages:
    print(f"Input : {message}")
    memory.remember(message)
    print("-" * 50)

print("\nSearching...\n")

queries = [
    "What is my name?",
    "Which college do I study at?",
    "Which programming language do I like?",
    "Which editor do I use?",
]

for query in queries:
    print(f"Query : {query}")

    results = memory.recall(query)

    if not results:
        print("No memories found.")
    else:
        for item in results:
            print(f"  {item['text']}   ({item['score']:.3f})")

    print("-" * 50)