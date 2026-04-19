
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

        self.add_btn = ctk.CTkButton(self.header, text="ДОБАВИТЬ книгу", fg_color="#7C9A82", height=40)
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
