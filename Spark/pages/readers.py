import customtkinter as ctk
import database
import localization
import os
from PIL import Image
import services.export_service as export_service
from tkinter import messagebox

class ReaderPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF")
        self.controller = controller

        # Настраиваем путь к папке assets
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
        except Exception as e:
            print(f"Ошибка логотипа: {e}")
            ctk.CTkLabel(self.logo_zone, text="📖", font=("Inter", 32)).pack(side="left", padx=(0, 15))

        text_frame = ctk.CTkFrame(self.logo_zone, fg_color="transparent")
        text_frame.pack(side="left", fill="y")
        ctk.CTkLabel(text_frame, text=localization.get("app_title_1"), font=("Inter", 24, "bold"), text_color="#FFFFFF").pack(anchor="w")
        ctk.CTkLabel(text_frame, text=localization.get("app_title_2"), font=("Inter", 14), text_color="#E6C619").pack(anchor="w")

        # --- НАВИГАЦИЯ ---
        self.nav_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.nav_zone.pack(side="top", fill="x")

        self.create_nav_btn(localization.get("main"), command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), is_active=True, command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn(localization.get("settings"), command=lambda: controller.show_frame("SettingsPage"))

        # --- ЗОНА ПРОФИЛЯ ---
        self.profile_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.profile_zone.pack(side="bottom", fill="x")

        user_path = os.path.join(self.assets_dir, "User_circle.png")
        if not os.path.exists(user_path):
            user_path = os.path.join(self.assets_dir, "User_cicrle.png")

        try:
            pil_user = Image.open(user_path)
            ctk_user = ctk.CTkImage(light_image=pil_user, dark_image=pil_user, size=(45, 45))
            user_display = ctk.CTkLabel(self.profile_zone, image=ctk_user, text="")
            user_display.pack(side="left", padx=(0, 15))
        except Exception as e:
            print(f"Ошибка аватара: {e}")
            ctk.CTkLabel(self.profile_zone, text="👤", font=("Inter", 24)).pack(side="left", padx=(0, 15))

        profile_text_frame = ctk.CTkFrame(self.profile_zone, fg_color="transparent")
        profile_text_frame.pack(side="left", fill="y")
        ctk.CTkLabel(profile_text_frame, text="СЕЗИМАЙ", text_color="white", font=("Inter", 14, "bold")).pack(anchor="w")
        ctk.CTkLabel(profile_text_frame, text=localization.get('librarian'), text_color="#BEAC64", font=("Inter", 14)).pack(anchor="w")

        # ==========================================
        # 2. RIGHT CONTAINER (Контентная область)
        # ==========================================
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=42, pady=50)

        # --- ШАПКА И ПОИСК ---
        self.header = ctk.CTkFrame(self.content_container, height=45, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.search_bar = ctk.CTkEntry(self.header, placeholder_text=localization.get("search_placeholder"), width=510, height=42, corner_radius=14, fg_color="#C4C4C4", text_color="black", border_width=0, font=("Inter", 14))
        self.search_bar.pack(side="left")
        self.search_bar.bind("<KeyRelease>", self.perform_search)

        self.add_btn = ctk.CTkButton(self.header, text=localization.get("add_reader"), fg_color="#BEAC64", text_color="black", width=193, height=42, corner_radius=14, font=("Inter", 14, "bold"), command=self.show_add_reader_modal)
        self.add_btn.pack(side="left", padx=(20, 0))

        # Выпадающее меню из 3-х вариантов экспорта
        self.export_btn = ctk.CTkOptionMenu(
            self.header,
            values=["Excel", "PDF", "JSON"], 
            fg_color="#F5F4F2", 
            button_color="#F5F4F2", 
            button_hover_color="#D9D9D9",
            text_color="black", 
            dropdown_text_color="black",
            dropdown_fg_color="#E8E8E8",
            dropdown_hover_color="#BEAC64",
            width=136, 
            height=42, 
            corner_radius=14, 
            font=("Inter", 14, "bold"),
            command=self.trigger_data_export
        )
        self.export_btn.set(localization.get("export"))
        self.export_btn.pack(side="left", padx=(20, 0))

        # --- ТАБЛИЦА ЧИТАТЕЛЕЙ ---
        self.table_frame = ctk.CTkFrame(self.content_container, fg_color="#D9D9D9", corner_radius=16, border_width=1, border_color="black")
        self.table_frame.pack(fill="both", expand=True)

        self.headers = [localization.get("inv_num"), localization.get("reader_name"), "Кол-во книг", "Прочитано"]
        self.load_data()

    # --- ЛОГИКА ТАБЛИЦЫ ---
    def perform_search(self, event):
        query = self.search_bar.get().strip()
        self.load_data(search_query=query)

    def load_data(self, search_query=""):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        for i, h in enumerate(self.headers):
            ctk.CTkLabel(self.table_frame, text=h, font=("Inter", 13, "bold"), text_color="black").grid(row=0, column=i, padx=20, pady=15, sticky="nsew")
            self.table_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkFrame(self.table_frame, height=1, fg_color="black").grid(row=1, column=0, columnspan=4, sticky="ew")

        if search_query:
            readers = database.search_readers(search_query)
        else:
            readers = database.get_all_readers()
        
        for row_idx, row_data in enumerate(readers, start=2):
            for col_idx, item in enumerate(row_data):
                ctk.CTkLabel(self.table_frame, text=str(item), text_color="black", font=("Inter", 13)).grid(row=row_idx, column=col_idx, padx=5, pady=10)
            
            ctk.CTkFrame(self.table_frame, height=1, fg_color="#A0A0A0").grid(row=row_idx*2+1, column=0, columnspan=4, sticky="ew")

    # --- МОДАЛЬНОЕ ОКНО ---
    def show_add_reader_modal(self):
        if hasattr(self, "modal") and self.modal.winfo_exists():
            return

        self.modal = ctk.CTkFrame(self.content_container, width=680, height=450, fg_color="#E8E8E8", corner_radius=20, border_width=1, border_color="#B0B0B0")
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        self.modal.grid_propagate(False)

        self.modal.grid_columnconfigure(0, weight=3)
        self.modal.grid_columnconfigure(1, weight=2)

        # =========================================================
        # ЛЕВАЯ ЧАСТЬ: ПОЛЯ ВВОДА (Контейнер)
        # =========================================================
        left_fields_frame = ctk.CTkFrame(self.modal, fg_color="transparent")
        left_fields_frame.grid(row=0, column=0, sticky="nsew", padx=(40, 20), pady=(40, 20))

        # 1. ФИО ЧИТАТЕЛЯ
        lbl_fio = ctk.CTkLabel(left_fields_frame, text="Введите имя читателя", font=("Inter", 13), text_color="black", fg_color="#C4C4C4", corner_radius=10, height=28)
        lbl_fio.pack(anchor="w", pady=(0, 6), padx=5)
        
        self.name_entry = ctk.CTkEntry(left_fields_frame, height=45, corner_radius=14, fg_color="#F5F4F2", text_color="black", border_width=1, border_color="#B0B0B0", font=("Inter", 15))
        self.name_entry.pack(fill="x", pady=(0, 25))

        # Контейнер для нижних двух инпутов, стоящих в один ряд
        row_inputs = ctk.CTkFrame(left_fields_frame, fg_color="transparent")
        row_inputs.pack(fill="x")
        row_inputs.grid_columnconfigure(0, weight=1)
        row_inputs.grid_columnconfigure(1, weight=1)

        # 2. ИНВЕНТАРНЫЙ НОМЕР
        inv_sub_frame = ctk.CTkFrame(row_inputs, fg_color="transparent")
        inv_sub_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        lbl_inv = ctk.CTkLabel(inv_sub_frame, text=localization.get("inv_num"), font=("Inter", 13), text_color="black", fg_color="#C4C4C4", corner_radius=10, height=28)
        lbl_inv.pack(anchor="w", pady=(0, 6), padx=5)

        self.inv_entry = ctk.CTkEntry(inv_sub_frame, height=45, corner_radius=14, fg_color="#F5F4F2", text_color="black", border_width=1, border_color="#B0B0B0", font=("Inter", 15))
        self.inv_entry.pack(fill="x")

        # 3. ДАТА РЕГИСТРАЦИИ
        date_sub_frame = ctk.CTkFrame(row_inputs, fg_color="transparent")
        date_sub_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        lbl_date = ctk.CTkLabel(date_sub_frame, text="Дата регистрации", font=("Inter", 13), text_color="black", fg_color="#C4C4C4", corner_radius=10, height=28)
        lbl_date.pack(anchor="w", pady=(0, 6), padx=5)

        current_date_str = database.datetime.now().strftime("%d.%m.%Y")
        self.date_entry = ctk.CTkEntry(date_sub_frame, height=45, corner_radius=14, fg_color="#F5F4F2", text_color="black", border_width=1, border_color="#B0B0B0", font=("Inter", 15))
        self.date_entry.insert(0, current_date_str)
        self.date_entry.pack(fill="x")

        # =========================================================
        # ПРАВАЯ ЧАСТЬ: АВАТАРКА ПРОФИЛЯ
        # =========================================================
        right_avatar_frame = ctk.CTkFrame(self.modal, fg_color="transparent")
        right_avatar_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 40), pady=(40, 20))

        user_path = os.path.join(self.assets_dir, "User_circle.png")
        if not os.path.exists(user_path):
            user_path = os.path.join(self.assets_dir, "User_cicrle.png")

        try:
            pil_img = Image.open(user_path)
            ctk_icon = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(130, 130))
            profile_display = ctk.CTkLabel(right_avatar_frame, image=ctk_icon, text="")
            profile_display.pack(pady=(20, 5))
        except Exception:
            profile_circle = ctk.CTkLabel(right_avatar_frame, text="👤", font=("Inter", 100), text_color="#BEAC64")
            profile_circle.pack(pady=(20, 5))

        ctk.CTkLabel(right_avatar_frame, text="новый читатель", font=("Inter", 14), text_color="gray").pack()

        # =========================================================
        # НИЖНЯЯ ЧАСТЬ: КНОПКИ УПРАВЛЕНИЯ
        # =========================================================
        btn_cancel = ctk.CTkButton(self.modal, text=localization.get("cancel").upper(), fg_color="transparent", text_color="black", hover_color="#D9D9D9", width=140, height=50, font=("Inter", 18, "bold"), command=self.modal.destroy)
        btn_cancel.place(x=290, y=360)

        btn_add = ctk.CTkButton(self.modal, text="ДОБАВИТЬ", fg_color="#BEAC64", text_color="white", hover_color="#A89755", width=180, height=50, corner_radius=14, font=("Inter", 18, "bold"), command=self.save_new_reader)
        btn_add.place(x=455, y=360)
        
    def save_new_reader(self):
        new_name = self.name_entry.get().strip()
        inv_no = self.inv_entry.get().strip()
        reg_date = self.date_entry.get().strip()

        if new_name != "":
            database.add_reader(new_name, inv_no, reg_date)
            self.load_data()
            
            if "DashboardPage" in self.controller.frames:
                self.controller.frames["DashboardPage"].refresh_data()
            if "ReportsPage" in self.controller.frames:
                self.controller.frames["ReportsPage"].refresh_reports()
                
            self.modal.destroy()
        else:
            self.name_entry.configure(border_color="#C13C3C", border_width=2)

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#BEAC64" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, text_color="white", font=("Inter", 20),
                            anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", pady=5)

    def trigger_data_export(self, choice):
        try:
            if choice == "JSON":
                path = export_service.export_to_json()
            elif choice == "Excel":
                path = export_service.export_to_excel()
            elif choice == "PDF":
                path = export_service.export_to_pdf()
            
            self.export_btn.set(localization.get("export"))
            filename = os.path.basename(path)
            messagebox.showinfo(localization.get("exp_success_title"), localization.get("exp_success_msg").format(filename))
        except Exception as e:
            self.export_btn.set(localization.get("export"))
            messagebox.showerror(localization.get("exp_error_title"), localization.get("exp_error_msg").format(str(e)))
