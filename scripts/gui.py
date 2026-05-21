import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import ttk
import logging


class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.set_window_settings()

        menubar = Menubar(self)

        self.config(menu=menubar)

    def set_window_settings(self) -> None:
        self.wm_title("Zundamon Twitch Reward TTS")

        self.geometry("350x500")
        self.resizable(width=False, height=True)
        self.minsize(width=350, height=100)
        self.maxsize(width=350, height=1000)

        self.option_add("*tearoff", False)


class Menubar(tk.Menu):
    def __init__(self, master: tk.Misc | None = None):
        super().__init__(master)

        # TODO: Make sure to apply actual commands
        self.add_command(label='接続設定', command='temp')
        self.add_command(label='NGワード', command='temp')


class ControlArea(tk.Frame):
    def __init__(self, master: tk.Misc | None = None):
        super().__init__(master)
        # TODO: Add "start/pause monitor" and "Clear audio storage" button


def __main__():
    root = Window()
    root.mainloop()


if __name__ == "__main__":
    __main__()