
import customtkinter as ctk

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        #Main card
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


        # ID Entry
        self.idsotrudnika = ctk.CTkLabel(
            self.main_card, 
            text="ID сотрудника", 
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
            text="Пароль", 
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
            text="ВОЙТИ", 
            width=360, height=50, 
            font=("Helvetica", 18, "bold"), 
            fg_color="#304146", hover_color="#1f2c30",
            text_color="white", corner_radius=15,
            command=self.login_action
        )
        self.login_button.place(x=258, y=550, anchor="center")

    def login_action(self):
        # Switch to MainPage when clicked
        self.controller.show_frame("DashboardPage")
