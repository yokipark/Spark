import customtkinter as ctk
import database  # <-- 1. Import our new database file

from pages.login import LoginPage
from pages.book_fund import MainPage
from pages.dashboard import DashboardPage
from pages.readers import ReaderPage

# 2. Run the initialization before the app starts
database.init_db() 

class LibraryApp(ctk.CTk):
# ... (Keep the rest of your main.py exactly the same)
    def __init__(self):
        super().__init__()

        self.title("Система Картотеки")
        self.geometry("1440x1024")
        
        # This container holds all the different pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Loop through classes and initialize them
        for PageClass in (LoginPage, MainPage, DashboardPage, ReaderPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # Stack all pages on top of each other in the same grid spot
            frame.grid(row=0, column=0, sticky="nsew")

        # Start with the login screen
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        """Bring a specific frame to the front"""
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
