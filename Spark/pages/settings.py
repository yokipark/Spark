import customtkinter as ctk
import database
import localization
import os
from PIL import Image
import services.export_service as export_service
from tkinter import messagebox

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        # Стартовое значение цвета под light-тему
        super().__init__(parent, fg_color="#FFFFFF")
        self.controller = controller

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(os.path.dirname(current_dir), "assets")

        # ==========================================
        # 1. SIDEBAR (Ширина: 370px)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=370, corner_radius=0, fg_color="#294730")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.sidebar_inner = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_inner.pack(fill="both", expand=True, padx=32, pady=(50, 25))

        # --- ЗОНА ЛОГОТИПА И ТЕКСТА ---
        self.logo_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.logo_zone.pack(side="top", fill="x", pady=(0, 40))

        logo_path = os.path.join(self.assets_dir, "library_icon.png")
        try:
            pil_logo = Image.open(logo_path)
            ctk_logo = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(50, 50))
            logo_display = ctk.CTkLabel(self.logo_zone, image=ctk_logo, text="")
            logo_display.pack(side="left", padx=(0, 15))
        except Exception:
            ctk.CTkLabel(self.logo_zone, text="📖", font=("Inter", 32)).pack(side="left", padx=(0, 15))

        text_frame = ctk.CTkFrame(self.logo_zone, fg_color="transparent")
        text_frame.pack(side="left", fill="y")
        ctk.CTkLabel(text_frame, text="Картотека", font=("Inter", 24, "bold"), text_color="#FFFFFF").pack(anchor="w")
        ctk.CTkLabel(text_frame, text="библиотекаря", font=("Inter", 14), text_color="#E6C619").pack(anchor="w")

        # --- НАВИГАЦИЯ ---
        self.nav_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.nav_zone.pack(side="top", fill="x")

        self.create_nav_btn(localization.get("main"), command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn(localization.get("settings"), is_active=True, command=lambda: controller.show_frame("SettingsPage"))

        # --- ЗОНА ПРОФИЛЯ СИДБАРА ---
        self.profile_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.profile_zone.pack(side="bottom", fill="x")

        user_path = os.path.join(self.assets_dir, "User_circle.png")
        try:
            pil_user = Image.open(user_path)
            ctk_user = ctk.CTkImage(light_image=pil_user, dark_image=pil_user, size=(45, 45))
            ctk.CTkLabel(self.profile_zone, image=ctk_user, text="").pack(side="left", padx=(0, 15))
        except Exception:
            ctk.CTkLabel(self.profile_zone, text="👤", font=("Inter", 24)).pack(side="left", padx=(0, 15))

        profile_text_frame = ctk.CTkFrame(self.profile_zone, fg_color="transparent")
        profile_text_frame.pack(side="left", fill="y")
        ctk.CTkLabel(profile_text_frame, text="СЕЗИМАЙ", text_color="white", font=("Inter", 14, "bold")).pack(anchor="w")
        ctk.CTkLabel(profile_text_frame, text=localization.get('librarian'), text_color="#BEAC64", font=("Inter", 14)).pack(anchor="w")

        # ==========================================
        # 2. ПРАВЫЙ КОНТЕЙНЕР
        # ==========================================
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True, padx=42, pady=50)

        # --- ШАПКА ---
        self.header = ctk.CTkFrame(self.content, height=45, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.search_bar = ctk.CTkEntry(self.header, placeholder_text=localization.get("search_placeholder", "Поиск..."), width=510, height=42, corner_radius=14, fg_color="#C4C4C4", text_color="black", border_width=0, font=("Inter", 14))
        self.search_bar.pack(side="left")

        self.add_btn = ctk.CTkButton(self.header, text=localization.get("add_book", "Добавить книгу"), fg_color="#BEAC64", text_color="black", width=193, height=42, corner_radius=14, font=("Inter", 14, "bold"), command=lambda: controller.show_frame("MainPage"))
        self.add_btn.pack(side="left", padx=(20, 0))

        self.export_btn = ctk.CTkOptionMenu(
            self.header, values=["Excel", "PDF", "JSON"], fg_color="#F5F4F2", button_color="#F5F4F2", button_hover_color="#D9D9D9",
            text_color="black", dropdown_text_color="black", dropdown_fg_color="#E8E8E8", dropdown_hover_color="#BEAC64",
            width=136, height=42, corner_radius=14, font=("Inter", 14, "bold"), command=self.trigger_data_export
        )
        self.export_btn.set(localization.get("export", "Export"))
        self.export_btn.pack(side="left", padx=(20, 0))

        # --- БЛОК ПРОФИЛЯ ---
        profile_card = ctk.CTkFrame(self.content, fg_color="#D9D9D9", corner_radius=16, height=200, border_width=1, border_color="black")
        profile_card.pack(fill="x", pady=(10, 20))
        profile_card.pack_propagate(False)

        ctk.CTkLabel(profile_card, text=localization.get("profile", "ПРОФИЛЬ").upper(), font=("Inter", 18, "bold"), text_color="black").place(x=25, y=20)
        
        try:
            pil_profile = Image.open(user_path)
            ctk_profile = ctk.CTkImage(light_image=pil_profile, dark_image=pil_profile, size=(90, 90))
            profile_display = ctk.CTkLabel(profile_card, image=ctk_profile, text="")
            profile_display.place(x=40, y=65)
        except Exception:
            ctk.CTkLabel(profile_card, text="👤", font=("Inter", 70), text_color="black").place(x=40, y=65)

        name_frame = ctk.CTkFrame(profile_card, fg_color="transparent")
        name_frame.place(x=160, y=75)
        ctk.CTkLabel(name_frame, text="СЕЗИМАЙ", font=("Inter", 24, "bold"), text_color="black").pack(anchor="w")
        ctk.CTkLabel(name_frame, text=localization.get('librarian', "Библиотекарь"), font=("Inter", 16), text_color="#7A7A7A").pack(anchor="w", pady=(2, 0))
        
        ctk.CTkButton(profile_card, text=localization.get("change_pass", "Сменить пароль"), fg_color="#F5F4F2", text_color="black", 
                      hover_color="#D9D9D9", border_width=1, border_color="black", corner_radius=14, width=180, height=45, font=("Inter", 14, "bold"),
                      command=self.show_pw_modal).place(x=910, y=110, anchor="ne")

        # --- НИЖНЯЯ СЕТКА БЛОКОВ НАСТРОЕК ---
        bottom_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        bottom_frame.pack(fill="both", expand=True)

        # 1. СИСТЕМА (Слева)
        sys_box = self.create_settings_box(
            bottom_frame, 
            localization.get("system", "СИСТЕМА"), 
            [localization.get("print", "Печать"), localization.get("sound", "Звук"), localization.get("notifications", "Уведомления")]
        )
        sys_box.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # 2. ИНТЕРФЕЙС (По центру)
        int_box = ctk.CTkFrame(bottom_frame, fg_color="#D9D9D9", corner_radius=16, border_width=1, border_color="black")
        int_box.pack(side="left", fill="both", expand=True, padx=0)
        int_box.pack_propagate(False)
        ctk.CTkLabel(int_box, text=localization.get("interface", "ИНТЕРФЕЙС").upper(), font=("Inter", 18, "bold"), text_color="black").pack(pady=(15, 5), anchor="w", padx=25)
        
        theme_row = ctk.CTkFrame(int_box, fg_color="transparent")
        theme_row.pack(fill="x", padx=25, pady=4)
        
        # Переключатель ТЕМЫ (Добавлен обработчик command)
        self.theme_switch = ctk.CTkSwitch(theme_row, text=localization.get("dark_mode", "Темная тема"), text_color="black", progress_color="#294730", font=("Inter", 14), command=self.toggle_dark_mode)
        self.theme_switch.pack(side="left")

        # Надпись «Акцентные цвета»
        ctk.CTkLabel(int_box, text="Акцентные цвета", font=("Inter", 15, "bold"), text_color="black").pack(pady=(20, 10), anchor="w", padx=25)

        # Сетка для размещения ассетов цветов в 2 ряда по макету
        color_grid = ctk.CTkFrame(int_box, fg_color="transparent")
        color_grid.pack(fill="x", padx=25)

        # Ряд 1 (Vector 4, 6, 8, 9@2x)
        row1 = ctk.CTkFrame(color_grid, fg_color="transparent")
        row1.pack(fill="x", anchor="w", pady=4)
        
        row1_files = ["Vector 4.png", "Vector 6.png", "Vector 8.png", "Vector 9@2x.png"]
        for f_name in row1_files:
            img_path = os.path.join(self.assets_dir, f_name)
            try:
                pil_color = Image.open(img_path)
                ctk_color_img = ctk.CTkImage(light_image=pil_color, dark_image=pil_color, size=(48, 44))
                btn = ctk.CTkButton(row1, image=ctk_color_img, text="", width=48, height=44, fg_color="transparent", hover_color="#C4C4C4")
                btn.pack(side="left", padx=4)
            except Exception:
                pass

        # Ряд 2 (Vector 10)
        row2 = ctk.CTkFrame(color_grid, fg_color="transparent")
        row2.pack(fill="x", anchor="w", pady=4)
        
        try:
            v10_path = os.path.join(self.assets_dir, "Vector 10.png")
            pil_v10 = Image.open(v10_path)
            ctk_v10_img = ctk.CTkImage(light_image=pil_v10, dark_image=pil_v10, size=(48, 44))
            btn_v10 = ctk.CTkButton(row2, image=ctk_v10_img, text="", width=48, height=44, fg_color="transparent", hover_color="#C4C4C4")
            btn_v10.pack(side="left", padx=4)
        except Exception:
            pass

        # Селектор языка снизу
        lang_row = ctk.CTkFrame(int_box, fg_color="transparent")
        lang_row.pack(fill="x", padx=25, pady=(20, 0))
        ctk.CTkLabel(lang_row, text=localization.get("lang", "Язык"), text_color="black", font=("Inter", 14)).pack(side="left")
        
        self.lang_menu = ctk.CTkOptionMenu(lang_row, values=["RU", "KG", "EN"], fg_color="#294730", button_color="#1F3624", corner_radius=10, font=("Inter", 13, "bold"), command=self.change_app_language)
        self.lang_menu.set(localization.current_lang)
        self.lang_menu.pack(side="right")

        # 3. ИНФОРМАЦИЯ О БИБЛИОТЕКЕ (Справа)
        usr_box = ctk.CTkFrame(bottom_frame, fg_color="#D9D9D9", corner_radius=16, border_width=1, border_color="black")
        usr_box.pack(side="left", fill="both", expand=True, padx=(20, 0))
        usr_box.pack_propagate(False)
        
        ctk.CTkLabel(usr_box, text=localization.get("lib_info", "ИНФОРМАЦИЯ О БИБЛИОТЕКЕ").upper(), font=("Inter", 16, "bold"), text_color="black").pack(pady=15, anchor="w", padx=20)
        
        self.library_info_editor = ctk.CTkTextbox(usr_box, fg_color="#F5F4F2", text_color="black", font=("Inter", 14), corner_radius=12, border_width=1, border_color="#B0B0B0")
        self.library_info_editor.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        figma_text = (
            "Название: Городская библиотека им. А.С. Пушкина\n"
            "с доступом к электронным ресурсам.\n"
            "- Название: Городская библиотека им. А.С. Пушкина\n"
            "- Часы работы: Пн-Сб, 09:00 - 19:00\n"
            "- Описание: Уютная библиотека в центре города с богатым "
            "фондом и доступом к электронным ресурсам."
        )
        self.library_info_editor.insert("0.0", figma_text)

    def toggle_dark_mode(self):
        """Вызывает глобальную смену темы через корневой контроллер приложения"""
        if self.theme_switch.get() == 1:
            # Если тумблер включен — отправляем команду "dark" в контроллер
            if hasattr(self.controller, "change_global_theme"):
                self.controller.change_global_theme("dark")
            else:
                # Фоллбэк, если метода в main.py еще нет
                ctk.set_appearance_mode("dark")
                self.configure(fg_color="#6D6D6D")
        else:
            # Если выключен — отправляем "light"
            if hasattr(self.controller, "change_global_theme"):
                self.controller.change_global_theme("light")
            else:
                ctk.set_appearance_mode("light")
                self.configure(fg_color="#FFFFFF")
    def change_app_language(self, choice):
        localization.set_lang(choice)
        if hasattr(self.controller, "rebuild_ui"):
            self.controller.frames["DashboardPage"].draw_weekly_chart(self.controller.frames["DashboardPage"].graph_box)
            self.controller.rebuild_ui()

    def create_settings_box(self, parent, title, items):
        box = ctk.CTkFrame(parent, fg_color="#D9D9D9", corner_radius=16, border_width=1, border_color="black")
        box.pack_propagate(False)
        ctk.CTkLabel(box, text=title.upper(), font=("Inter", 18, "bold"), text_color="black").pack(pady=15, anchor="w", padx=25)
        for item in items:
            row = ctk.CTkFrame(box, fg_color="transparent")
            row.pack(fill="x", padx=25, pady=8)
            ctk.CTkLabel(row, text=item, text_color="black", font=("Inter", 14)).pack(side="left")
            ctk.CTkSwitch(row, text="", progress_color="#294730").pack(side="right")
        return box

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#BEAC64" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, text_color="white", font=("Inter", 20),
                            anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", pady=5)
        
    def show_pw_modal(self):
        self.modal = ctk.CTkFrame(self, fg_color="#E8E8E8", corner_radius=16, border_width=1, border_color="black")
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(self.modal, text="Новый пароль:", text_color="black", font=("Inter", 14, "bold")).pack(padx=30, pady=(20, 5))
        self.new_pw_entry = ctk.CTkEntry(self.modal, show="*", width=200, font=("Inter", 14))
        self.new_pw_entry.pack(padx=30, pady=10)
        ctk.CTkButton(self.modal, text="Сохранить", fg_color="#294730", font=("Inter", 14, "bold"), corner_radius=10, command=self.save_pw).pack(pady=(10, 20))

    def save_pw(self):
        new_val = self.new_pw_entry.get()
        if new_val:
            database.update_password("admin", new_val)
            self.modal.destroy()

    def trigger_data_export(self, choice):
        try:
            if choice == "JSON": path = export_service.export_to_json()
            elif choice == "Excel": path = export_service.export_to_excel()
            elif choice == "PDF": path = export_service.export_to_pdf()
            self.export_btn.set(localization.get("export", "Export"))
            messagebox.showinfo("Экспорт завершен", f"Успешно выгружено в файл:\n{os.path.basename(path)}")
        except Exception as e:
            self.export_btn.set(localization.get("export", "Export"))
            messagebox.showerror("Ошибка экспорта", str(e))
