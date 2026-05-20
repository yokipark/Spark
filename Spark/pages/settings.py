import customtkinter as ctk
import database
import localization # Подключаем наш словарь!

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

        # ==========================================
        # SIDEBAR (Широкий дизайн 370px + Spark Logo)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=370, corner_radius=0, fg_color="#4A6550")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.sidebar_inner = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_inner.pack(fill="both", expand=True, padx=32, pady=(50, 25))

        self.logo_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.logo_zone.pack(side="top", fill="x", pady=(0, 40)) # 40px gap below the logo
        
        ctk.CTkLabel(self.logo_zone, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(anchor="w")
        ctk.CTkLabel(self.logo_zone, text="библиотекаря", font=("Helvetica", 14), text_color="#E6C619").pack(anchor="w")

        self.nav_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.nav_zone.pack(side="top", fill="x")

        # ИСПОЛЬЗУЕМ ПЕРЕВОДЫ ДЛЯ КНОПОК!
        self.create_nav_btn(localization.get("main"), command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn(localization.get("settings"), is_active=True, command=lambda: controller.show_frame("SettingsPage"))

        self.profile_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.profile_zone.pack(side="bottom", fill="x")
        ctk.CTkLabel(self.profile_zone, text=f"👤 СЕЗИМАЙ\n{localization.get('librarian')}", text_color="white", justify="left").pack(side="left")

        # ==========================================
        # RIGHT CONTENT (Отступ 90px справа)
        # ==========================================
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True, padx=(20, 90), pady=20)

        # 1. ПРОФИЛЬ
        profile_card = ctk.CTkFrame(self.content, fg_color="#C4C4C4", corner_radius=15, height=200, border_width=1, border_color="#B0B0B0")
        profile_card.pack(fill="x", pady=(10, 20))
        profile_card.pack_propagate(False)

        ctk.CTkLabel(profile_card, text=localization.get("profile"), font=("Helvetica", 18, "bold"), text_color="black").place(x=25, y=20)
        ctk.CTkLabel(profile_card, text="👤", font=("Helvetica", 80), text_color="#A0A0A0").place(x=40, y=60)
        ctk.CTkLabel(profile_card, text=f"СЕЗИМАЙ\n{localization.get('librarian')}", font=("Helvetica", 20), text_color="black", justify="left").place(x=150, y=85)
        
        ctk.CTkButton(profile_card, text=localization.get("change_pass"), fg_color="#A8ADA8", text_color="black", 
                      hover_color="#9CA39E", border_width=1, border_color="black", corner_radius=5, width=150,
                      command=self.show_pw_modal).place(x=450, y=100, anchor="center")

        # 2. НИЖНИЕ БЛОКИ
        bottom_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        bottom_frame.pack(fill="both", expand=True)

        # СИСТЕМА
        sys_box = self.create_settings_box(
            bottom_frame, 
            localization.get("system"), 
            [localization.get("print"), localization.get("sound"), localization.get("notifications")]
        )
        sys_box.pack(side="left", fill="both", expand=True, padx=(0, 10))
        # ИНТЕРФЕЙС (Добавили переключатель языка!)
        int_box = ctk.CTkFrame(bottom_frame, fg_color="#C4C4C4", corner_radius=15, border_width=1, border_color="#B0B0B0")
        int_box.pack(side="left", fill="both", expand=True, padx=10)
        ctk.CTkLabel(int_box, text=localization.get("interface"), font=("Helvetica", 16, "bold"), text_color="black").pack(pady=15)
        
        theme_row = ctk.CTkFrame(int_box, fg_color="transparent")
        theme_row.pack(fill="x", padx=25, pady=8)
        ctk.CTkSwitch(theme_row, text=localization.get("dark_mode"), text_color="black", progress_color="#4A6550").pack(side="left")

        # Выбор языка
        lang_row = ctk.CTkFrame(int_box, fg_color="transparent")
        lang_row.pack(fill="x", padx=25, pady=20)
        ctk.CTkLabel(lang_row, text=localization.get("lang"), text_color="black", font=("Helvetica", 13)).pack(side="left")
        
        self.lang_menu = ctk.CTkOptionMenu(lang_row, values=["RU", "KG", "EN"], fg_color="#4A6550", button_color="#36493B", command=self.change_app_language)
        self.lang_menu.set(localization.current_lang) # Устанавливаем текущий язык
        self.lang_menu.pack(side="right")

        # ПОЛЬЗОВАТЕЛЬ
        usr_box = ctk.CTkFrame(bottom_frame, fg_color="#C4C4C4", corner_radius=15, border_width=1, border_color="#B0B0B0")
        usr_box.pack(side="left", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(usr_box, text=localization.get("user"), font=("Helvetica", 16, "bold"), text_color="black").pack(pady=15)

    def change_app_language(self, choice):
        """Меняет язык в словаре и просит главный файл перезагрузить интерфейс"""
        localization.set_lang(choice)
        # Если мы хотим, чтобы интерфейс мгновенно обновился, нам нужно вызвать метод перезагрузки в main.py
        if hasattr(self.controller, "rebuild_ui"):
            self.controller.rebuild_ui()

    def create_settings_box(self, parent, title, items):
        box = ctk.CTkFrame(parent, fg_color="#C4C4C4", corner_radius=15, border_width=1, border_color="#B0B0B0")
        ctk.CTkLabel(box, text=title, font=("Helvetica", 16, "bold"), text_color="black").pack(pady=15)
        for item in items:
            row = ctk.CTkFrame(box, fg_color="transparent")
            row.pack(fill="x", padx=25, pady=8)
            ctk.CTkLabel(row, text=item, text_color="black", font=("Helvetica", 13)).pack(side="left")
            ctk.CTkSwitch(row, text="", progress_color="#4A6550").pack(side="right")
        return box

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, anchor="w", height=45, corner_radius=10, command=command)
        btn.pack(fill="x", padx=10, pady=5)

    def show_pw_modal(self):
        self.modal = ctk.CTkFrame(self, fg_color="#E8E8E8", corner_radius=15, border_width=1, border_color="black")
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(self.modal, text="Новый пароль:", text_color="black", font=("Helvetica", 14, "bold")).pack(padx=30, pady=(20, 5))
        self.new_pw_entry = ctk.CTkEntry(self.modal, show="*", width=200)
        self.new_pw_entry.pack(padx=30, pady=10)
        ctk.CTkButton(self.modal, text="Сохранить", fg_color="#4A6550", command=self.save_pw).pack(pady=(10, 20))

    def save_pw(self):
        new_val = self.new_pw_entry.get()
        if new_val:
            database.update_password("admin", new_val)
            self.modal.destroy()
