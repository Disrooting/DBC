import customtkinter as ctk

STATUS_COLORS = {
    "online": "#23A55A",
    "idle": "#F0B232",
    "dnd": "#F23F43",
    "offline": "#80848E",
}

STATUS_ORDER = {"online": 0, "idle": 1, "dnd": 2, "offline": 3}


class MemberPanel:

    def __init__(self, parent, image_loader=None):

        self.image_loader = image_loader

        self.frame = ctk.CTkScrollableFrame(

            parent,

            width=220

        )

        self.frame.grid(

            row=1,

            column=3,

            sticky="ns"

        )

    def clear(self):

        for widget in self.frame.winfo_children():

            widget.destroy()

    def add_member(
        self,
        name,
        bot=False,
        status="offline",
        avatar_url=None,
    ):

        row = ctk.CTkFrame(self.frame, fg_color="transparent")
        row.pack(fill="x", padx=5, pady=2)

        avatar_label = ctk.CTkLabel(row, text="\U0001F464", width=24)
        avatar_label.pack(side="left", padx=(0, 6))
        if self.image_loader and avatar_url:
            self.image_loader.load_async(
                avatar_url, lambda photo, lbl=avatar_label: lbl.configure(image=photo, text="")
            )

        dot = ctk.CTkLabel(
            row, text="\u25CF", text_color=STATUS_COLORS.get(status, STATUS_COLORS["offline"]), width=12
        )
        dot.pack(side="left")

        text = name
        if bot:
            text += " [BOT]"

        label = ctk.CTkLabel(
            row,
            text=text,
            anchor="w",
        )
        label.pack(side="left", padx=(4, 0), fill="x", expand=True)

    def add_members_sorted(self, members):
        """members: list of dicts with keys name, bot, status, avatar_url.
        Sorts by status priority (online > idle > dnd > offline), then name --
        the classic Discord member-list ordering."""
        ordered = sorted(
            members,
            key=lambda m: (STATUS_ORDER.get(m.get("status", "offline"), 3), m.get("name", "").lower()),
        )
        for m in ordered:
            self.add_member(
                m.get("name", "Unknown"),
                bot=m.get("bot", False),
                status=m.get("status", "offline"),
                avatar_url=m.get("avatar_url"),
            )
