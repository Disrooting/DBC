import customtkinter as ctk


class Toolbar:

    def __init__(self, parent, on_connect_click=None, on_theme_toggle=None):

        self.on_connect_click = on_connect_click
        self.on_theme_toggle = on_theme_toggle

        self.frame = ctk.CTkFrame(
            parent,
            height=65,
            corner_radius=0,
            fg_color="#1e1f22"
        )

        self.frame.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="ew"
        )

        self.frame.grid_propagate(False)

        self.build()

    def build(self):

        left = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            padx=10
        )

        self.title = ctk.CTkLabel(
            left,
            text="\U0001F537 Discord Client",
            font=("Segoe UI",18,"bold")
        )

        self.title.pack(
            side="left"
        )

        self.status_dot = ctk.CTkLabel(
            left,
            text="\U0001F534",
            font=("Segoe UI", 12),
        )

        self.status_dot.pack(
            side="left",
            padx=(15, 3)
        )

        self.status = ctk.CTkLabel(
            left,
            text="Disconnected"
        )

        self.status.pack(
            side="left",
            padx=(0, 15)
        )

        right = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        right.pack(
            side="right",
            padx=10
        )

        self.connect_button = ctk.CTkButton(
            right,
            text="Connect",
            width=110,
            command=self._handle_connect_click,
        )

        self.connect_button.pack(
            side="right"
        )

        self.theme_button = ctk.CTkButton(
            right,
            text="\U0001F319",
            width=40,
            command=self._handle_theme_toggle,
            fg_color="transparent",
            border_width=1,
        )

        self.theme_button.pack(
            side="right",
            padx=(0, 10),
        )

    def _handle_connect_click(self):
        if self.on_connect_click:
            self.on_connect_click()

    def _handle_theme_toggle(self):
        if self.on_theme_toggle:
            self.on_theme_toggle()

    def set_status(self, text, state="disconnected"):
        """state: 'disconnected' | 'connecting' | 'connected'"""
        dots = {"disconnected": "\U0001F534", "connecting": "\U0001F7E1", "connected": "\U0001F7E2"}
        self.status_dot.configure(text=dots.get(state, "\U0001F534"))
        self.status.configure(text=text)

        if state == "connected":
            self.connect_button.configure(text="Disconnect")
        elif state == "connecting":
            self.connect_button.configure(text="Connecting...", state="disabled")
        else:
            self.connect_button.configure(text="Connect", state="normal")
