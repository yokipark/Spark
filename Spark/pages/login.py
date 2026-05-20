import customtkinter as ctk
import localization
class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        # FIXED: Changed "transparent" to the exact green color from your design
        super().__init__(parent, fg_color="#4A6550")
        self.controller = controller

        # Main card
        self.main_card = ctk.CTkFrame(
            self, 
            width=516, 
            height=732, 
            fg_color="#cfd2d0", 
            corner_radius=20
        )
        self.main_card.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_card,
            text="Картотека", 
            font=("Helvetica", 28, "bold"), 
            text_color="black"
        )
        self.title_label.place(x=258, y=190, anchor="center")

        self.subtitle = ctk.CTkLabel(
            self.main_card, 
            text="Библиотекаря", 
            font=("Helvetica", 16), 
            text_color="black"
        )
        self.subtitle.place(x=258, y=220, anchor="center")

        # --- NEW: Error Label (Hidden by default) ---
        self.error_label = ctk.CTkLabel(
            self.main_card, 
            text="", 
            font=("Helvetica", 12, "bold"), 
            text_color="#C13C3C" # Red color for errors
        )
        self.error_label.place(x=258, y=265, anchor="center")

        # ID Entry
        self.idsotrudnika = ctk.CTkLabel(
            self.main_card, 
            text=localization.get("ID сотрудника"), 
            font=("Helvetica", 12), 
            text_color="black"
        )
        self.idsotrudnika.place(x=68, y=300, anchor="w")

        self.id_entry = ctk.CTkEntry(
            self.main_card, 
            width=380, height=45, 
            fg_color="#bebebe", border_color="#bebebe", text_color="black", corner_radius=10
        )
        self.id_entry.place(x=258, y=335, anchor="center")

        # Password Entry
        self.pass_label = ctk.CTkLabel(
            self.main_card, 
            text=localization.get("Пароль"), 
            font=("Helvetica", 12), 
            text_color="black"
        )
        self.pass_label.place(x=68, y=390, anchor="w")

        self.pass_entry = ctk.CTkEntry(
            self.main_card, 
            width=380, height=45, 
            fg_color="#bebebe", border_color="#bebebe", text_color="black", corner_radius=10, 
            show="*"
        )
        self.pass_entry.place(x=258, y=425, anchor="center")

        # Login Button
        self.login_button = ctk.CTkButton(
            self.main_card, 
            text=localization.get("Login"), 
            width=360, height=50, 
            font=("Helvetica", 18, "bold"), 
            fg_color="#304146", hover_color="#1f2c30",
            text_color="white", corner_radius=15,
            command=self.login_action
        )
        self.login_button.place(x=258, y=550, anchor="center")

    def login_action(self):
        # 1. Grab the text the user typed
        user_id = self.id_entry.get()
        password = self.pass_entry.get()

        # 2. Check the credentials (Hardcoded for now)
        if user_id == "admin" and password == "1234":
            # SUCCESS!
            
            # Reset borders and error text in case they failed previously
            self.error_label.configure(text="")
            self.id_entry.configure(border_color="#bebebe", border_width=1)
            self.pass_entry.configure(border_color="#bebebe", border_width=1)
            
            # Clear the entry boxes so they are empty when you log out and come back
            self.id_entry.delete(0, 'end')
            self.pass_entry.delete(0, 'end')

            # Switch to Dashboard
            self.controller.show_frame("DashboardPage")
        else:
            # FAILED! Show error text and make borders red
            self.error_label.configure(text=localization.get("incorrect_password"))
            self.id_entry.configure(border_color="#C13C3C", border_width=2)
            self.pass_entry.configure(border_color="#C13C3C", border_width=2)
