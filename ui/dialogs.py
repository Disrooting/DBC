"""
=========================================================
 Discord Desktop Client V2
 dialogs.py

 Modal dialogs: token entry and simple message boxes.
=========================================================
"""

import customtkinter as ctk


class TokenDialog(ctk.CTkToplevel):
    """Modal dialog to collect a bot token. Blocks interaction with the
    main window until submitted or cancelled (grab_set), and reports the
    result back via an on_submit callback rather than a return value,
    since Tk dialogs are event-driven, not blocking calls."""

    def __init__(self, parent, on_submit, initial_value=""):
        super().__init__(parent)

        self.on_submit = on_submit

        self.title("Connect to Discord")
        self.geometry("420x220")
        self.resizable(False, False)

        # Keep this dialog on top and modal.
        self.transient(parent)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(
            self,
            text="Enter your bot token",
            font=("Segoe UI", 16, "bold"),
        )
        label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        sublabel = ctk.CTkLabel(
            self,
            text="This is stored locally in bot_config.json and never sent anywhere\n"
                 "except Discord's own API to connect your bot.",
            font=("Segoe UI", 11),
            text_color="#949BA4",
            justify="left",
        )
        sublabel.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="Bot token",
            show="•",
            width=380,
        )
        self.entry.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        if initial_value:
            self.entry.insert(0, initial_value)
        self.entry.bind("<Return>", lambda e: self._submit())

        self.error_label = ctk.CTkLabel(self, text="", text_color="#ED4245")
        self.error_label.grid(row=3, column=0, padx=20, pady=(0, 5), sticky="w")

        self.remember_var = ctk.BooleanVar(value=True)
        remember_check = ctk.CTkCheckBox(
            self, text="Remember this token", variable=self.remember_var
        )
        remember_check.grid(row=4, column=0, padx=20, pady=5, sticky="w")

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=5, column=0, padx=20, pady=15, sticky="ew")

        connect_btn = ctk.CTkButton(
            button_frame, text="Connect", command=self._submit, width=120
        )
        connect_btn.pack(side="right")

        cancel_btn = ctk.CTkButton(
            button_frame, text="Cancel", command=self.destroy,
            fg_color="transparent", border_width=1, width=120,
        )
        cancel_btn.pack(side="right", padx=(0, 10))

        self.entry.focus_set()

    def show_error(self, message):
        self.error_label.configure(text=message)

    def _submit(self):
        token = self.entry.get().strip()
        if not token:
            self.show_error("Enter a token first.")
            return
        remember = self.remember_var.get()
        self.destroy()
        self.on_submit(token, remember)


class MessageDialog(ctk.CTkToplevel):
    """Simple modal message box for errors/info -- used when connecting
    fails, since there's nowhere else in this app to surface that yet."""

    def __init__(self, parent, title, message, error=False):
        super().__init__(parent)

        self.title(title)
        self.geometry("360x160")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        icon = "❌" if error else "ℹ️"
        label = ctk.CTkLabel(
            self,
            text=f"{icon} {message}",
            font=("Segoe UI", 13),
            wraplength=320,
            justify="left",
        )
        label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)

        ok_btn = ctk.CTkButton(self, text="OK", command=self.destroy, width=100)
        ok_btn.grid(row=1, column=0, pady=(0, 20))
