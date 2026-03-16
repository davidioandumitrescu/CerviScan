import customtkinter as ctk
from PIL import Image


class ContactPage:
    def __init__(self, root, previous_page):
        self.root = root
        self.previous_page = previous_page
        self.logo_image = ctk.CTkImage(
            Image.open("assets/logo.png"), size=(104, 84)
        )
        self.email_image = ctk.CTkImage(
            Image.open("assets/email_logo.png"), size=(50, 35)
        )
        self.phone_image = ctk.CTkImage(
            Image.open("assets/phone_logo.png"), size=(50, 50)
        )

        self.create_contact_page()

    def create_contact_page(self):
        # Clear any existing elements
        for widget in self.root.winfo_children():
            widget.destroy()

        # Logo (top left corner)
        self.logo_label = ctk.CTkLabel(self.root, image=self.logo_image, text="")  # 143x115
        self.logo_label.place(relx=0, rely=0.01, anchor="nw")

        # Contact Information Text
        self.contact_label = ctk.CTkLabel(
            self.root,
            text="If you have any questions or problems,\nfeel free to contact us",
            font=("OpenSans", 32, "bold")
        )
        self.contact_label.place(relx=0.5, rely=0.2, anchor="center")

        # Phone Icon
        self.phone_image = ctk.CTkLabel(self.root, image=self.phone_image, text="")
        self.phone_image.place(relx=0.5, rely=0.38, anchor="center")

        # Phone Icon and Number
        self.phone_label = ctk.CTkLabel(self.root, text="0261 792", font=("OpenSans", 32,"bold"))
        self.phone_label.place(relx=0.5, rely=0.45, anchor="center")

        # Email Icon
        self.email_image = ctk.CTkLabel(self.root, image=self.email_image, text="")
        self.email_image.place(relx=0.5, rely=0.55, anchor="center")

        # Email Icon and Address
        self.email_label = ctk.CTkLabel(self.root, text="info@cerviscan.com", font=("OpenSans", 32,"bold"))
        self.email_label.place(relx=0.5, rely=0.60, anchor="center")

        # Back Button
        self.back_button = ctk.CTkButton(
            self.root, text="Back", command=self.go_back, width=120, height=40, fg_color="#FF69B4"
        )
        self.back_button.place(relx=0.02, rely=0.96, anchor="sw")

    def go_back(self):
        # Navigate back to the previous page
        self.previous_page(self.root)
