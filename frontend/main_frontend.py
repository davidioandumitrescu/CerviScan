import customtkinter as ctk
from frontend.pages.WelcomePage import WelcomePage

# Initialize the CustomTkinter app
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class CerviScanApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("CerviScan")
        self.geometry("1000x800")
        self.resizable(True, True)

        self.configure(bg="white")

        # Load the Welcome Page
        WelcomePage(self)

if __name__ == "__main__":
    app = CerviScanApp()
    app.mainloop()
