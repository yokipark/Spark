import customtkinter as ctk

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Система Картотеки")
        self.geometry("1440x1024")
        self.configure(fg_color="#4A6550")

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(side="top", fill="both", expand=True)

    
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for PageClass in (LoginPage, MainPage, DashboardPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        #Main card
        self.main_card = ctk.CTkFrame(
            self, 
            width=516, 
            height=732, 
            fg_color="#cfd2d0", 
            corner_radius=20
        )
        self.main_card.place(relx=0.5, rely=0.5, anchor="center")


        # Title
        self.title_label = ctk.CTkLabel(
            self.main_card,
            text="Картотека", 
            font=("Helvetica", 28, "bold"), 
            text_color="black"
        )
        self.title_label.place(x=258, y=190, anchor="center")

        self.subtitle = ctk.CTkLabel(
            self.main_card, 
            text="Библиотекаря", 
            font=("Helvetica", 16), 
            text_color="black"
        )
        self.subtitle.place(x=258, y=220, anchor="center")


        # ID Entry
        self.idsotrudnika = ctk.CTkLabel(
            self.main_card, 
            text="ID сотрудника", 
            font=("Helvetica", 12), 
            text_color="black"
        )

        self.idsotrudnika.place(x=68, y=300, anchor="w")

        self.id_entry = ctk.CTkEntry(
            self.main_card, 
            width=380, height=45, 
            fg_color="#bebebe", border_color="#bebebe", text_color="black", corner_radius=10
        )
        self.id_entry.place(x=258, y=335, anchor="center")

        # Password Entry
        self.pass_label = ctk.CTkLabel(
            self.main_card, 
            text="Пароль", 
            font=("Helvetica", 12), 
            text_color="black"
        )
        self.pass_label.place(x=68, y=390, anchor="w")

        self.pass_entry = ctk.CTkEntry(
            self.main_card, 
            width=380, height=45, 
            fg_color="#bebebe", border_color="#bebebe", text_color="black", corner_radius=10, 
            show="*"
        )
        self.pass_entry.place(x=258, y=425, anchor="center")

        # Login Button
        self.login_button = ctk.CTkButton(
            self.main_card, 
            text="ВОЙТИ", 
            width=360, height=50, 
            font=("Helvetica", 18, "bold"), 
            fg_color="#304146", hover_color="#1f2c30",
            text_color="white", corner_radius=15,
            command=self.login_action
        )
        self.login_button.place(x=258, y=550, anchor="center")

    def login_action(self):
        # Switch to MainPage when clicked
        self.controller.show_frame("DashboardPage")

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
        """Creates the labels and badges for a single row in the table"""
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
class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

        #  Sidebar 
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#4A6550")
        self.sidebar.pack(side="left", fill="y")

        # Sidebar Title
        ctk.CTkLabel(self.sidebar, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(pady=(30, 0))
        ctk.CTkLabel(self.sidebar, text="библиотекаря", font=("Helvetica", 14), text_color="#E6C619").pack(pady=(0, 30))

        # sidebar buttons 
        self.create_nav_btn("🏠 Главное", is_active=True, command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn("📋 Книжный фонд", command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn("👤 Читатель", command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn("🕒 Выдача/Возврат")
        self.create_nav_btn("📊 Отчеты")
        self.create_nav_btn("⚙️ Настройки")

        # profile
        profile_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        profile_frame.pack(side="bottom", pady=20, padx=20, fill="x")
        ctk.CTkLabel(profile_frame, text="👤 СЕЗИМАЙ\nБиблиотекарь", text_color="white", justify="left").pack(side="left")


        # *** Right Content ***
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # HEADER
        self.create_header(self.right_container)

        # Stats Row
        self.stats_frame = ctk.CTkFrame(self.right_container, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=10)
        self.create_stat_card(self.stats_frame, "Книг на руках", "127", "✅", 0)
        self.create_stat_card(self.stats_frame, "Просрочено", "54", "❗", 1)
        self.create_stat_card(self.stats_frame, "Новые читатели", "19", "👤", 2)

        #Graph Placeholder
        self.middle_row = ctk.CTkFrame(self.right_container, fg_color="transparent")
        self.middle_row.pack(fill="both", expand=True, pady=10)
        self.middle_row.grid_columnconfigure(0, weight=3)
        self.middle_row.grid_columnconfigure(1, weight=1)

        self.graph_box = ctk.CTkFrame(self.middle_row, fg_color="#C4C4C4", corner_radius=15)
        self.graph_box.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        ctk.CTkLabel(self.graph_box, text="Активность за неделю", font=("Helvetica", 16, "bold"), text_color="black").pack(pady=10)

        self.actions_box = ctk.CTkFrame(self.middle_row, fg_color="#C4C4C4", corner_radius=15)
        self.actions_box.grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(self.actions_box, text="Быстрые действия", font=("Helvetica", 16, "bold"), text_color="black").pack(pady=10)
        
        for action in ["Быстрая выдача", "Принять возврат", "Добавить читателя"]:
            ctk.CTkButton(self.actions_box, text=action, fg_color="#4A6550", height=40, corner_radius=20).pack(pady=5, padx=20, fill="x")

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color=bg, text_color="white", 
                            anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", padx=10, pady=5)

    def create_stat_card(self, parent, title, value, icon, col):
        card = ctk.CTkFrame(parent, fg_color="#C4C4C4", height=150, corner_radius=15)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        ctk.CTkLabel(card, text=title, font=("Helvetica", 16), text_color="black").place(x=20, y=20)
        ctk.CTkLabel(card, text=value, font=("Helvetica", 48, "bold"), text_color="black").place(x=20, y=60)
        ctk.CTkLabel(card, text=icon, font=("Helvetica", 32)).place(relx=0.8, rely=0.5, anchor="center")

    def create_header(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkEntry(header, placeholder_text="Поиск...", width=400, height=40, corner_radius=20).pack(side="left")
        ctk.CTkButton(header, text="ЭКСПОРТ ⌄", fg_color="#D1C4A3", text_color="black", width=100, height=40).pack(side="right")
        ctk.CTkButton(header, text="ДОБАВИТЬ КНИГУ", fg_color="#7C9A82", height=40).pack(side="right", padx=10)

class ReaderPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#4A6550")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(pady=(30, 0))
        ctk.CTkLabel(self.sidebar, text="библиотекаря", font=("Helvetica", 14), text_color="#E6C619").pack(pady=(0, 30))

        # sidebar buttons 
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

        # RIGHT CONTENT CONTAINER
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Header
        self.header = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.search_bar = ctk.CTkEntry(self.header, placeholder_text="Поиск по всей базе(название, автор, ISBN)", width=450, height=40, corner_radius=20)
        self.search_bar.pack(side="left", padx=10)

        self.add_btn = ctk.CTkButton(self.header, text="ДОБАВИТЬ ЧИТАТЕЛЯ", fg_color="#7C9A82", height=40)
        self.add_btn.pack(side="left", padx=10)

        self.export_btn = ctk.CTkOptionMenu(self.header, values=["Excel", "PDF"], fg_color="#D1C4A3", button_color="#D1C4A3", text_color="black", height=40)
        self.export_btn.set("ЭКСПОРТ ⌄")
        self.export_btn.pack(side="right", padx=10)

        # Table
        self.table_frame = ctk.CTkFrame(self.content_container, fg_color="white", corner_radius=10)
        self.table_frame.pack(fill="both", expand=True, pady=10)

        headers = ["№ читателя", "ФИО читателя", "Количество книг на руках", "Прочитанно"]
        for i, h in enumerate(headers):
            lbl = ctk.CTkLabel(self.table_frame, text=h, font=("Helvetica", 13, "bold"), text_color="gray")
            lbl.grid(row=0, column=i, padx=20, pady=15, sticky="nsew")
            self.table_frame.grid_columnconfigure(i, weight=1)

  
        self.add_table_row(1, ["98755", "Акылбекова Айпери", "5", "15"])
        self.add_table_row(2, ["75444", "Булазова Шахида", "1", "10"])


    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color=bg, text_color="white", 
                            anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", padx=10, pady=5)

    def add_table_row(self, row_idx, data):
        for i, item in enumerate(data):

            lbl = ctk.CTkLabel(self.table_frame, text=item, text_color="black", font=("Helvetica", 13))
            lbl.grid(row=row_idx, column=i, padx=5, pady=10)


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
