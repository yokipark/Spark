import customtkinter as ctk

class IssueReturnPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#4A6550")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(pady=(30, 0))
        ctk.CTkLabel(self.sidebar, text="библиотекаря", font=("Helvetica", 14), text_color="#E6C619").pack(pady=(0, 30))

        # Notice: 'Выдача/Возврат' is now active!
        self.create_nav_btn("🏠 Главное", command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn("📋 Книжный фонд", command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn("👤 Читатель", command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn("🕒 Выдача/Возврат", is_active=True, command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn("📊 Отчеты")
        self.create_nav_btn("⚙️ Настройки")

        # Profile at bottom
        self.profile_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.profile_frame.pack(side="bottom", pady=20, padx=20, fill="x")
        ctk.CTkLabel(self.profile_frame, text="👤 СЕЗИМАЙ\nБиблиотекарь", text_color="white", justify="left").pack(side="left")

        # --- RIGHT CONTENT CONTAINER ---
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # 1. Header
        self.header = ctk.CTkFrame(self.content, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 10))

        self.search_bar = ctk.CTkEntry(self.header, placeholder_text="Поиск по всей базе...", width=450, height=40, corner_radius=20)
        self.search_bar.pack(side="left", padx=10)

        self.add_btn = ctk.CTkButton(self.header, text="ДОБАВИТЬ КНИГУ", fg_color="#7C9A82", height=40)
        self.add_btn.pack(side="left", padx=10)

        self.export_btn = ctk.CTkOptionMenu(self.header, values=["Excel", "PDF"], fg_color="#D1C4A3", button_color="#D1C4A3", text_color="black", height=40)
        self.export_btn.set("ЭКСПОРТ ⌄")
        self.export_btn.pack(side="right", padx=10)

        # --- MAIN SPLIT LAYOUT ---
        # We use a grid to split the main area into Left (Reader) and Right (Book) columns
        self.body = ctk.CTkFrame(self.content, fg_color="transparent")
        self.body.pack(fill="both", expand=True, pady=10)
        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_columnconfigure(1, weight=1)

        # ==========================================
        # LEFT COLUMN: Reader Info
        # ==========================================
        left_col = ctk.CTkFrame(self.body, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(left_col, text="ЧИТАТЕЛЯ", font=("Helvetica", 22, "bold"), text_color="black").pack(anchor="w", pady=(0, 10))

        # Reader ID / Book ID Inputs
        inputs_frame = ctk.CTkFrame(left_col, fg_color="transparent")
        inputs_frame.pack(fill="x", pady=(0, 20))
        
        id_frame1 = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        id_frame1.pack(side="left", padx=(0, 20))
        ctk.CTkLabel(id_frame1, text="Код читателя", text_color="black", font=("Helvetica", 14)).pack(anchor="w")
        ctk.CTkEntry(id_frame1, width=180, height=40, corner_radius=10, fg_color="#C4C4C4", border_color="#A0A0A0").pack()

        id_frame2 = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        id_frame2.pack(side="left")
        ctk.CTkLabel(id_frame2, text="Код книги", text_color="black", font=("Helvetica", 14)).pack(anchor="w")
        ctk.CTkEntry(id_frame2, width=180, height=40, corner_radius=10, fg_color="#C4C4C4", border_color="#A0A0A0").pack()

        ctk.CTkLabel(left_col, text="ФИО", font=("Helvetica", 22, "bold"), text_color="black").pack(anchor="w", pady=(10, 5))

        # Profile & Date section (Side by side)
        profile_date_frame = ctk.CTkFrame(left_col, fg_color="transparent")
        profile_date_frame.pack(fill="both", expand=True)

        # Profile Card
        profile_card = ctk.CTkFrame(profile_date_frame, fg_color="#C4C4C4", corner_radius=15, width=250)
        profile_card.pack(side="left", fill="y", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(profile_card, text="👤", font=("Helvetica", 90), text_color="#7C9A82").pack(pady=(20, 0))
        ctk.CTkLabel(profile_card, text="СЕЗИМАЙ\nБиблиотекарь", text_color="gray", font=("Helvetica", 12)).pack()
        
        ctk.CTkLabel(profile_card, text="Книги на руках", font=("Helvetica", 14, "bold"), text_color="black").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(profile_card, text="Мертвые души\nМаленький принц\nИстория искусств", font=("Helvetica", 14), text_color="black", justify="left").pack(anchor="w", padx=20)

        # Date Card
        date_card = ctk.CTkFrame(profile_date_frame, fg_color="#C4C4C4", corner_radius=15, width=150, height=120)
        date_card.pack(side="left", anchor="n")
        date_card.pack_propagate(False)
        ctk.CTkLabel(date_card, text="ДАТА", font=("Helvetica", 14, "bold"), text_color="black").pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkEntry(date_card, width=120, height=35, corner_radius=10, fg_color="#D9D9D9", border_width=1, border_color="#A0A0A0").pack(padx=15)

        # ==========================================
        # RIGHT COLUMN: Book Actions
        # ==========================================
        right_col = ctk.CTkFrame(self.body, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # Big Book Card
        book_card = ctk.CTkFrame(right_col, fg_color="#C4C4C4", corner_radius=15)
        book_card.pack(fill="x", pady=(35, 10)) # Added padding top to align with left column

        ctk.CTkLabel(book_card, text="КНИГА", font=("Helvetica", 22, "bold"), text_color="black").pack(anchor="w", padx=20, pady=(20, 10))

        book_inputs = ctk.CTkFrame(book_card, fg_color="transparent")
        book_inputs.pack(fill="x", padx=20, pady=(0, 20))

        b_id_frame = ctk.CTkFrame(book_inputs, fg_color="transparent")
        b_id_frame.pack(side="left", padx=(0, 20))
        ctk.CTkLabel(b_id_frame, text="Код книги", text_color="black", font=("Helvetica", 14)).pack(anchor="w")
        ctk.CTkEntry(b_id_frame, width=180, height=40, corner_radius=10, fg_color="#D9D9D9", border_color="#A0A0A0").pack()

        b_name_frame = ctk.CTkFrame(book_inputs, fg_color="transparent")
        b_name_frame.pack(side="left")
        ctk.CTkLabel(b_name_frame, text="Название", text_color="black", font=("Helvetica", 14)).pack(anchor="w")
        ctk.CTkEntry(b_name_frame, width=220, height=40, corner_radius=10, fg_color="#D9D9D9", border_color="#A0A0A0").pack()

        # Action Buttons
        ctk.CTkButton(book_card, text="Оформить выдачу", fg_color="#8A9E8A", hover_color="#6D826D", text_color="black", font=("Helvetica", 16, "bold"), height=50, corner_radius=10).pack(fill="x", padx=20, pady=(10, 5))
        ctk.CTkButton(book_card, text="Оформить возврат", fg_color="#B09B66", hover_color="#917E4D", text_color="black", font=("Helvetica", 16, "bold"), height=50, corner_radius=10).pack(fill="x", padx=20, pady=(5, 20))

        # History Card
        history_card = ctk.CTkFrame(right_col, fg_color="#C4C4C4", corner_radius=15)
        history_card.pack(fill="both", expand=True, pady=(10, 0))
        
        ctk.CTkLabel(history_card, text="История", font=("Helvetica", 16, "bold"), text_color="black").pack(anchor="w", padx=20, pady=(15, 5))
        history_text = "90001\n90021\n12005\n89045"
        ctk.CTkLabel(history_card, text=history_text, font=("Helvetica", 24), text_color="black", justify="left").pack(anchor="w", padx=20)

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color=bg, text_color="white", anchor="w", height=45, corner_radius=10, command=command)
        btn.pack(fill="x", padx=10, pady=5)
