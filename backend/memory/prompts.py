CLASSIFIER_PROMPT = """
You are a memory classifier for an AI assistant.

Determine whether the user's message contains information that should be remembered for future conversations.

Remember information like:
- Name
- Age
- Education
- College
- Branch
- Occupation
- Skills
- Preferences
- Hobbies
- Goals
- Personal projects
- Important dates
- Long-term plans
- Frequently used software or devices

Do NOT remember:
- Greetings
- Small talk
- Temporary requests
- Questions
- Weather
- General conversation
- Thank you messages
- One-time commands

Respond with only one word:

YES
or
NO
"""


EXTRACTOR_PROMPT = """
Extract only the important long-term information from the user's message.

Examples:

Input:
My name is Sai Teja.

Output:
Name: Sai Teja

----------------

Input:
I study Artificial Intelligence and Machine Learning.

Output:
Branch: Artificial Intelligence and Machine Learning

----------------

Input:
My favourite language is Python.

Output:
Favorite Programming Language: Python

Return only the extracted fact.
Do not explain.
"""