import customtkinter as ctk
from tkinter import filedialog


class ChatPanel:

    def __init__(self, parent, on_send=None, on_attach=None):

        self.on_send = on_send
        self.on_attach = on_attach

        self.frame = ctk.CTkFrame(
            parent,
            corner_radius=0
        )

        self.frame.grid(
            row=1,
            column=2,
            sticky="nsew"
        )

        self.frame.grid_rowconfigure(
            1,
            weight=1
        )

        self.frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.build()

    def build(self):

        self.header = ctk.CTkLabel(

            self.frame,

            text="# General",

            font=("Segoe UI",18,"bold")

        )

        self.header.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            padx=20,
            pady=10
        )

        self.text = ctk.CTkTextbox(

            self.frame,

            wrap="word",

            undo=True,

            state="disabled",

        )

        self.text.grid(

            row=1,

            column=0,

            columnspan=3,

            sticky="nsew",

            padx=10,

            pady=10

        )

        self.attach_button = ctk.CTkButton(
            self.frame,
            text="\U0001F4CE",
            width=40,
            command=self._handle_attach,
        )
        self.attach_button.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(10, 0),
            pady=10,
        )

        self.input = ctk.CTkEntry(

            self.frame,

            placeholder_text="Type message..."

        )

        self.input.grid(

            row=2,

            column=1,

            sticky="ew",

            padx=5,

            pady=10

        )

        self.input.bind("<Return>", lambda e: self._handle_send())

        self.send_button = ctk.CTkButton(
            self.frame,
            text="Send",
            width=80,
            command=self._handle_send,
        )
        self.send_button.grid(
            row=2,
            column=2,
            sticky="e",
            padx=(0, 10),
            pady=10,
        )

    def _handle_send(self):
        content = self.input.get().strip()
        if not content:
            return
        self.input.delete(0, "end")
        if self.on_send:
            self.on_send(content)

    def _handle_attach(self):
        if not self.on_attach:
            return
        filepath = filedialog.askopenfilename(title="Select a file to send")
        if filepath:
            self.on_attach(filepath)

    def set_channel(self, name):
        self.header.configure(text=f"# {name}")

    def clear_messages(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")

    def add_message(self, author, content, timestamp=None, is_self=False):
        self.text.configure(state="normal")
        prefix = f"[{timestamp}] " if timestamp else ""
        who = f"{author} (you)" if is_self else author
        self.text.insert("end", f"{prefix}{who}: {content}\n")
        self.text.configure(state="disabled")
        self.text.see("end")

    def add_system_message(self, content):
        self.text.configure(state="normal")
        self.text.insert("end", f"* {content}\n")
        self.text.configure(state="disabled")
        self.text.see("end")
