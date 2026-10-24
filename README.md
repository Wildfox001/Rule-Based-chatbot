# ChatBuddy: Rule-Based Chatbot

A beginner-friendly desktop chatbot built with Python and Tkinter for a CodeOrbit Tech AI Internship project. ChatBuddy has a polished chat window with message bubbles, a scrollable conversation, a send box, and a clear-chat button.

## Project structure

```text
Rule_Based_Chatbot/
├── chatbot.py   # Message matching rules and replies
├── main.py      # Tkinter interface
└── README.md    # Project guide
```

## What ChatBuddy can answer

The built-in rules cover greetings, help, its name, Python, AI, machine learning, Tkinter, programming, computers, the internet, a joke, thanks, and goodbye. It can also calculate simple two-number addition, subtraction, multiplication, and division. Examples include `python`, `What is AI?`, and `What is 7 plus 5?`.

ChatBuddy is an offline rule-based project. It cannot correctly answer every possible question or look up live facts. When a message does not match one of its rules, it says so and suggests topics it understands. A chatbot that answers open-ended questions needs a connected AI service and its own setup and credentials.

## Prerequisites

- Python 3.8 or newer
- Tkinter, included with most standard Python installations
- Visual Studio Code (recommended)

No external Python packages are required, so this project does not need a `requirements.txt` file.

## Run in VS Code

1. Open Visual Studio Code.
2. Choose **File → Open Folder...** and select the `Rule_Based_Chatbot` folder.
3. Choose **Terminal → New Terminal**.
4. Run:

   ```powershell
   python main.py
   ```

   If Windows does not recognize `python`, try:

   ```powershell
   py main.py
   ```

5. Type in the **Your message** box below the conversation. Press **Enter** or click **Send**.
6. Click **Clear chat** to start a fresh conversation.

If Python reports that Tkinter is unavailable, install Python from python.org with the **Tcl/Tk and IDLE** feature selected, then reopen VS Code.

## How the rules work

`main.py` passes each non-empty message to `get_response()` in `chatbot.py`. The chatbot trims extra spaces, checks an ordered list of case-insensitive word and phrase patterns, and returns the first matching reply. A separate safe calculation handler recognizes a small arithmetic expression without running user-provided code. If nothing matches, the chatbot returns a clear fallback response.

To add another response, add a pattern and reply to `RULES` in `chatbot.py`. Keep specific patterns before broader ones so a broad topic such as `Python` does not override a more specific rule.
