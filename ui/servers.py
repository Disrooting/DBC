import customtkinter as ctk


class ServerPanel:

    def __init__(self, parent, image_loader=None):

        self.image_loader = image_loader

        self.frame = ctk.CTkScrollableFrame(

            parent,

            width=240

        )

        self.frame.grid(

            row=1,

            column=0,

            sticky="ns"

        )

    def clear(self):

        for w in self.frame.winfo_children():

            w.destroy()

    def add_server(self, name, callback, icon_url=None):

        row = ctk.CTkFrame(self.frame, fg_color="transparent")
        row.pack(fill="x", padx=5, pady=2)

        icon_label = ctk.CTkLabel(row, text="\U0001F310", width=28)
        icon_label.pack(side="left", padx=(0, 4))
        if self.image_loader and icon_url:
            self.image_loader.load_async(
                icon_url, lambda photo, lbl=icon_label: lbl.configure(image=photo, text="")
            )

        button = ctk.CTkButton(

            row,

            text=name,

            command=callback,

            anchor="w"

        )

        button.pack(

            side="left",

            fill="x",

            expand=True,

        )
