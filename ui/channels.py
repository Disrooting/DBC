import customtkinter as ctk


class ChannelPanel:

    def __init__(self,parent):

        self.frame = ctk.CTkScrollableFrame(

            parent,

            width=220

        )

        self.frame.grid(

            row=1,

            column=1,

            sticky="ns"

        )

    def clear(self):

        for w in self.frame.winfo_children():

            w.destroy()

    def add_channel(

        self,

        name,

        callback

    ):

        button = ctk.CTkButton(

            self.frame,

            text="# "+name,

            anchor="w",

            command=callback

        )

        button.pack(

            fill="x",

            padx=5,

            pady=2

        )