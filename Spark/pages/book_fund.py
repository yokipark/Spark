import customtkinter as ctk
import database
import localization
class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

        # ==========================================
        # SIDEBAR (Широкий дизайн 370px)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=370, corner_radius=0, fg_color="#4A6550")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.sidebar_inner = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_inner.pack(fill="both", expand=True, padx=32, pady=(50, 25))

        self.logo_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.logo_zone.pack(side="top", fill="x", pady=(0, 40))
        ctk.CTkLabel(self.logo_zone, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(anchor="w")
        ctk.CTkLabel(self.logo_zone, text="библиотекаря", font=("Helvetica", 14), text_color="#E6C619").pack(anchor="w")

        self.nav_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.nav_zone.pack(side="top", fill="x")

        self.create_nav_btn(localization.get("main"), command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), is_active=True, command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn(localization.get("settings"), command=lambda: controller.show_frame("SettingsPage"))

        self.profile_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.profile_zone.pack(side="bottom", fill="x")
        ctk.CTkLabel(self.profile_zone, text=f"👤 СЕЗИМАЙ\n{localization.get("librarian")}", text_color="white", justify="left").pack(side="left")

        # ==========================================
        # RIGHT CONTENT
        # ==========================================
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # --- ШАПКА И ПОИСК ---
        self.header = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.search_bar = ctk.CTkEntry(self.header, placeholder_text=localization.get("Поиск по названию, автору или №..."), width=400, height=40, corner_radius=20, fg_color="#C4C4C4", text_color="black")
        self.search_bar.pack(side="left", padx=10)
        
        # ⚡ МАГИЯ ПОИСКА: Слушаем каждое нажатие клавиатуры!
        self.search_bar.bind("<KeyRelease>", self.perform_search)

        self.add_btn = ctk.CTkButton(self.header, text=localization.get("add_book"), fg_color="#7C9A82", text_color="black", height=40, command=self.show_add_book_modal)
        self.add_btn.pack(side="left", padx=10)

        self.export_btn = ctk.CTkOptionMenu(self.header, values=["Excel", "PDF"], fg_color="#D1C4A3", button_color="#D1C4A3", text_color="black", height=40)
        self.export_btn.set(localization.get("export"))
        self.export_btn.pack(side="right", padx=10)

        # --- ТАБЛИЦА ---
        self.table_frame = ctk.CTkFrame(self.content_container, fg_color="#C4C4C4", corner_radius=15, border_width=1, border_color="#A0A0A0")
        self.table_frame.pack(fill="both", expand=True, pady=10)

        self.headers = [
            localization.get("inv_num"),
            localization.get("book_title"),
            localization.get("author"),
            localization.get("genre"),
            localization.get("status"),
            localization.get("place")
        ]        
        # Загружаем все книги при старте
        self.load_data()

    # --- ЛОГИКА ---

    def perform_search(self, event):
        """Вызывается при каждом нажатии клавиши в строке поиска."""
        query = self.search_bar.get().strip()
        self.load_data(search_query=query)

    def load_data(self, search_query=""):
        """Загружает книги из БД. Если есть search_query, фильтрует их."""
        # Очищаем старые данные (кроме заголовков, но мы их перерисуем для надежности)
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Рисуем заголовки
        for i, h in enumerate(self.headers):
            ctk.CTkLabel(self.table_frame, text=h, font=("Helvetica", 13, "bold"), text_color="black").grid(row=0, column=i, padx=20, pady=15, sticky="nsew")
            self.table_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkFrame(self.table_frame, height=1, fg_color="#A0A0A0").grid(row=1, column=0, columnspan=6, sticky="ew")

        # Получаем данные из базы
        if search_query:
            books = database.search_books(search_query)
        else:
            books = database.get_all_books()

        # Рисуем строки
        for row_idx, row_data in enumerate(books, start=2):
            for col_idx, item in enumerate(row_data):
                if item in ["В наличии", "Выдана"]:
                    color = "#2E9E4A" if item == "В наличии" else "#B8A45F"
                    badge_frame = ctk.CTkFrame(self.table_frame, fg_color=color, corner_radius=10)
                    badge_frame.grid(row=row_idx, column=col_idx, padx=5, pady=5)
                    ctk.CTkLabel(badge_frame, text=item, text_color="white", font=("Helvetica", 12)).pack(padx=10, pady=2)
                else:
                    ctk.CTkLabel(self.table_frame, text=str(item), text_color="black", font=("Helvetica", 13)).grid(row=row_idx, column=col_idx, padx=5, pady=10)
            
            # Линия между строками
            ctk.CTkFrame(self.table_frame, height=1, fg_color="#A0A0A0").grid(row=row_idx*2+1, column=0, columnspan=6, sticky="ew")

    # --- МОДАЛЬНОЕ ОКНО ---

    def show_add_book_modal(self):
        if hasattr(self, "modal_frame") and self.modal_frame.winfo_exists():
            return

        self.modal_frame = ctk.CTkFrame(self.content_container, fg_color="#E8E8E8", corner_radius=15, border_width=1, border_color="#B0B0B0")
        self.modal_frame.place(relx=0.5, rely=0.4, anchor="center") 
        self.modal_frame.pack_propagate(False)
        self.modal_frame.configure(width=750, height=350)

        inner = ctk.CTkFrame(self.modal_frame, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(inner, text=localization.get("book_title"), text_color="black").grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w")
        ctk.CTkLabel(inner, text=localization.get("author"), text_color="black").grid(row=0, column=1, padx=10, pady=(0, 5), sticky="w")
        ctk.CTkLabel(inner, text=localization.get("inv_num"), text_color="black").grid(row=0, column=2, padx=10, pady=(0, 5), sticky="w")

        self.entry_title = ctk.CTkEntry(inner, width=220, height=45, fg_color="#D9D9D9", text_color="black")
        self.entry_title.grid(row=1, column=0, padx=10, pady=(0, 20))
        
        self.entry_author = ctk.CTkEntry(inner, width=220, height=45, fg_color="#D9D9D9", text_color="black")
        self.entry_author.grid(row=1, column=1, padx=10, pady=(0, 20))
        
        self.entry_id = ctk.CTkEntry(inner, width=150, height=45, fg_color="#D9D9D9", text_color="black")
        self.entry_id.grid(row=1, column=2, padx=10, pady=(0, 20))

        ctk.CTkLabel(inner, text=localization.get("genre"), text_color="black").grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")
        ctk.CTkLabel(inner, text=localization.get("place"), text_color="black").grid(row=2, column=1, padx=10, pady=(0, 5), sticky="w")

        self.entry_genre = ctk.CTkEntry(inner, width=220, height=45, fg_color="#D9D9D9", text_color="black")
        self.entry_genre.grid(row=3, column=0, padx=10, pady=(0, 30))
        
        self.entry_place = ctk.CTkEntry(inner, width=220, height=45, fg_color="#D9D9D9", text_color="black")
        self.entry_place.grid(row=3, column=1, padx=10, pady=(0, 30))

        ctk.CTkButton(inner, text=localization.get("add_book"), font=("Helvetica", 16, "bold"), fg_color="#B8A45F", text_color="black", 
                      width=160, height=50, command=self.save_new_book).grid(row=4, column=2, sticky="e")
        ctk.CTkButton(inner, text=localization.get("cancel"), fg_color="transparent", text_color="gray", hover_color="#D9D9D9", 
                      command=self.modal_frame.destroy).grid(row=4, column=1, sticky="e", padx=10)

    def save_new_book(self):
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        inv_no = self.entry_id.get().strip()
        genre = self.entry_genre.get().strip()
        place = self.entry_place.get().strip()

        if title and author and inv_no and genre and place:
            database.add_book(inv_no, title, author, genre, place)
            self.load_data() # Перезагружаем таблицу с новой книгой
            
            # Обновляем дашборд, так как книг стало больше!
            if "DashboardPage" in self.controller.frames:
                self.controller.frames["DashboardPage"].refresh_data()
                
            self.modal_frame.destroy()

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, text_color="white", 
                            anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", pady=5)
