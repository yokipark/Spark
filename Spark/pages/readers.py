
import customtkinter as ctk
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
