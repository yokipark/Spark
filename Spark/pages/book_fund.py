import customtkinter as ctk
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
        self.create_nav_btn("🕒 Выдача/Возврат")
        self.create_nav_btn("📊 Отчеты")
        self.create_nav_btn("⚙️ Настройки")

        # RIGHT CONTENT CONTAINER
        
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # 1. Header (Search + Buttons)
        self.header = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.search_bar = ctk.CTkEntry(self.header, placeholder_text="Поиск по всей базе...", width=450, height=40, corner_radius=20)
        self.search_bar.pack(side="left", padx=10)

        self.add_btn = ctk.CTkButton(self.header, text="ДОБАВИТЬ книгу", fg_color="#7C9A82", height=40, command=self.show_add_book_modal)
        self.add_btn.pack(side="left", padx=10)

        self.export_btn = ctk.CTkOptionMenu(self.header, values=["Excel", "PDF"], fg_color="#D1C4A3", button_color="#D1C4A3", text_color="black", height=40)
        self.export_btn.set("ЭКСПОРТ ⌄")
        self.export_btn.pack(side="right", padx=10)

        # Filters
        self.filter_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.filter_frame.pack(fill="x", pady=10)
        for f in ["ЖАНРЫ", "АВТОРЫ", "ГОД", "СТАТУС"]:
            ctk.CTkOptionMenu(self.filter_frame, values=[f], fg_color="#C4C4C4", text_color="black", button_color="#C4C4C4", width=120).pack(side="left", padx=5)

        # THE TABLE 
        self.table_frame = ctk.CTkFrame(self.content_container, fg_color="white", corner_radius=10)
        
        self.table_frame.pack(fill="both", expand=True, pady=10)

        
        headers = ["Инвертарный №", "Название книги", "Автор", "Жанр", "Статус", "Место"]
        for i, h in enumerate(headers):
            lbl = ctk.CTkLabel(self.table_frame, text=h, font=("Helvetica", 13, "bold"), text_color="gray")
            lbl.grid(row=0, column=i, padx=20, pady=15, sticky="nsew")
            self.table_frame.grid_columnconfigure(i, weight=1)

        
        self.add_table_row(1, ["90001", "Зимний вечер", "А.С. Пушкин", "Новелл", "В наличии", "4"])
        self.add_table_row(2, ["89045", "Джамиля", "Ч. Айтматов", "Новелл", "Выдана", "27"])

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color=bg, text_color="white", 
                            anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", padx=10, pady=5)

    def add_table_row(self, row_idx, data):
        for i, item in enumerate(data):
            
            if item == "В наличии" or item == "Выдана":
                color = "#7C9A82" if item == "В наличии" else "#B8A45F"
                badge_frame = ctk.CTkFrame(self.table_frame, fg_color=color, corner_radius=10)
                badge_frame.grid(row=row_idx, column=i, padx=5, pady=5)
                
                lbl = ctk.CTkLabel(badge_frame, text=item, text_color="white", font=("Helvetica", 12))
                lbl.pack(padx=10, pady=2)
            else:
                lbl = ctk.CTkLabel(self.table_frame, text=item, text_color="black", font=("Helvetica", 13))
                lbl.grid(row=row_idx, column=i, padx=5, pady=5)
    def show_add_book_modal(self):
        # Prevent opening multiple modals if clicked twice
        if hasattr(self, "modal_frame") and self.modal_frame.winfo_exists():
            return

        # 1. Create the dark shadow/background (Optional, but looks nice)
        self.modal_frame = ctk.CTkFrame(self.content_container, fg_color="#E8E8E8", corner_radius=15, border_width=1, border_color="#B0B0B0")
        
        # .place lets us hover it over everything in the exact center
        self.modal_frame.place(relx=0.5, rely=0.4, anchor="center") 

        # Inner padding frame
        inner = ctk.CTkFrame(self.modal_frame, fg_color="transparent")
        inner.pack(padx=40, pady=40)

        # 2. Add the Labels
        ctk.CTkLabel(inner, text="Введите название книги", text_color="black", font=("Helvetica", 14)).grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w")
        ctk.CTkLabel(inner, text="Введите автора", text_color="black", font=("Helvetica", 14)).grid(row=0, column=1, padx=10, pady=(0, 5), sticky="w")
        ctk.CTkLabel(inner, text="Инвертарный №", text_color="black", font=("Helvetica", 14)).grid(row=0, column=2, padx=10, pady=(0, 5), sticky="w")

        # 3. Add the Entry Boxes
        self.entry_title = ctk.CTkEntry(inner, width=200, height=45, fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black", corner_radius=10)
        self.entry_title.grid(row=1, column=0, padx=10, pady=(0, 50))

        self.entry_author = ctk.CTkEntry(inner, width=200, height=45, fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black", corner_radius=10)
        self.entry_author.grid(row=1, column=1, padx=10, pady=(0, 50))

        self.entry_id = ctk.CTkEntry(inner, width=150, height=45, fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black", corner_radius=10)
        self.entry_id.grid(row=1, column=2, padx=10, pady=(0, 50))

        # 4. Add the Gold Action Button
        # The command uses a lambda to first destroy the popup, then you could link logic to add it to the table!
        add_btn = ctk.CTkButton(inner, text="ДОБАВИТЬ", font=("Helvetica", 16, "bold"), fg_color="#B8A45F", hover_color="#9A884B", 
                                text_color="white", width=160, height=50, corner_radius=10, command=self.close_modal)
        add_btn.grid(row=2, column=2, sticky="e")
        
        # Adding a close button for good UX (Optional, uncomment if you want a way to cancel)
        # ctk.CTkButton(inner, text="Отмена", fg_color="transparent", text_color="gray", hover_color="#D9D9D9", command=self.close_modal).grid(row=2, column=1, sticky="e", padx=10)

    def close_modal(self):
        # Destroys the popup and returns to the normal screen
        if hasattr(self, "modal_frame") and self.modal_frame.winfo_exists():
            self.modal_frame.destroy()
