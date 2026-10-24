"""Professional, beginner-friendly Tkinter interface for ChatBuddy."""

import tkinter as tk
from tkinter import ttk

from chatbot import get_response


BACKGROUND = "#100B1F"
CHAT_BACKGROUND = "#100B1F"
PANEL = "#1A1230"
BUBBLE = "#261B3D"
TEXT = "#F8F5FF"
MUTED = "#B6AACD"
PURPLE = "#9333EA"
LAVENDER = "#C4B5FD"
CYAN = "#22D3EE"
SUCCESS = "#174A3A"
BORDER = "#37294F"
BUTTON_HOVER = "#7E22CE"


class ChatbotApp:
    """Build and manage the chatbot window and its message bubbles."""

    def __init__(self, root):
        self.root = root
        self.root.title("ChatBuddy | Rule-Based Chatbot")
        self.root.geometry("920x700")
        self.root.minsize(680, 520)
        self.root.configure(bg=BACKGROUND)
        self.bubble_labels = []

        self._configure_styles()
        self._build_layout()
        self._show_welcome()
        self.input_entry.focus_set()

    def _configure_styles(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Chat.TEntry",
            padding=(12, 11),
            fieldbackground=BUBBLE,
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            insertcolor=TEXT,
            selectbackground=PURPLE,
            selectforeground=TEXT,
        )
        style.map("Chat.TEntry", bordercolor=[("focus", PURPLE)])
        style.configure(
            "Chat.Vertical.TScrollbar",
            troughcolor=BACKGROUND,
            background=PANEL,
            bordercolor=BACKGROUND,
            arrowcolor=MUTED,
        )

    def _build_layout(self):
        accent_bar = tk.Frame(self.root, bg=PURPLE, height=4)
        accent_bar.pack(fill="x")
        accent_bar.pack_propagate(False)

        header = tk.Frame(self.root, bg=PANEL, padx=26, pady=18)
        header.pack(fill="x")

        title_area = tk.Frame(header, bg=PANEL)
        title_area.pack(side="left", fill="x", expand=True)
        tk.Label(
            title_area,
            text="ChatBuddy",
            font=("Segoe UI", 19, "bold"),
            fg=TEXT,
            bg=PANEL,
        ).pack(anchor="w")
        tk.Label(
            title_area,
            text="RULE-BASED CHAT ASSISTANT",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=PANEL,
        ).pack(anchor="w", pady=(2, 0))

        tk.Label(
            header,
            text="●  Offline demo",
            font=("Segoe UI", 9, "bold"),
            fg=CYAN,
            bg=SUCCESS,
            padx=12,
            pady=7,
        ).pack(side="left", padx=(12, 18))
        clear_button = tk.Button(
            header,
            text="Clear chat",
            command=self.clear_chat,
            font=("Segoe UI", 9, "bold"),
            fg=TEXT,
            bg=BUBBLE,
            activebackground="#3A2854",
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            padx=14,
            pady=9,
            cursor="hand2",
        )
        clear_button.pack(side="right")
        clear_button.bind("<Enter>", lambda _event: clear_button.configure(bg="#3A2854"))
        clear_button.bind("<Leave>", lambda _event: clear_button.configure(bg=BUBBLE))

        tk.Label(
            self.root,
            text="Ask about Python, AI, coding, or basic maths. This demo replies using rules stored in the project.",
            font=("Segoe UI", 10),
            fg=MUTED,
            bg=BACKGROUND,
            anchor="w",
            padx=24,
            pady=14,
        ).pack(fill="x")

        # Pack the input panel before the expanding conversation panel so it
        # always stays visible at the bottom of the window.
        self._build_composer()
        self._build_conversation()

    def _build_composer(self):
        composer = tk.Frame(self.root, bg=PANEL, padx=18, pady=14)
        composer.pack(side="bottom", fill="x", padx=18, pady=(0, 16))
        composer.configure(highlightbackground=BORDER, highlightthickness=1)

        tk.Label(
            composer,
            text="YOUR MESSAGE",
            font=("Segoe UI", 8, "bold"),
            fg=MUTED,
            bg=PANEL,
        ).pack(anchor="w", pady=(0, 7))

        input_row = tk.Frame(composer, bg=PANEL)
        input_row.pack(fill="x")
        self.input_entry = ttk.Entry(input_row, style="Chat.TEntry", font=("Segoe UI", 11))
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self._on_enter)

        self.send_button = tk.Button(
            input_row,
            text="Send",
            command=self.send_message,
            font=("Segoe UI", 10, "bold"),
            fg=TEXT,
            bg=PURPLE,
            activebackground=BUTTON_HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            padx=22,
            pady=11,
            cursor="hand2",
        )
        self.send_button.pack(side="right")
        self.send_button.bind("<Enter>", lambda _event: self.send_button.configure(bg=BUTTON_HOVER))
        self.send_button.bind("<Leave>", lambda _event: self.send_button.configure(bg=PURPLE))

        tk.Label(
            composer,
            text="Press Enter to send · Clear chat starts a fresh conversation",
            font=("Segoe UI", 8),
            fg=MUTED,
            bg=PANEL,
        ).pack(anchor="w", pady=(8, 0))

    def _build_conversation(self):
        panel = tk.Frame(self.root, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        self.chat_canvas = tk.Canvas(panel, bg=CHAT_BACKGROUND, highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(
            panel,
            orient="vertical",
            command=self.chat_canvas.yview,
            style="Chat.Vertical.TScrollbar",
        )
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.message_frame = tk.Frame(self.chat_canvas, bg=CHAT_BACKGROUND)
        self.canvas_window = self.chat_canvas.create_window(
            (0, 0), window=self.message_frame, anchor="nw"
        )
        self.message_frame.bind("<Configure>", self._update_scroll_region)
        self.chat_canvas.bind("<Configure>", self._resize_message_frame)

    def _resize_message_frame(self, event):
        self.chat_canvas.itemconfigure(self.canvas_window, width=event.width)
        wraplength = max(240, min(620, event.width - 150))
        for label in self.bubble_labels:
            label.configure(wraplength=wraplength)

    def _update_scroll_region(self, _event=None):
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))

    def _add_message(self, speaker, message, kind):
        """Add a left-aligned assistant bubble or a right-aligned user bubble."""
        row = tk.Frame(self.message_frame, bg=CHAT_BACKGROUND)
        row.pack(fill="x", padx=18, pady=8)

        if kind == "bot":
            avatar = tk.Label(
                row,
                text="CB",
                font=("Segoe UI", 8, "bold"),
                fg=LAVENDER,
                bg=SUCCESS,
                width=3,
                height=2,
            )
            avatar.grid(row=0, column=0, sticky="nw", padx=(0, 10))
            bubble = tk.Frame(row, bg=BUBBLE, padx=13, pady=10)
            bubble.configure(highlightbackground=BORDER, highlightthickness=1)
            bubble.grid(row=0, column=1, sticky="w")
            row.grid_columnconfigure(2, weight=1)
            label_color = LAVENDER
            justify = "left"
        else:
            row.grid_columnconfigure(0, weight=1)
            bubble = tk.Frame(row, bg=PANEL, padx=13, pady=10)
            bubble.configure(highlightbackground=CYAN, highlightthickness=1)
            bubble.grid(row=0, column=1, sticky="e")
            avatar = tk.Label(
                row,
                text="YOU",
                font=("Segoe UI", 8, "bold"),
                fg=CYAN,
                bg=CHAT_BACKGROUND,
                padx=10,
            )
            avatar.grid(row=0, column=2, sticky="ne", padx=(10, 0), pady=(5, 0))
            label_color = CYAN
            justify = "left"

        tk.Label(
            bubble,
            text=speaker.upper(),
            font=("Segoe UI", 8, "bold"),
            fg=label_color,
            bg=bubble.cget("bg"),
            anchor="w",
        ).pack(anchor="w", pady=(0, 4))

        message_label = tk.Label(
            bubble,
            text=message,
            font=("Segoe UI", 10),
            fg=TEXT,
            bg=bubble.cget("bg"),
            wraplength=max(240, min(620, self.chat_canvas.winfo_width() - 150)),
            justify=justify,
            anchor="w",
        )
        message_label.pack(anchor="w")
        self.bubble_labels.append(message_label)
        self.root.after_idle(self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        self._update_scroll_region()
        self.chat_canvas.yview_moveto(1.0)

    def _show_welcome(self):
        self._add_message(
            "ChatBuddy",
            "Hi! I'm ChatBuddy. Ask me about Python, AI, coding, or basic maths. "
            "For example: “What is Python?” or “What is 7 plus 5?”",
            "bot",
        )

    def _on_enter(self, _event):
        self.send_message()
        return "break"

    def send_message(self):
        """Ignore blank input, then show the user's text and the matching reply."""
        message = self.input_entry.get().strip()
        if not message:
            self.root.bell()
            return

        self._add_message("You", message, "user")
        self.input_entry.delete(0, "end")
        self._add_message("ChatBuddy", get_response(message), "bot")
        self.input_entry.focus_set()

    def clear_chat(self):
        """Remove visible messages and restore the welcome message."""
        for child in self.message_frame.winfo_children():
            child.destroy()
        self.bubble_labels.clear()
        self._show_welcome()
        self.input_entry.focus_set()


def main():
    root = tk.Tk()
    ChatbotApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
