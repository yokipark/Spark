import customtkinter as ctk

class ReaderPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#4A6550")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(pady=(30, 0))
        ctk.CTkLabel(self.sidebar, text="библиотекаря", font=("Helvetica", 14), text_color="#E6C619").pack(pady=(0, 30))

        self.create_nav_btn("🏠 Главное", command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn("📋 Книжный фонд", command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn("👤 Читатель", is_active=True, command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn("🕒 Выдача/Возврат")
        self.create_nav_btn("📊 Отчеты")
        self.create_nav_btn("⚙️ Настройки")

        # Profile at bottom
        self.profile_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.profile_frame.pack(side="bottom", pady=20, padx=20, fill="x")
        ctk.CTkLabel(self.profile_frame, text="👤 СЕЗИМАЙ\nБиблиотекарь", text_color="white", justify="left").pack(side="left")

        # --- RIGHT CONTENT CONTAINER ---
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # 1. Header
        self.header = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.search_bar = ctk.CTkEntry(self.header, placeholder_text="Поиск по всей базе...", width=450, height=40, corner_radius=20)
        self.search_bar.pack(side="left", padx=10)

        # LINKED BUTTON: command=self.show_reader_details
        self.add_btn = ctk.CTkButton(self.header, text="ДОБАВИТЬ ЧИТАТЕЛЯ", fg_color="#7C9A82", height=40, command=self.show_reader_details)
        self.add_btn.pack(side="left", padx=10)

        self.export_btn = ctk.CTkOptionMenu(self.header, values=["Excel", "PDF"], fg_color="#D1C4A3", button_color="#D1C4A3", text_color="black", height=40)
        self.export_btn.set("ЭКСПОРТ ⌄")
        self.export_btn.pack(side="right", padx=10)

        # 2. Main Reader Table (The background list)
        self.table_frame = ctk.CTkFrame(self.content_container, fg_color="white", corner_radius=10)
        self.table_frame.pack(fill="both", expand=True, pady=10)

        headers = ["№ читателя", "ФИО читателя", "Кол-во книг", "Прочитанно"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.table_frame, text=h, font=("Helvetica", 13, "bold"), text_color="gray").grid(row=0, column=i, padx=20, pady=15, sticky="nsew")
            self.table_frame.grid_columnconfigure(i, weight=1)

        self.add_table_row(1, ["98755", "Акылбекова Айпери", "5", "15"])
        self.add_table_row(2, ["75444", "Булазова Шахида", "1", "10"])

    # --- Helper Methods ---

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color=bg, text_color="white", anchor="w", height=45, corner_radius=10, command=command)
        btn.pack(fill="x", padx=10, pady=5)

    def add_table_row(self, row_idx, data):
        for i, item in enumerate(data):
            ctk.CTkLabel(self.table_frame, text=item, text_color="black").grid(row=row_idx, column=i, padx=5, pady=10)

    # --- Reader Profile Modal ---

    def show_reader_details(self):
        if hasattr(self, "modal") and self.modal.winfo_exists():
            return

        # Main Modal Background
        self.modal = ctk.CTkFrame(self.content_container, width=580, height=650, fg_color="#C4C4C4", corner_radius=20, border_width=1, border_color="#A0A0A0")
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        
        # 🛡️ THE GUARDIANS: These stop the modal from collapsing or hiding elements
        self.modal.pack_propagate(False)
        self.modal.grid_propagate(False)

        # Top Right Button
        ctk.CTkButton(self.modal, text="Добавить читателя", fg_color="#7C9A82", width=180, height=35, command=self.modal.destroy).place(x=360, y=30)

        # Profile Image (FIXED: Added explicit width/height to stop clipping)
        profile_circle = ctk.CTkLabel(self.modal, text="👤", font=("Helvetica", 90), text_color="#7C9A82", width=130, height=130)
        profile_circle.place(x=80, y=120, anchor="center")

        # Name Labels
        ctk.CTkLabel(self.modal, text="АННА\nАлексеевна", font=("Helvetica", 24, "bold"), text_color="black", justify="left").place(x=160, y=105, anchor="w")
        ctk.CTkLabel(self.modal, text="читатель", font=("Helvetica", 14), text_color="gray").place(x=160, y=150, anchor="w")

        # --- Section: ТЕКУЩИЕ КНИГИ ---
        ctk.CTkLabel(self.modal, text="ТЕКУЩИЕ КНИГИ", font=("Helvetica", 14, "bold"), text_color="black").place(x=40, y=210)
        
        # Sub-table 1 (FIXED: Added width, height, and grid_propagate)
        table1 = ctk.CTkFrame(self.modal, fg_color="white", corner_radius=5, width=500, height=100)
        table1.place(x=40, y=240)
        table1.grid_propagate(False) 
        
        # Header Row
        ctk.CTkLabel(table1, text="Название книги", text_color="gray", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(table1, text="Срок возврата", text_color="gray", font=("Helvetica", 12, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="e")
        table1.grid_columnconfigure(0, weight=1)
        
        # Data Rows
        ctk.CTkLabel(table1, text="Мертвые души", text_color="black").grid(row=1, column=0, padx=10, sticky="w")
        ctk.CTkLabel(table1, text="Просрочено", text_color="#8B0000").grid(row=1, column=1, padx=10, sticky="e") # Dark red
        
        ctk.CTkLabel(table1, text="Маленький принц", text_color="black").grid(row=2, column=0, padx=10, sticky="w")
        ctk.CTkLabel(table1, text="11 янв", text_color="black").grid(row=2, column=1, padx=10, sticky="e")

        # --- Section: ИСТОРИЯ ВЫДАЧ ---
        ctk.CTkLabel(self.modal, text="ИСТОРИЯ ВЫДАЧ", font=("Helvetica", 14, "bold"), text_color="black").place(x=40, y=360)
        
        # Sub-table 2 (FIXED: Added width, height, and pack_propagate)
        table2 = ctk.CTkFrame(self.modal, fg_color="#D1D1D1", corner_radius=5, width=500, height=120)
        table2.place(x=40, y=390)
        table2.pack_propagate(False)

        ctk.CTkLabel(table2, text="Название книги", text_color="gray", font=("Helvetica", 12)).pack(anchor="w", padx=10, pady=2)
        ctk.CTkLabel(table2, text="Красное яблоко", text_color="black").pack(anchor="w", padx=10, pady=2)
        ctk.CTkLabel(table2, text="Гордость и предубеждение", text_color="black").pack(anchor="w", padx=10, pady=2)
