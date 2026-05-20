import customtkinter as ctk
import localization
class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

                # ==========================================
        # 1. SIDEBAR BACKGROUND (Width: 370px)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=370, corner_radius=0, fg_color="#4A6550")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) # Locks the width exactly to 370

        # ==========================================
        # 2. INNER PADDING (Figma Specs: 32, 50, 25)
        # ==========================================
        self.sidebar_inner = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        # padx=32 (left/right), pady=(50, 25) (top 50, bottom 25)
        self.sidebar_inner.pack(fill="both", expand=True, padx=32, pady=(50, 25))

        # ==========================================
        # ZONE A: TOP (Logo)
        # ==========================================
        self.logo_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.logo_zone.pack(side="top", fill="x", pady=(0, 40)) # 40px gap below the logo
        
        ctk.CTkLabel(self.logo_zone, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(anchor="w")
        ctk.CTkLabel(self.logo_zone, text="библиотекаря", font=("Helvetica", 14), text_color="#E6C619").pack(anchor="w")

        # ==========================================
        # ZONE B: MIDDLE (Navigation Buttons)
        # ==========================================
        self.nav_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.nav_zone.pack(side="top", fill="x")

        self.create_nav_btn(localization.get("main"), command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), is_active=True, command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn(localization.get("settings"), command=lambda: controller.show_frame("SettingsPage"))

        # ==========================================
        # ZONE C: BOTTOM (Profile)
        # ==========================================
        self.profile_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        # side="bottom" forces this to stay at the very bottom, respecting the 25px bottom padding!
        self.profile_zone.pack(side="bottom", fill="x")
        
        ctk.CTkLabel(self.profile_zone, text="👤 СЕЗИМАЙ\nБиблиотекарь", text_color="white", justify="left").pack(side="left")

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

        # 2. Date Filter
        self.date_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.date_frame.pack(fill="x", pady=(10, 20), padx=10)
        
        ctk.CTkLabel(self.date_frame, text="январь   2025", fg_color="#A8ADA8", text_color="black", corner_radius=15, width=150, height=35).pack(side="left")
        ctk.CTkLabel(self.date_frame, text=" - ", text_color="black", font=("Helvetica", 16, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(self.date_frame, text="декабрь   2025", fg_color="#A8ADA8", text_color="black", corner_radius=15, width=150, height=35).pack(side="left")

        # --- DASHBOARD GRID ---
        self.dashboard = ctk.CTkFrame(self.content, fg_color="transparent")
        self.dashboard.pack(fill="both", expand=True)

        # TOP ROW
        top_row = ctk.CTkFrame(self.dashboard, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 10))

        # Card 1: Total Issued
        card_total = ctk.CTkFrame(top_row, fg_color="#C4C4C4", corner_radius=15, height=220)
        card_total.pack(side="left", fill="both", expand=True, padx=10)
        card_total.pack_propagate(False)
        ctk.CTkLabel(card_total, text="ВСЕГО\nВЫДАНО", font=("Helvetica", 18, "bold"), text_color="black", justify="left").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(card_total, text="2 348", font=("Helvetica", 36), text_color="black").pack(anchor="w", padx=20)
        
        # Mini Bar Chart using Canvas
        bar_canvas = ctk.CTkCanvas(card_total, width=200, height=80, bg="#C4C4C4", highlightthickness=0)
        bar_canvas.pack(anchor="w", padx=20, pady=10)
        bar_canvas.create_line(10, 70, 190, 70, fill="black", width=1) # Baseline
        bar_canvas.create_line(30, 60, 30, 70, fill="#E6C619", width=2) # Yellow
        bar_canvas.create_line(70, 30, 70, 70, fill="#C13C3C", width=2) # Red
        bar_canvas.create_line(110, 20, 110, 70, fill="#E6C619", width=2) # Yellow
        bar_canvas.create_line(150, 40, 150, 70, fill="#E6C619", width=2) # Yellow
        bar_canvas.create_line(190, 10, 190, 70, fill="#2E9E4A", width=2) # Green

        # Middle Column (New Books / New Readers)
        mid_col = ctk.CTkFrame(top_row, fg_color="transparent")
        mid_col.pack(side="left", fill="y", padx=10)
        
        card_new_books = ctk.CTkFrame(mid_col, fg_color="#C4C4C4", corner_radius=15, width=180, height=105)
        card_new_books.pack(pady=(0, 10))
        card_new_books.pack_propagate(False)
        ctk.CTkLabel(card_new_books, text="НОВЫХ КНИГ", font=("Helvetica", 16, "bold"), text_color="black").pack(anchor="w", padx=15, pady=(15, 0))
        ctk.CTkLabel(card_new_books, text="15", font=("Helvetica", 32), text_color="black").pack(anchor="w", padx=15)

        card_new_readers = ctk.CTkFrame(mid_col, fg_color="#C4C4C4", corner_radius=15, width=180, height=105)
        card_new_readers.pack()
        card_new_readers.pack_propagate(False)
        ctk.CTkLabel(card_new_readers, text="НОВЫХ\nЧИТАТЕЛЕЙ", font=("Helvetica", 16, "bold"), text_color="black", justify="left").pack(anchor="w", padx=15, pady=(10, 0))
        ctk.CTkLabel(card_new_readers, text="27", font=("Helvetica", 32), text_color="black").pack(anchor="w", padx=15)

        # Card 3: Popular Genres
        card_genres = ctk.CTkFrame(top_row, fg_color="#C4C4C4", corner_radius=15, height=220)
        card_genres.pack(side="left", fill="both", expand=True, padx=10)
        card_genres.pack_propagate(False)
        ctk.CTkLabel(card_genres, text="ПОПУЛЯРНЫЕ\nЖАНРЫ", font=("Helvetica", 18, "bold"), text_color="black", justify="left").pack(anchor="w", padx=20, pady=(20, 5))
        
        # Mini Pie Chart using Canvas
        pie_canvas = ctk.CTkCanvas(card_genres, width=100, height=100, bg="#C4C4C4", highlightthickness=0)
        pie_canvas.place(x=20, y=90)
        pie_canvas.create_arc(5, 5, 95, 95, start=0, extent=240, fill="#2E9E4A", outline="") # Green part
        pie_canvas.create_arc(5, 5, 95, 95, start=240, extent=120, fill="#E6C619", outline="") # Yellow part

        # Pie Chart Legend
        legend_frame = ctk.CTkFrame(card_genres, fg_color="transparent")
        legend_frame.place(x=130, y=100)
        
        # Legend item 1
        l1 = ctk.CTkFrame(legend_frame, fg_color="transparent")
        l1.pack(anchor="w", pady=5)
        ctk.CTkLabel(l1, text="●", text_color="#E6C619", font=("Helvetica", 16)).pack(side="left")
        ctk.CTkLabel(l1, text="Художественная\nлитература", text_color="black", font=("Helvetica", 11), justify="left").pack(side="left", padx=5)
        
        # Legend item 2
        l2 = ctk.CTkFrame(legend_frame, fg_color="transparent")
        l2.pack(anchor="w")
        ctk.CTkLabel(l2, text="●", text_color="#2E9E4A", font=("Helvetica", 16)).pack(side="left")
        ctk.CTkLabel(l2, text="Новелла", text_color="black", font=("Helvetica", 11)).pack(side="left", padx=5)

        # BOTTOM ROW
        bottom_row = ctk.CTkFrame(self.dashboard, fg_color="transparent")
        bottom_row.pack(fill="both", expand=True, pady=10)

        # Card 4: Active Readers
        card_active = ctk.CTkFrame(bottom_row, fg_color="#C4C4C4", corner_radius=15, width=280)
        card_active.pack(side="left", fill="y", padx=10)
        card_active.pack_propagate(False)
        ctk.CTkLabel(card_active, text="АКТИВНЫЕ ЧИТАТЕЛИ", font=("Helvetica", 18, "bold"), text_color="black").pack(anchor="w", padx=20, pady=(15, 10))
        
        stats_split = ctk.CTkFrame(card_active, fg_color="transparent")
        stats_split.pack(fill="x", padx=20)
        
        # Left Stat
        stat_left = ctk.CTkFrame(stats_split, fg_color="transparent")
        stat_left.pack(side="left", expand=True)
        ctk.CTkLabel(stat_left, text="Активные\nчитатели", text_color="black", font=("Helvetica", 12)).pack()
        ctk.CTkLabel(stat_left, text="289", font=("Helvetica", 36), text_color="black").pack(pady=10)
        
        # Divider Line
        ctk.CTkFrame(stats_split, width=1, height=80, fg_color="#A0A0A0").pack(side="left")
        
        # Right Stat
        stat_right = ctk.CTkFrame(stats_split, fg_color="transparent")
        stat_right.pack(side="right", expand=True)
        ctk.CTkLabel(stat_right, text="Бросили\n", text_color="black", font=("Helvetica", 12)).pack() # Extra \n to align heights
        ctk.CTkLabel(stat_right, text="41", font=("Helvetica", 36), text_color="black").pack(pady=10)

        # Card 5: Overdue Table
        card_overdue = ctk.CTkFrame(bottom_row, fg_color="#C4C4C4", corner_radius=15)
        card_overdue.pack(side="left", fill="both", expand=True, padx=10)
        ctk.CTkLabel(card_overdue, text="ПРОСРОЧЕНЫ", font=("Helvetica", 18, "bold"), text_color="black").pack(anchor="w", padx=20, pady=(15, 10))
        
        overdue_table = ctk.CTkFrame(card_overdue, fg_color="transparent", border_width=1, border_color="#A0A0A0")
        overdue_table.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Table Header
        h_frame = ctk.CTkFrame(overdue_table, fg_color="#B0B0B0", corner_radius=0)
        h_frame.pack(fill="x")
        ctk.CTkLabel(h_frame, text="Ивертарный №", text_color="black").pack(side="left", padx=20, pady=5)
        ctk.CTkLabel(h_frame, text="Название книги", text_color="black").pack(side="right", padx=60, pady=5)
        
        # Table Row
        r_frame = ctk.CTkFrame(overdue_table, fg_color="transparent")
        r_frame.pack(fill="x")
        ctk.CTkLabel(r_frame, text="90001", text_color="black").pack(side="left", padx=40, pady=5)
        ctk.CTkLabel(r_frame, text="Зимний вечер", text_color="black").pack(side="right", padx=60, pady=5)

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, text_color="white", anchor="w", height=45, corner_radius=10, command=command)
        btn.pack(fill="x", padx=10, pady=5)
