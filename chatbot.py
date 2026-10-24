"""Intent matching and responses for the Rule-Based Chatbot."""

import re
from datetime import datetime


# Keep specific rules above broader rules. Patterns are case-insensitive, and
# word boundaries make short topics such as "AI" match as whole words.
RULES = [
    (
        re.compile(r"^(hi|hello|hey|good morning|good afternoon|good evening)\b", re.IGNORECASE),
        "Hello! What would you like to know?",
    ),
    (
        re.compile(r"\bhow are you\b|\bhow are u\b", re.IGNORECASE),
        "I'm doing well, thanks for asking! What can I help you with?",
    ),
    (
        re.compile(r"\b(what is your name|what's your name|who are you|what are you called)\b", re.IGNORECASE),
        "I'm ChatBuddy, a small offline chatbot made with Python. I answer using rules written in this project.",
    ),
    (
        re.compile(r"\b(what can you do|how can you help|help me|show me what you know)\b", re.IGNORECASE),
        "I can chat about Python, AI, machine learning, coding, Tkinter, and basic arithmetic. Try a question in one of those areas.",
    ),
    (
        re.compile(r"\b(what is ai|what's ai|define ai|explain ai|artificial intelligence)\b|\bai\b", re.IGNORECASE),
        "Artificial intelligence (AI) is a field of computing that builds systems able to perform tasks such as understanding language, recognizing patterns, and making predictions.",
    ),
    (
        re.compile(r"\b(machine learning|what is ml|what's ml|define ml)\b", re.IGNORECASE),
        "Machine learning is a part of AI. It lets a computer learn patterns from examples and use them to make predictions, instead of following only hand-written instructions.",
    ),
    (
        re.compile(r"\bpython\b", re.IGNORECASE),
        "Python is a popular, readable programming language used for automation, websites, data analysis, and AI. This chatbot itself is written in Python.",
    ),
    (
        re.compile(r"\b(tkinter|tk interface)\b", re.IGNORECASE),
        "Tkinter is Python's built-in toolkit for making desktop windows, buttons, text fields, and other graphical interface elements.",
    ),
    (
        re.compile(r"\b(rule[- ]based|chatbot|chat bot)\b", re.IGNORECASE),
        "A rule-based chatbot checks a message against predefined patterns and returns the reply attached to the first matching rule. It is predictable, but it cannot understand every possible question like a general AI model can.",
    ),
    (
        re.compile(r"\b(programming|coding|write code|code)\b", re.IGNORECASE),
        "Programming means writing instructions that a computer can follow. A good way to begin is to choose a small task, break it into steps, and practice with a language such as Python.",
    ),
    (
        re.compile(r"\b(computer|hardware|software)\b", re.IGNORECASE),
        "A computer is a device that follows instructions to process information. Hardware is its physical parts, while software is the programs it runs.",
    ),
    (
        re.compile(r"\b(internet|world wide web|www)\b", re.IGNORECASE),
        "The internet is a global network of connected devices. The web is one service on that network, where browsers open linked pages and applications.",
    ),
    (
        re.compile(r"\b(joke|make me laugh|something funny)\b", re.IGNORECASE),
        "Why did the programmer bring a ladder? Because the bug was on another level!",
    ),
    (
        re.compile(r"\b(thank you|thanks|thx)\b", re.IGNORECASE),
        "You're welcome! Feel free to ask another question.",
    ),
    (
        re.compile(r"\b(bye|goodbye|see you|see ya|farewell)\b", re.IGNORECASE),
        "Goodbye! Thanks for chatting with me.",
    ),
]


def _answer_arithmetic(message):
    """Answer a simple two-number calculation without evaluating user code."""
    expression = re.fullmatch(
        r"\s*(?:(?:what is|calculate|compute)\s+)?"
        r"(-?\d+(?:\.\d+)?)\s*"
        r"(\+|plus|-|minus|\*|x|times|multiplied by|/|divided by)\s*"
        r"(-?\d+(?:\.\d+)?)\s*[?.!]??\s*",
        message,
        re.IGNORECASE,
    )
    if not expression:
        return None

    left, operation, right = expression.groups()
    left, right = float(left), float(right)
    operation = operation.lower()
    if operation in ("+", "plus"):
        result = left + right
    elif operation in ("-", "minus"):
        result = left - right
    elif operation in ("*", "x", "times", "multiplied by"):
        result = left * right
    else:
        if right == 0:
            return "A number cannot be divided by zero."
        result = left / right

    if result.is_integer():
        result = int(result)
    return f"The answer is {result}."


def get_response(message):
    """Return the first rule-based reply matching a user's message."""
    if message is None:
        return "Please type a question or message first."

    text = str(message).strip()
    if not text:
        return "Please type a question or message first."

    arithmetic_reply = _answer_arithmetic(text)
    if arithmetic_reply is not None:
        return arithmetic_reply

    for pattern, response in RULES:
        if pattern.search(text):
            return response

    return (
        "I don't have a rule for that question yet. I can help with Python, AI, "
        "machine learning, coding, Tkinter, computers, or simple arithmetic."
    )
