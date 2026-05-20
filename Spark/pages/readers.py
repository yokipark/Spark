import customtkinter as ctk
import database 

class ReaderPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

        # --- SIDEBAR --- (Same as before)
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#4A6550")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(pady=(30, 0))
        
        self.create_nav_btn("🏠 Главное", commanimport customtkinter as ctk
import database
import localization
class ReaderPage(ctk.CTkFrame):
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

        # Логотип
        self.logo_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.logo_zone.pack(side="top", fill="x", pady=(0, 40)) 
        ctk.CTkLabel(self.logo_zone, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(anchor="w")
        ctk.CTkLabel(self.logo_zone, text="библиотекаря", font=("Helvetica", 14), text_color="#E6C619").pack(anchor="w")

        # Навигация
        self.nav_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.nav_zone.pack(side="top", fill="x")

        self.create_nav_btn(localization.get("main"), command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), is_active=True, command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn(localization.get("settings"), command=lambda: controller.show_frame("SettingsPage"))

        # Профиль
        self.profile_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.profile_zone.pack(side="bottom", fill="x")
        ctk.CTkLabel(self.profile_zone, text=f"👤 СЕЗИМАЙ\n{localization.get("librarian")}", text_color="white", justify="left").pack(side="left")

        # ==========================================
        # RIGHT CONTENT
        # ==========================================
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # --- ШАПКА ---
        self.header = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.search_bar = ctk.CTkEntry(self.header, placeholder_text="Поиск по ФИО или № читателя...", width=400, height=40, corner_radius=20, fg_color="#C4C4C4", text_color="black")
        self.search_bar.pack(side="left", padx=10)
        
        # ⚡ МАГИЯ ПОИСКА для читателей
        self.search_bar.bind("<KeyRelease>", self.perform_search)

        self.add_btn = ctk.CTkButton(self.header, text=localization.get("add_reader"), fg_color="#7C9A82", text_color="black", height=40, command=self.show_add_reader_modal)
        self.add_btn.pack(side="left", padx=10)

        self.export_btn = ctk.CTkOptionMenu(self.header, values=["Excel", "PDF"], fg_color="#D1C4A3", button_color="#D1C4A3", text_color="black", height=40)
        self.export_btn.set(localization.get("export"))
        self.export_btn.pack(side="right", padx=10)

        # --- ТАБЛИЦА ---
        self.table_frame = ctk.CTkFrame(self.content_container, fg_color="#C4C4C4", corner_radius=15, border_width=1, border_color="#A0A0A0")
        self.table_frame.pack(fill="both", expand=True, pady=10)

        self.headers = ["№ читателя", localization.get("reader_name"), "Кол-во книг", "Прочитанно"]
        self.load_data()

    # --- ЛОГИКА ---

    def perform_search(self, event):
        query = self.search_bar.get().strip()
        self.load_data(search_query=query)

    def load_data(self, search_query=""):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        for i, h in enumerate(self.headers):
            ctk.CTkLabel(self.table_frame, text=h, font=("Helvetica", 13, "bold"), text_color="black").grid(row=0, column=i, padx=20, pady=15, sticky="nsew")
            self.table_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkFrame(self.table_frame, height=1, fg_color="#A0A0A0").grid(row=1, column=0, columnspan=4, sticky="ew")

        # Подгружаем данные (с фильтром или без)
        if search_query:
            readers = database.search_readers(search_query)
        else:
            readers = database.get_all_readers()
        
        for row_idx, row_data in enumerate(readers, start=2):
            for col_idx, item in enumerate(row_data):
                ctk.CTkLabel(self.table_frame, text=str(item), text_color="black", font=("Helvetica", 13)).grid(row=row_idx, column=col_idx, padx=5, pady=10)
            
            ctk.CTkFrame(self.table_frame, height=1, fg_color="#A0A0A0").grid(row=row_idx*2+1, column=0, columnspan=4, sticky="ew")

    # --- МОДАЛЬНОЕ ОКНО ---

    def show_add_reader_modal(self):
        if hasattr(self, "modal") and self.modal.winfo_exists():
            return

        self.modal = ctk.CTkFrame(self.content_container, width=580, height=350, fg_color="#E8E8E8", corner_radius=20, border_width=1, border_color="#B0B0B0")
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        self.modal.pack_propagate(False)

        ctk.CTkButton(self.modal, text="Сохранить", fg_color="#7C9A82", text_color="black", width=180, height=35, command=self.save_new_reader).place(x=360, y=30)
        ctk.CTkButton(self.modal, text="Отмена", fg_color="transparent", text_color="gray", hover_color="#D9D9D9", width=100, height=35, command=self.modal.destroy).place(x=250, y=30)

        profile_circle = ctk.CTkLabel(self.modal, text="👤", font=("Helvetica", 90), text_color="#7C9A82", width=130, height=130)
        profile_circle.place(x=80, y=120, anchor="center")

        self.name_entry = ctk.CTkEntry(self.modal, placeholder_text="Введите ФИО", font=("Helvetica", 18), width=250, height=40, fg_color="#D9D9D9", text_color="black")
        self.name_entry.place(x=160, y=105, anchor="w")
        
        ctk.CTkLabel(self.modal, text="новый читатель", font=("Helvetica", 14), text_color="gray").place(x=160, y=150, anchor="w")

    def save_new_reader(self):
        new_name = self.name_entry.get().strip()
        if new_name != "":
            database.add_reader(new_name)
            self.load_data()
            
            # Обновляем Дашборд!
            if "DashboardPage" in self.controller.frames:
                self.controller.frames["DashboardPage"].refresh_data()
                
            self.modal.destroy()
        else:
            self.name_entry.configure(border_color="#C13C3C", border_width=2)

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, text_color="white", 
                            anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", pady=5)import customtkinter as ctk
import database
import localization
class ReaderPage(ctk.CTkFrame):
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

        # Логотип
        self.logo_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.logo_zone.pack(side="top", fill="x", pady=(0, 40)) 
        ctk.CTkLabel(self.logo_zone, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(anchor="w")
        ctk.CTkLabel(self.logo_zone, text="библиотекаря", font=("Helvetica", 14), text_color="#E6C619").pack(anchor="w")

        # Навигация
        self.nav_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.nav_zone.pack(side="top", fill="x")

        self.create_nav_btn(localization.get("main"), command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), is_active=True, command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn(localization.get("settings"), command=lambda: controller.show_frame("SettingsPage"))

        # Профиль
        self.profile_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.profile_zone.pack(side="bottom", fill="x")
        ctk.CTkLabel(self.profile_zone, text=f"👤 СЕЗИМАЙ\n{localization.get("librarian")}", text_color="white", justify="left").pack(side="left")

        # ==========================================
        # RIGHT CONTENT
        # ==========================================
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # --- ШАПКА ---
        self.header = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.search_bar = ctk.CTkEntry(self.header, placeholder_text="Поиск по ФИО или № читателя...", width=400, height=40, corner_radius=20, fg_color="#C4C4C4", text_color="black")
        self.search_bar.pack(side="left", padx=10)
        
        # ⚡ МАГИЯ ПОИСКА для читателей
        self.search_bar.bind("<KeyRelease>", self.perform_search)

        self.add_btn = ctk.CTkButton(self.header, text=localization.get("add_reader"), fg_color="#7C9A82", text_color="black", height=40, command=self.show_add_reader_modal)
        self.add_btn.pack(side="left", padx=10)

        self.export_btn = ctk.CTkOptionMenu(self.header, values=["Excel", "PDF"], fg_color="#D1C4A3", button_color="#D1C4A3", text_color="black", height=40)
        self.export_btn.set(localization.get("export"))
        self.export_btn.pack(side="right", padx=10)

        # --- ТАБЛИЦА ---
        self.table_frame = ctk.CTkFrame(self.content_container, fg_color="#C4C4C4", corner_radius=15, border_width=1, border_color="#A0A0A0")
        self.table_frame.pack(fill="both", expand=True, pady=10)

        self.headers = ["№ читателя", localization.get("reader_name"), "Кол-во книг", "Прочитанно"]
        self.load_data()

    # --- ЛОГИКА ---

    def perform_search(self, event):
        query = self.search_bar.get().strip()
        self.load_data(search_query=query)

    def load_data(self, search_query=""):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        for i, h in enumerate(self.headers):
            ctk.CTkLabel(self.table_frame, text=h, font=("Helvetica", 13, "bold"), text_color="black").grid(row=0, column=i, padx=20, pady=15, sticky="nsew")
            self.table_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkFrame(self.table_frame, height=1, fg_color="#A0A0A0").grid(row=1, column=0, columnspan=4, sticky="ew")

        # Подгружаем данные (с фильтром или без)
        if search_query:
            readers = database.search_readers(search_query)
        else:
            readers = database.get_all_readers()
        
        for row_idx, row_data in enumerate(readers, start=2):
            for col_idx, item in enumerate(row_data):
                ctk.CTkLabel(self.table_frame, text=str(item), text_color="black", font=("Helvetica", 13)).grid(row=row_idx, column=col_idx, padx=5, pady=10)
            
            ctk.CTkFrame(self.table_frame, height=1, fg_color="#A0A0A0").grid(row=row_idx*2+1, column=0, columnspan=4, sticky="ew")

    # --- МОДАЛЬНОЕ ОКНО ---

    def show_add_reader_modal(self):
        if hasattr(self, "modal") and self.modal.winfo_exists():
            return

        self.modal = ctk.CTkFrame(self.content_container, width=580, height=350, fg_color="#E8E8E8", corner_radius=20, border_width=1, border_color="#B0B0B0")
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        self.modal.pack_propagate(False)

        ctk.CTkButton(self.modal, text="Сохранить", fg_color="#7C9A82", text_color="black", width=180, height=35, command=self.save_new_reader).place(x=360, y=30)
        ctk.CTkButton(self.modal, text="Отмена", fg_color="transparent", text_color="gray", hover_color="#D9D9D9", width=100, height=35, command=self.modal.destroy).place(x=250, y=30)

        profile_circle = ctk.CTkLabel(self.modal, text="👤", font=("Helvetica", 90), text_color="#7C9A82", width=130, height=130)
        profile_circle.place(x=80, y=120, anchor="center")

        self.name_entry = ctk.CTkEntry(self.modal, placeholder_text="Введите ФИО", font=("Helvetica", 18), width=250, height=40, fg_color="#D9D9D9", text_color="black")
        self.name_entry.place(x=160, y=105, anchor="w")
        
        ctk.CTkLabel(self.modal, text="новый читатель", font=("Helvetica", 14), text_color="gray").place(x=160, y=150, anchor="w")

    def save_new_reader(self):
        new_name = self.name_entry.get().strip()
        if new_name != "":
            database.add_reader(new_name)
            self.load_data()
            
            # Обновляем Дашборд!
            if "DashboardPage" in self.controller.frames:
                self.controller.frames["DashboardPage"].refresh_data()
                
            self.modal.destroy()
        else:
            self.name_entry.configure(border_color="#C13C3C", border_width=2)

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, text_color="white", 
                            anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", pady=5)d=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn("📋 Книжный фонд", command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn("👤 Читатель", is_active=True, command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn("🕒 Выдача/Возврат", command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn("📊 Отчеты", command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn("⚙️ Настройки", command=lambda: controller.show_frame("SettingsPage"))


        # --- RIGHT CONTENT CONTAINER ---
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Header
        self.header = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.search_bar = ctk.CTkEntry(self.header, placeholder_text="Поиск по всей базе...", width=450, height=40, corner_radius=20)
        self.search_bar.pack(side="left", padx=10)

        self.add_btn = ctk.CTkButton(self.header, text="ДОБАВИТЬ ЧИТАТЕЛЯ", fg_color="#7C9A82", height=40, command=self.show_add_reader_modal)
        self.add_btn.pack(side="left", padx=10)

        # --- TABLE SETUP ---
        self.table_frame = ctk.CTkFrame(self.content_container, fg_color="white", corner_radius=10)
        self.table_frame.pack(fill="both", expand=True, pady=10)

        self.headers = ["№ читателя", "ФИО читателя", "Кол-во книг", "Прочитанно"]
        
        # Load the initial data from the database
        self.load_data()

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color=bg, text_color="white", anchor="w", height=45, corner_radius=10, command=command)
        btn.pack(fill="x", padx=10, pady=5)

    def load_data(self):
        """Clears the table and reloads everything from the SQLite database."""
        # 1. Clear existing table (except headers)
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # 2. Rebuild headers
        for i, h in enumerate(self.headers):
            ctk.CTkLabel(self.table_frame, text=h, font=("Helvetica", 13, "bold"), text_color="gray").grid(row=0, column=i, padx=20, pady=15, sticky="nsew")
            self.table_frame.grid_columnconfigure(i, weight=1)

        # 3. Fetch data from database
        readers = database.get_all_readers()
        
        # 4. Populate table
        for row_idx, row_data in enumerate(readers, start=1):
            for col_idx, item in enumerate(row_data):
                ctk.CTkLabel(self.table_frame, text=str(item), text_color="black").grid(row=row_idx, column=col_idx, padx=5, pady=10)

    # --- MODAL: Add Reader ---

    def show_add_reader_modal(self):
        if hasattr(self, "modal") and self.modal.winfo_exists():
            return

        self.modal = ctk.CTkFrame(self.content_container, width=580, height=650, fg_color="#C4C4C4", corner_radius=20, border_width=1, border_color="#A0A0A0")
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        self.modal.pack_propagate(False)
        self.modal.grid_propagate(False)

        # BUTTON: Changed to call self.save_new_reader
        ctk.CTkButton(self.modal, text="Сохранить", fg_color="#7C9A82", width=180, height=35, command=self.save_new_reader).place(x=360, y=30)
        ctk.CTkButton(self.modal, text="Отмена", fg_color="transparent", text_color="black", hover_color="#A0A0A0", width=100, height=35, command=self.modal.destroy).place(x=250, y=30)

        # Profile Image
        profile_circle = ctk.CTkLabel(self.modal, text="👤", font=("Helvetica", 90), text_color="#7C9A82", width=130, height=130)
        profile_circle.place(x=80, y=120, anchor="center")

        # ENTRY: The text box to type the name!
        self.name_entry = ctk.CTkEntry(self.modal, placeholder_text="Введите ФИО", font=("Helvetica", 18), width=250, height=40, fg_color="#E0E0E0", text_color="black")
        self.name_entry.place(x=160, y=105, anchor="w")
        
        ctk.CTkLabel(self.modal, text="новый читатель", font=("Helvetica", 14), text_color="gray").place(x=160, y=150, anchor="w")

        # (I left the book tables blank here, since a new reader has no books yet)
        ctk.CTkLabel(self.modal, text="ТЕКУЩИЕ КНИГИ: Нет", font=("Helvetica", 14, "bold"), text_color="gray").place(x=40, y=210)
        ctk.CTkLabel(self.modal, text="ИСТОРИЯ ВЫДАЧ: Нет", font=("Helvetica", 14, "bold"), text_color="gray").place(x=40, y=360)

    def save_new_reader(self):
        """Gets text from the entry, saves to DB, and refreshes the table."""
        new_name = self.name_entry.get()
        
        if new_name.strip() != "":
            # 1. Save to SQLite
            database.add_reader(new_name)
            
            # 2. Refresh the UI Table to show the new person
            self.load_data()
            
            # 3. Close the modal
            self.modal.destroy()
        else:
            # Optionally change border color to red to show an error
            self.name_entry.configure(border_color="red", border_width=2)
import customtkinter as ctk
import database 

class ReaderPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

        # --- SIDEBAR --- (Same as before)
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#4A6550")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(pady=(30, 0))
        
        self.create_nav_btn("🏠 Главное", command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn("📋 Книжный фонд", command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn("👤 Читатель", is_active=True, command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn("🕒 Выдача/Возврат", command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn("📊 Отчеты", command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn("⚙️ Настройки", command=lambda: controller.show_frame("SettingsPage"))


        # --- RIGHT CONTENT CONTAINER ---
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Header
        self.header = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.search_bar = ctk.CTkEntry(self.header, placeholder_text="Поиск по всей базе...", width=450, height=40, corner_radius=20)
        self.search_bar.pack(side="left", padx=10)

        self.add_btn = ctk.CTkButton(self.header, text="ДОБАВИТЬ ЧИТАТЕЛЯ", fg_color="#7C9A82", height=40, command=self.show_add_reader_modal)
        self.add_btn.pack(side="left", padx=10)

        # --- TABLE SETUP ---
        self.table_frame = ctk.CTkFrame(self.content_container, fg_color="white", corner_radius=10)
        self.table_frame.pack(fill="both", expand=True, pady=10)

        self.headers = ["№ читателя", "ФИО читателя", "Кол-во книг", "Прочитанно"]
        
        # Load the initial data from the database
        self.load_data()

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color=bg, text_color="white", anchor="w", height=45, corner_radius=10, command=command)
        btn.pack(fill="x", padx=10, pady=5)

    def load_data(self):
        """Clears the table and reloads everything from the SQLite database."""
        # 1. Clear existing table (except headers)
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # 2. Rebuild headers
        for i, h in enumerate(self.headers):
            ctk.CTkLabel(self.table_frame, text=h, font=("Helvetica", 13, "bold"), text_color="gray").grid(row=0, column=i, padx=20, pady=15, sticky="nsew")
            self.table_frame.grid_columnconfigure(i, weight=1)

        # 3. Fetch data from database
        readers = database.get_all_readers()
        
        # 4. Populate table
        for row_idx, row_data in enumerate(readers, start=1):
            for col_idx, item in enumerate(row_data):
                ctk.CTkLabel(self.table_frame, text=str(item), text_color="black").grid(row=row_idx, column=col_idx, padx=5, pady=10)

    # --- MODAL: Add Reader ---

    def show_add_reader_modal(self):
        if hasattr(self, "modal") and self.modal.winfo_exists():
            return

        self.modal = ctk.CTkFrame(self.content_container, width=580, height=650, fg_color="#C4C4C4", corner_radius=20, border_width=1, border_color="#A0A0A0")
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        self.modal.pack_propagate(False)
        self.modal.grid_propagate(False)

        # BUTTON: Changed to call self.save_new_reader
        ctk.CTkButton(self.modal, text="Сохранить", fg_color="#7C9A82", width=180, height=35, command=self.save_new_reader).place(x=360, y=30)
        ctk.CTkButton(self.modal, text="Отмена", fg_color="transparent", text_color="black", hover_color="#A0A0A0", width=100, height=35, command=self.modal.destroy).place(x=250, y=30)

        # Profile Image
        profile_circle = ctk.CTkLabel(self.modal, text="👤", font=("Helvetica", 90), text_color="#7C9A82", width=130, height=130)
        profile_circle.place(x=80, y=120, anchor="center")

        # ENTRY: The text box to type the name!
        self.name_entry = ctk.CTkEntry(self.modal, placeholder_text="Введите ФИО", font=("Helvetica", 18), width=250, height=40, fg_color="#E0E0E0", text_color="black")
        self.name_entry.place(x=160, y=105, anchor="w")
        
        ctk.CTkLabel(self.modal, text="новый читатель", font=("Helvetica", 14), text_color="gray").place(x=160, y=150, anchor="w")

        # (I left the book tables blank here, since a new reader has no books yet)
        ctk.CTkLabel(self.modal, text="ТЕКУЩИЕ КНИГИ: Нет", font=("Helvetica", 14, "bold"), text_color="gray").place(x=40, y=210)
        ctk.CTkLabel(self.modal, text="ИСТОРИЯ ВЫДАЧ: Нет", font=("Helvetica", 14, "bold"), text_color="gray").place(x=40, y=360)

    def save_new_reader(self):
        """Gets text from the entry, saves to DB, and refreshes the table."""
        new_name = self.name_entry.get()
        
        if new_name.strip() != "":
            # 1. Save to SQLite
            database.add_reader(new_name)
            
            # 2. Refresh the UI Table to show the new person
            self.load_data()
            
            # 3. Close the modal
            self.modal.destroy()
        else:
            # Optionally change border color to red to show an error
            self.name_entry.configure(border_color="red", border_width=2)
