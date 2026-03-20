import tkinter as tk
import tkinter.scrolledtext as st
import logging


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title = "Zundamon Twitch Reward TTS"

        self.geometry("350x500")
        self.resizable(False, True)
        self.minsize(350, 100)
        self.maxsize(350, 1000)

        self.option_add("*tearoff", False)

        menubar = Menubar(self)

        self.config(menu=menubar)


class Menubar(tk.Menu):
    def __init__(self, master: tk.Misc | None = None):
        super().__init__(master)

        configMenu = tk.Menu(master=self, tearoff=0)

        self.add_cascade(label="設定", menu = configMenu)
        # TODO: Associate action to config menu option


class ControlArea(tk.Frame):
    def __init__(self, master: tk.Misc | None = None):
        super().__init__(master)
        # TODO: Add "start/pause monitor" and "Clear audio storage" button


def __main__():
    root = Window()
    root.mainloop()


if __name__ == "__main__":
    __main__()