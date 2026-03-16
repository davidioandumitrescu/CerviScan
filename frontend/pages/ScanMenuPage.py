import asyncio
import os
from datetime import datetime
from threading import Thread

import customtkinter as ctk
import numpy as np
from PIL import Image
import tkinter.filedialog as TinerFileDialog
from frontend.pages.ContactPage import ContactPage
from pathlib import Path
from frontend.model.UNETModel import iterate_over_images
class ScanMenuPage:
    def __init__(self, root):
        self.root = root
        self.logo_image = ctk.CTkImage(
            Image.open("assets/logo.png"), size=(104, 84)
        )
        self.browse_images_folder_button = None
        self.browse_result_folder_button = None
        self.scan_button = None
        self.loading_bar = None
        self.see_result_button = None
        self.browse_images_path_label = None
        self.browse_result_path_label = None
        self.see_result_lable = None
        self.question_mark_image = ctk.CTkImage(
            Image.open("assets/questionmark2.png"), size=(35, 35)
        )
        self.result=[]

        self.images_folder_path = ""
        self.result_folder_path = ""

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

        self.logo_label = ctk.CTkLabel(self.root, image=self.logo_image, text="")
        self.logo_label.place(relx=0, rely=0.01, anchor="nw")

        select_images_label = ctk.CTkLabel(
            self.root, text="Select the folder that contains the ct scans", font=("OpenSans", 18, "bold")
        )
        select_images_label.place(relx=0.1, rely=0.15, anchor="w")

        self.browse_images_folder_button = ctk.CTkButton(
            self.root, text="Browse", command=self.browse_images_folder, width=200, height=40, fg_color="#047D72"
        )
        self.browse_images_folder_button.place(relx=0.1, rely=0.2, anchor="w")

        select_path_label = ctk.CTkLabel(
            self.root, text="Selected Path: ", font=("OpenSans", 12)
        )
        self.browse_images_path_label = ctk.CTkLabel(
            self.root, text="No folder selected", font=("OpenSans", 12)
        )
        select_path_label.place(relx=0.1, rely=0.25, anchor="w")
        self.browse_images_path_label.place(relx=0.1, rely=0.3, anchor="w")

        select_result_folder_label = ctk.CTkLabel(
            self.root, text="Select the folder where the scanned ct scans will be placed", font=("OpenSans", 18, "bold")
        )
        select_result_folder_label.place(relx=0.1, rely=0.65, anchor="w")

        self.browse_result_folder_button = ctk.CTkButton(
            self.root, text="Browse", command=self.browse_result_folder, width=200, height=40, fg_color="#047D72"
        )
        self.browse_result_folder_button.place(relx=0.1, rely=0.7, anchor="w")

        select_result_path_label = ctk.CTkLabel(
            self.root, text="Selected Path: ", font=("OpenSans", 12)
        )
        self.browse_result_path_label = ctk.CTkLabel(
            self.root, text="No folder selected", font=("OpenSans", 12)
        )
        select_result_path_label.place(relx=0.1, rely=0.75, anchor="w")
        self.browse_result_path_label.place(relx=0.1, rely=0.8, anchor="w")

        self.scan_button = ctk.CTkButton(
            self.root, text="Start Scan", command=self.startScan, width=200, height=40, fg_color="#FF69B4", state='disabled'
        )
        self.scan_button.place(relx=0.85, rely=0.2, anchor="e")

        self.status_label = ctk.CTkLabel(
            self.root, text="Status: ", font=("OpenSans", 20,"bold")
        )
        self.status_label.place(relx=0.85, rely=0.40, anchor="e")
        self.loading_bar = ctk.CTkProgressBar(self.root, width=400, height=40, )
        self.loading_bar.set(0)
        self.loading_bar.place(relx=0.85, rely=0.45, anchor="e")


        self.see_result_button = ctk.CTkButton(
            self.root, text="See Result", command=self.see_result, width=200, height=40, fg_color="#FF69B4", state='disabled'
        )
        self.see_result_button.place(relx=0.85, rely=0.7, anchor="e")

        self.see_result_lable = ctk.CTkLabel(
            self.root, text="The scans are done.\nClick this to open the folder containing them.", font=("OpenSans", 18,"bold"),fg_color="transparent"
        )
        # Hide the label initially
        self.see_result_lable.place_forget()


    def browse_images_folder(self):
        selected_path = TinerFileDialog.askdirectory()
        if selected_path:
            self.images_folder_path = selected_path
            self.browse_images_path_label.configure(text=selected_path)
            if self.result_folder_path != "":
                self.scan_button.configure(state='normal')

    def browse_result_folder(self):
        selected_path = TinerFileDialog.askdirectory()
        if selected_path:
            self.result_folder_path = selected_path
            self.browse_result_path_label.configure(text=selected_path)
            if self.images_folder_path != "":
                self.scan_button.configure(state='normal')

    def startScan(self):
        thread=Thread(target=self.scan)
        thread.start()

    def scan(self):
        self.loading_bar.set(0)
        self.status_label.configure(text="Status: Scanning...")
        self.result=[]
        folder_path = Path(self.images_folder_path)
        extensions=[".jpg",".jpeg"]

        files = [f for f in folder_path.iterdir() if f.is_file() and extensions.__contains__(f.suffix)]
        result_images= iterate_over_images(files)

        for i in range(len(files)):
            image_array = result_images[i]

            # Ensure array is uint8 and within [0, 255]
            if image_array.dtype != np.uint8:
                image_array = (image_array * 255).astype(np.uint8)

            # Convert NumPy array to PIL Image
            image = Image.fromarray(image_array)

            # Save the image
            image.save(self.result_folder_path + "/" + files[i].name)
        self.loading_bar.set(100)
        self.status_label.configure(text="Status: Done!")
        self.see_result_button.configure(state='normal')

    def see_result(self):
        os.startfile(self.result_folder_path)

    def go_to_contact_page(self):
        # Navigate to Contact Page
        ContactPage(self.root, previous_page=self.__class__)