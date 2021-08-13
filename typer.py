import tkinter as tk
from contextlib import contextmanager
from tkinter import ttk

import pydirectinput

NUM_ROW = "!@#$%^&*()_+"


def type_char(char: str):
    if char in NUM_ROW:
        char = str(NUM_ROW.index(char) + 1)
        with shift_key():
            pydirectinput.press(char)
    elif char.isupper():
        char = char.lower()
        with shift_key():
            pydirectinput.press(char)
    else:
        pydirectinput.press(char)


@contextmanager
def shift_key():
    try:
        pydirectinput.keyDown("shift")
        yield
    finally:
        pydirectinput.keyUp("shift")


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.entry_str = tk.StringVar()
        self.show_entry = tk.BooleanVar(value=False)
        self.delay = tk.StringVar(value=2)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.entry_label = ttk.Label(self, text="Enter text:")
        self.entry_label.grid(row=0, column=0, sticky=tk.W)

        self.entry = ttk.Entry(
            self,
            font="TkFixedFont",
            show="*",
            textvariable=self.entry_str,
        )
        self.entry.grid(row=0, column=1)
        self.entry_str.trace("w", self.validate)

        self.change_entry = ttk.Checkbutton(
            self,
            text="Show text",
            command=self.on_change_entry,
            variable=self.show_entry,
        )
        self.change_entry.grid(row=0, column=2)
        self.grid_rowconfigure(0, pad=20)
        self.delay_label = ttk.Label(self, text="Delay, sec:")
        self.delay_label.grid(row=1, column=0, sticky=tk.W)

        self.spinbox = ttk.Spinbox(
            self,
            from_=0,
            to=30,
            textvariable=self.delay,
            width=5,
        )
        self.spinbox.grid(row=1, column=1, sticky=tk.W)

        self.text_button = ttk.Button(
            self,
            text="Type text",
            command=self.on_type_text,
            state=tk.DISABLED,
        )
        self.text_button.grid(row=2, column=1, pady=10)

        self.statusbar = ttk.Label(
            self,
            text="Ready",
            border=0,
            relief=tk.SUNKEN,
        )
        self.statusbar.grid(row=3, columnspan=3, sticky=tk.EW)

    def validate(self, *args):
        state = tk.NORMAL if self.entry_str.get() else tk.DISABLED
        self.text_button.config(state=state)

    def on_change_entry(self):
        if self.show_entry.get():
            self.entry.config(show="")
        else:
            self.entry.config(show="*")

    def on_type_text(self):
        self.statusbar["text"] = "Waitng to focus switch..."
        self.text_button.config(state=tk.DISABLED)
        self.bind("<FocusOut>", self.wait_unfocus)

    def wait_unfocus(self, *args):
        delay = int(self.delay.get()) * 1000
        self.after(delay, self.type_chars)

    def type_chars(self, *args):
        text = self.entry_str.get()
        for idx, char in enumerate(text, start=1):
            type_char(char)
            self.statusbar["text"] = f"Typing {idx}/{len(text)}..."
            self.update_idletasks()
        self.unbind("<FocusOut>")
        self.statusbar["text"] = "Ready"
        self.text_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    master = tk.Tk()
    style = ttk.Style(master)
    style.theme_use("xpnative")
    master.resizable(False, False)
    master.title("Typer")
    app = Application(master)
    app.mainloop()
