import customtkinter as ctk
from PIL import Image
from frontend.pages.ContactPage import ContactPage
from frontend.pages.ScanMenuPage import ScanMenuPage


class WelcomePage:
    def __init__(self, root):
        self.help_button = None
        self.root = root
        self.logo_image = ctk.CTkImage(
            Image.open("assets/logo.png"), size=(281, 232)
        )
        self.question_mark_image = ctk.CTkImage(
            Image.open("assets/questionmark2.png"), size=(35, 35)
        )
        self.create_welcome_page()

    def create_welcome_page(self):
        # Clear any existing elements
        for widget in self.root.winfo_children():
            widget.destroy()

        # Help Button (top right corner) with custom image
        self.help_button = ctk.CTkButton(
            self.root,
            image=self.question_mark_image,
            text="",  # No text, just the image
            width=35,
            height=35,
            command=self.go_to_contact_page,
            fg_color="transparent",  # Optional: Make the button background transparent
            hover_color="#E0E0E0"  # Optional: Add a hover effect
        )
        self.help_button.place(relx=0.95, rely=0.05, anchor="ne")

        # Welcome Text
        self.welcome_label = ctk.CTkLabel(
            self.root, text="Welcome to CerviScan", font=("OpenSans", 32, "bold")
        )
        self.welcome_label.place(relx=0.5, rely=0.15, anchor="center")

        # Version Text
        self.version_label = ctk.CTkLabel(self.root, text="version no: 0.0.1", font=("Arial", 14))
        self.version_label.place(relx=0.5, rely=0.22, anchor="center")

        # Logo
        self.logo_label = ctk.CTkLabel(self.root, image=self.logo_image, text="")
        self.logo_label.place(relx=0.5, rely=0.4, anchor="center")

        # Continue Button
        self.continue_button = ctk.CTkButton(
            self.root, text="Continue", command=self.go_to_scan_setup_page, width=200, height=40, fg_color="#FF69B4"
        )
        self.continue_button.place(relx=0.5, rely=0.7, anchor="center")

    def go_to_scan_setup_page(self):
        # Navigate to Scan Setup Page
        ScanMenuPage(self.root)

    def go_to_contact_page(self):
        # Navigate to Contact Page
        ContactPage(self.root, previous_page=self.__class__)
