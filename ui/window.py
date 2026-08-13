import customtkinter as ctk

from core.constants import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class MainWindow:

    def __init__(self):

        self.root = ctk.CTk()

        self.root.title(APP_NAME)

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.root.minsize(1200, 600)

        self.root.grid_rowconfigure(1, weight=1)

        self.root.grid_columnconfigure(2, weight=1)

    def run(self):

        self.root.mainloop()