import customtkinter as ctk
import database

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#4A6550")
        self.sidebar.pack(side="left", fill="y")
        
        # Logo/Title
        ctk.CTkLabel(self.sidebar, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(pady=(30, 30))
        
        # Navigation
        self.create_nav_btn("🏠 Главное", command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn("📋 Книжный фонд", command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn("👤 Читатель", command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn("🕒 Выдача/Возврат", command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn("📊 Отчеты", command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn("⚙️ Настройки", is_active=True, command=lambda: controller.show_frame("SettingsPage"))

        # --- RIGHT CONTENT ---
        # Fixed: Added padx=(20, 90) to ensure the 90px distance from the right side
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True, padx=(40, 90), pady=20)

        # 1. PROFILE SECTION
        profile_card = ctk.CTkFrame(self.content, fg_color="#C4C4C4", corner_radius=15, height=200)
        profile_card.pack(fill="x", pady=(10, 20))
        profile_card.pack_propagate(False)

        ctk.CTkLabel(profile_card, text="ПРОФИЛЬ", font=("Helvetica", 18, "bold"), text_color="black").place(x=25, y=20)
        
        # Profile Icon Placeholder
        profile_icon = ctk.CTkLabel(profile_card, text="👤", font=("Helvetica", 80), text_color="#A0A0A0")
        profile_icon.place(x=40, y=60)
        
        ctk.CTkLabel(profile_card, text="СЕЗИМАЙ\nБиблиотекарь", font=("Helvetica", 20), text_color="black", justify="left").place(x=150, y=85)
        
        # "Сменить пароль" button - Positioned more centrally as seen in myshot-1778730207.jpg
        change_pw_btn = ctk.CTkButton(
            profile_card, 
            text="Сменить пароль", 
            fg_color="#A8ADA8", 
            text_color="black", 
            hover_color="#9CA39E", 
            border_width=1, 
            border_color="black", 
            corner_radius=5,
            width=150,
            command=self.show_pw_modal
        )
        change_pw_btn.place(x=450, y=100, anchor="center")

        # 2. BOTTOM GRIDS (System / Interface / User)
        # Using a container with no expansion constraints to keep the 90px right margin clean
        bottom_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        bottom_frame.pack(fill="both", expand=True)

        # СИСТЕМА
        sys_box = self.create_settings_box(bottom_frame, "СИСТЕМА", ["печать", "звук", "уведомление"])
        sys_box.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # ИНТЕРФЕЙС
        int_box = ctk.CTkFrame(bottom_frame, fg_color="#C4C4C4", corner_radius=15)
        int_box.pack(side="left", fill="both", expand=True, padx=10)
        ctk.CTkLabel(int_box, text="ИНТЕРФЕЙС", font=("Helvetica", 16, "bold"), text_color="black").pack(pady=15)
        
        theme_row = ctk.CTkFrame(int_box, fg_color="transparent")
        theme_row.pack(fill="x", padx=20)
        ctk.CTkSwitch(theme_row, text="Темная тема", text_color="black", progress_color="#4A6550").pack(side="left")

        # ПОЛЬЗОВАТЕЛЬ (Consistent with the 90px right spacing of the container)
        usr_box = ctk.CTkFrame(bottom_frame, fg_color="#C4C4C4", corner_radius=15)
        usr_box.pack(side="left", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(usr_box, text="ПОЛЬЗОВАТЕЛЬ", font=("Helvetica", 16, "bold"), text_color="black").pack(pady=15)

    def create_settings_box(self, parent, title, items):
        box = ctk.CTkFrame(parent, fg_color="#C4C4C4", corner_radius=15)
        ctk.CTkLabel(box, text=title, font=("Helvetica", 16, "bold"), text_color="black").pack(pady=15)
        for item in items:
            row = ctk.CTkFrame(box, fg_color="transparent")
            row.pack(fill="x", padx=25, pady=8)
            ctk.CTkLabel(row, text=item, text_color="black", font=("Helvetica", 13)).pack(side="left")
            ctk.CTkSwitch(row, text="", progress_color="#4A6550").pack(side="right")
        return box

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color=bg, anchor="w", height=45, corner_radius=10, command=command)
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
