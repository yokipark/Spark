import customtkinter as ctk
import database # Import our database logic

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#4A6550")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(pady=(30, 0))
        ctk.CTkLabel(self.sidebar, text="библиотекаря", font=("Helvetica", 14), text_color="#E6C619").pack(pady=(0, 30))

        self.create_nav_btn("🏠 Главное", command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn("📋 Книжный фонд", is_active=True, command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn("👤 Читатель", command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn("🕒 Выдача/Возврат", command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn("📊 Отчеты", command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn("⚙️ Настройки", command=lambda: controller.show_frame("SettingsPage"))

        # Profile
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

        # Connected to show_add_book_modal
        self.add_btn = ctk.CTkButton(self.header, text="ДОБАВИТЬ книгу", fg_color="#7C9A82", height=40, command=self.show_add_book_modal)
        self.add_btn.pack(side="left", padx=10)

        self.export_btn = ctk.CTkOptionMenu(self.header, values=["Excel", "PDF"], fg_color="#D1C4A3", button_color="#D1C4A3", text_color="black", height=40)
        self.export_btn.set("ЭКСПОРТ ⌄")
        self.export_btn.pack(side="right", padx=10)

        # 2. Filters
        self.filter_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.filter_frame.pack(fill="x", pady=10)
        for f in ["ЖАНРЫ", "АВТОРЫ", "ГОД", "СТАТУС"]:
            ctk.CTkOptionMenu(self.filter_frame, values=[f], fg_color="#C4C4C4", text_color="black", button_color="#C4C4C4", width=120).pack(side="left", padx=5)

        # 3. Table Setup
        self.table_frame = ctk.CTkFrame(self.content_container, fg_color="white", corner_radius=10)
        self.table_frame.pack(fill="both", expand=True, pady=10)

        self.headers = ["Инвертарный №", "Название книги", "Автор", "Жанр", "Статус", "Место"]
        
        # Load data from database on startup
        self.load_data()

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color=bg, text_color="white", anchor="w", height=45, corner_radius=10, command=command)
        btn.pack(fill="x", padx=10, pady=5)

    def load_data(self):
        """Fetches books from SQLite and builds the table with status badges"""
        # Clear existing table data
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Rebuild headers
        for i, h in enumerate(self.headers):
            ctk.CTkLabel(self.table_frame, text=h, font=("Helvetica", 13, "bold"), text_color="gray").grid(row=0, column=i, padx=20, pady=15, sticky="nsew")
            self.table_frame.grid_columnconfigure(i, weight=1)

        # Fetch from DB
        books = database.get_all_books()

        # Populate rows
        for row_idx, row_data in enumerate(books, start=1):
            for col_idx, item in enumerate(row_data):
                # The badge logic for the "Status" column (index 4)
                if item in ["В наличии", "Выдана"]:
                    color = "#7C9A82" if item == "В наличии" else "#B8A45F"
                    badge_frame = ctk.CTkFrame(self.table_frame, fg_color=color, corner_radius=10)
                    badge_frame.grid(row=row_idx, column=col_idx, padx=5, pady=5)
                    ctk.CTkLabel(badge_frame, text=item, text_color="white", font=("Helvetica", 12)).pack(padx=10, pady=2)
                else:
                    ctk.CTkLabel(self.table_frame, text=str(item), text_color="black", font=("Helvetica", 13)).grid(row=row_idx, column=col_idx, padx=5, pady=5)

    # --- Modal Methods ---
    def show_add_book_modal(self):
        if hasattr(self, "modal_frame") and self.modal_frame.winfo_exists():
            return

        self.modal_frame = ctk.CTkFrame(self.content_container, fg_color="#E8E8E8", corner_radius=15, border_width=1, border_color="#B0B0B0")
        self.modal_frame.place(relx=0.5, rely=0.4, anchor="center") 
        
        # Stop collapsing
        self.modal_frame.pack_propagate(False)
        self.modal_frame.configure(width=750, height=350)

        inner = ctk.CTkFrame(self.modal_frame, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        # Row 0: Labels
        ctk.CTkLabel(inner, text="Название книги", text_color="black").grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w")
        ctk.CTkLabel(inner, text="Автор", text_color="black").grid(row=0, column=1, padx=10, pady=(0, 5), sticky="w")
        ctk.CTkLabel(inner, text="Инвертарный №", text_color="black").grid(row=0, column=2, padx=10, pady=(0, 5), sticky="w")

        # Row 1: Top Entries
        self.entry_title = ctk.CTkEntry(inner, width=220, height=45, fg_color="#D9D9D9", text_color="black")
        self.entry_title.grid(row=1, column=0, padx=10, pady=(0, 20))
        
        self.entry_author = ctk.CTkEntry(inner, width=220, height=45, fg_color="#D9D9D9", text_color="black")
        self.entry_author.grid(row=1, column=1, padx=10, pady=(0, 20))
        
        self.entry_id = ctk.CTkEntry(inner, width=150, height=45, fg_color="#D9D9D9", text_color="black")
        self.entry_id.grid(row=1, column=2, padx=10, pady=(0, 20))

        # Row 2: Bottom Labels
        ctk.CTkLabel(inner, text="Жанр", text_color="black").grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")
        ctk.CTkLabel(inner, text="Место", text_color="black").grid(row=2, column=1, padx=10, pady=(0, 5), sticky="w")

        # Row 3: Bottom Entries
        self.entry_genre = ctk.CTkEntry(inner, width=220, height=45, fg_color="#D9D9D9", text_color="black")
        self.entry_genre.grid(row=3, column=0, padx=10, pady=(0, 30))
        
        self.entry_place = ctk.CTkEntry(inner, width=220, height=45, fg_color="#D9D9D9", text_color="black")
        self.entry_place.grid(row=3, column=1, padx=10, pady=(0, 30))

        # Row 4: Buttons
        ctk.CTkButton(inner, text="ДОБАВИТЬ", font=("Helvetica", 16, "bold"), fg_color="#B8A45F", hover_color="#9A884B", 
                      text_color="white", width=160, height=50, command=self.save_new_book).grid(row=4, column=2, sticky="e")
        ctk.CTkButton(inner, text="Отмена", fg_color="transparent", text_color="gray", hover_color="#D9D9D9", 
                      command=self.modal_frame.destroy).grid(row=4, column=1, sticky="e", padx=10)

    def save_new_book(self):
        """Gathers data, sends it to the DB, and refreshes the view."""
        title = self.entry_title.get()
        author = self.entry_author.get()
        inv_no = self.entry_id.get()
        genre = self.entry_genre.get()
        place = self.entry_place.get()

        # Basic check to make sure fields aren't empty
        if title and author and inv_no and genre and place:
            database.add_book(inv_no, title, author, genre, place)
            self.load_data()            # Refresh table
            self.modal_frame.destroy()  # Close popup
        else:
            print("Please fill out all fields!") # Or display an error label to the user
