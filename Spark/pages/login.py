import customtkinter as ctk
import localization
import os
from PIL import Image


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#4A6550")
        self.controller = controller

        # Настраиваем пути к папке assets
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(os.path.dirname(current_dir), "assets")

        self.main_card = ctk.CTkFrame(
            self,
            width=516,
            height=732,
            fg_color="#cfd2d0",
            corner_radius=20
        )
        self.main_card.place(relx=0.5, rely=0.5, anchor="center")

        # --- ЛОГОТИП (РАЗМЕЩЕН НАД ЗАГОЛОВКОМ) ---
        logo_path = os.path.join(self.assets_dir, "library_icon.png")
        try:
            pil_logo = Image.open(logo_path)
            # Делаем логотип покрупнее для экрана логина
            ctk_logo = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(90, 90))
            self.logo_label = ctk.CTkLabel(self.main_card, image=ctk_logo, text="")
            self.logo_label.place(x=258, y=100, anchor="center")
        except Exception:
            # Если картинка не найдется, покажем красивую заглушку-эмодзи
            self.logo_label = ctk.CTkLabel(self.main_card, text="📖", font=("Inter", 70), text_color="#304146")
            self.logo_label.place(x=258, y=100, anchor="center")

        self.title_label = ctk.CTkLabel(
            self.main_card,
            text=localization.get("app_title_1"),
            font=("Inter", 24),
            text_color="black"
        )
        self.title_label.place(x=258, y=190, anchor="center")

        self.subtitle = ctk.CTkLabel(
            self.main_card,
            text=localization.get("app_title_2"),
            font=("Inter", 24),
            text_color="black"
        )
        self.subtitle.place(x=258, y=220, anchor="center")

        # Error Label
        self.error_label = ctk.CTkLabel(
            self.main_card,
            text="",
            font=("Helvetica", 12, "bold"),
            text_color="#C13C3C"  # Red color for errors
        )
        self.error_label.place(x=258, y=265, anchor="center")

        # ID Entry
        self.idsotrudnika = ctk.CTkLabel(
            self.main_card,
            text=localization.get("ID сотрудника"),
            font=("Inter", 17),
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
            font=("Inter", 17),
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

        # 2. Check the credentials
        # (Идеально было бы использовать database.verify_login(user_id, password), но пока оставляем твой хардкод)
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
