#!/usr/bin/env python3
"""
Cat v1.x – A 2‑bit quantized language model demo (inspired by DeepSeek R1)
Minimal tkinter GUI (600x400) with simulated 2‑bit weights.
For educational purposes only – does not contain a real 2B parameter model.
"""

import tkinter as tk
from tkinter import scrolledtext, font
import random
import time
import threading

# -------------------- 2‑bit Toy Model (Cat v1.x) --------------------
class CatModel:
    """
    A playful 2‑bit quantized language model.
    Weights are stored as 2‑bit values (only -1, 0, 1, 2).
    The “model” generates responses based on a simple state machine.
    """
    def __init__(self):
        # Simulated 2‑bit weights (each -1, 0, 1, or 2)
        self.weights = {
            'greet':   [1, 0, 2, -1],
            'ask':     [0, 1, -1, 2],
            'answer':  [2, -1, 0, 1],
            'default': [1, 1, 0, 0]
        }
        # Tiny vocabulary of response parts
        self.phrases = [
            "Meow, I'm Cat v1.x, a 2‑bit neural network.",
            "I have only 2 bits per weight, so I'm very efficient.",
            "I'm quantized, therefore I am.",
            "The meaning of life? Probably catnip.",
            "I can't really think, but I pretend.",
            "Ask me something else, human.",
            "That's interesting! ... I think.",
            "I have 2 billion parameters? No, just 2 bits.",
            "Beep boop, 2‑bit processing... purr.",
            "Error: brain too small, but heart big.",
            "I'm just a demo, not a real LLM.",
        ]
        self.context = []  # conversation history

    def generate(self, prompt):
        """Return a simulated response based on prompt and internal state."""
        # Simulate processing delay
        time.sleep(0.5)

        # Simple keyword matching to pick a phrase category
        prompt_lower = prompt.lower()
        if any(word in prompt_lower for word in ['hello', 'hi', 'hey', 'meow']):
            idx = 0
        elif any(word in prompt_lower for word in ['what', 'who', 'why', 'how', '?']):
            idx = 1
        elif any(word in prompt_lower for word in ['bye', 'goodbye', 'exit']):
            idx = 2
        else:
            idx = 3

        # Mix in a little randomness based on “weights”
        weight_vec = self.weights.get(['greet','ask','answer','default'][idx], self.weights['default'])
        # Use weights to bias choice (very simplistic)
        bias = sum(weight_vec) % len(self.phrases)
        chosen = (idx + bias) % len(self.phrases)

        # Occasionally add a follow‑up from context
        response = self.phrases[chosen]
        if self.context and random.random() < 0.3:
            response += " " + random.choice(self.phrases)

        self.context.append(prompt)
        return response

# -------------------- GUI Application --------------------
class CatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cat v1.x – 2‑bit Quantized LLM")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Use a clean monospaced font
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=10)

        # Create the model instance
        self.model = CatModel()

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state='disabled',
            height=15, font=("Consolas", 10)
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = tk.Frame(root)
        input_frame.pack(padx=10, pady=(0,10), fill=tk.X)

        self.input_entry = tk.Entry(input_frame, font=("Consolas", 10))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            input_frame, text="Send", command=self.send_message,
            width=8
        )
        self.send_button.pack(side=tk.RIGHT, padx=(5,0))

        # Initial greeting
        self.display_message("System", "Cat v1.x loaded. Say meow!")

    def display_message(self, sender, message):
        """Insert a message into the chat display."""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')

    def send_message(self, event=None):
        """Handle user input and generate a response."""
        user_input = self.input_entry.get().strip()
        if not user_input:
            return

        self.display_message("You", user_input)
        self.input_entry.delete(0, tk.END)

        # Disable input while “thinking”
        self.input_entry.config(state='disabled')
        self.send_button.config(state='disabled')
        self.root.update()

        # Generate response in a separate thread to keep GUI responsive
        def respond():
            reply = self.model.generate(user_input)
            # Schedule the reply display on the main thread
            self.root.after(0, lambda: self.display_message("Cat", reply))
            self.root.after(0, lambda: self.input_entry.config(state='normal'))
            self.root.after(0, lambda: self.send_button.config(state='normal'))
            self.root.after(0, lambda: self.input_entry.focus())

        thread = threading.Thread(target=respond, daemon=True)
        thread.start()

# -------------------- Entry Point --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CatApp(root)
    root.mainloop()
