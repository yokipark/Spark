import customtkinter as ctk

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
        self.create_nav_btn("🕒 Выдача/Возврат", command=lambda: controller.show_frame("IssueReturnPage"))
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
