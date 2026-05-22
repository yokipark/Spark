import customtkinter as ctk
import localization
import database
import os
from PIL import Image
import services.export_service as export_service
from tkinter import messagebox

class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF")
        self.controller = controller

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(os.path.dirname(current_dir), "assets")

        # ==========================================
        # 1. SIDEBAR (Ширина: 370px)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=370, corner_radius=0, fg_color="#294730")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) 

        self.sidebar_inner = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_inner.pack(fill="both", expand=True, padx=32, pady=(50, 25))

        # --- ЗОНА ЛОГОТИПА И ТЕКСТА ---
        self.logo_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.logo_zone.pack(side="top", fill="x", pady=(0, 40)) 
        
        logo_path = os.path.join(self.assets_dir, "library_icon.png")
        try:
            pil_logo = Image.open(logo_path)
            ctk_logo = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(50, 50))
            ctk.CTkLabel(self.logo_zone, image=ctk_logo, text="").pack(side="left", padx=(0, 15))
        except Exception:
            ctk.CTkLabel(self.logo_zone, text="📖", font=("Inter", 32)).pack(side="left", padx=(0, 15))

        text_frame = ctk.CTkFrame(self.logo_zone, fg_color="transparent")
        text_frame.pack(side="left", fill="y")
        ctk.CTkLabel(text_frame, text=localization.get("app_title_1"), font=("Inter", 24, "bold"), text_color="#FFFFFF").pack(anchor="w")
        ctk.CTkLabel(text_frame, text=localization.get("app_title_2"), font=("Inter", 14), text_color="#E6C619").pack(anchor="w")

        # --- НАВИГАЦИЯ ---
        self.nav_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.nav_zone.pack(side="top", fill="x")

        self.create_nav_btn(localization.get("main"), command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), is_active=True, command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn(localization.get("settings"), command=lambda: controller.show_frame("SettingsPage"))

        # --- ЗОНА ПРОФИЛЯ ---
        self.profile_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.profile_zone.pack(side="bottom", fill="x")
        
        user_path = os.path.join(self.assets_dir, "User_circle.png")
        if not os.path.exists(user_path):
            user_path = os.path.join(self.assets_dir, "User_cicrle.png")

        try:
            pil_user = Image.open(user_path)
            ctk_user = ctk.CTkImage(light_image=pil_user, dark_image=pil_user, size=(45, 45))
            ctk.CTkLabel(self.profile_zone, image=ctk_user, text="").pack(side="left", padx=(0, 15))
        except Exception:
            ctk.CTkLabel(self.profile_zone, text="👤", font=("Inter", 24)).pack(side="left", padx=(0, 15))
        
        profile_text_frame = ctk.CTkFrame(self.profile_zone, fg_color="transparent")
        profile_text_frame.pack(side="left", fill="y")
        ctk.CTkLabel(profile_text_frame, text="СЕЗИМАЙ", text_color="white", font=("Inter", 14, "bold")).pack(anchor="w")
        ctk.CTkLabel(profile_text_frame, text=localization.get('librarian'), text_color="#BEAC64", font=("Inter", 14)).pack(anchor="w")

        # ==========================================
        # 2. RIGHT CONTAINER (Контентная область)
        # ==========================================
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True, padx=42, pady=50)

        # --- 1. ШАПКА И ПОИСК ---
        self.header = ctk.CTkFrame(self.content, height=45, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.search_bar = ctk.CTkEntry(self.header, placeholder_text=localization.get("search_placeholder"), width=510, height=42, corner_radius=14, fg_color="#C4C4C4", text_color="black", border_width=0, font=("Inter", 14))
        self.search_bar.pack(side="left")

        self.add_btn = ctk.CTkButton(self.header, text=localization.get("add_book"), fg_color="#BEAC64", text_color="black", width=193, height=42, corner_radius=14, font=("Inter", 14, "bold"), command=lambda: controller.show_frame("MainPage"))
        self.add_btn.pack(side="left", padx=(20, 0))

        self.export_btn = ctk.CTkOptionMenu(
            self.header, 
            values=["Excel", "PDF", "JSON"], 
            fg_color="#F5F4F2", 
            button_color="#F5F4F2", 
            button_hover_color="#D9D9D9",
            text_color="black", 
            dropdown_text_color="black",
            dropdown_fg_color="#E8E8E8",
            dropdown_hover_color="#BEAC64",
            width=136, 
            height=42, 
            corner_radius=14, 
            font=("Inter", 14, "bold"),
            command=self.trigger_data_export
        )
        self.export_btn.set(localization.get("export")) 
        self.export_btn.pack(side="left", padx=(20, 0)) 

        # --- 2. ФИЛЬТР ДАТЫ ---
        self.date_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.date_frame.pack(fill="x", pady=(10, 20))
        
        try:
            available_months = database.get_available_months()
        except Exception:
            available_months = ["Январь 2025"]

        if not available_months:
            available_months = ["Январь 2025"]

        self.start_month_menu = ctk.CTkOptionMenu(self.date_frame, values=available_months, fg_color="#C4C4C4", text_color="black", button_color="#A0A0A0", corner_radius=14, width=160, height=35, font=("Inter", 14), command=self.on_date_change)
        self.start_month_menu.set(available_months[0])
        self.start_month_menu.pack(side="left")

        ctk.CTkLabel(self.date_frame, text=" - ", text_color="black", font=("Inter", 16, "bold")).pack(side="left", padx=10)

        self.end_month_menu = ctk.CTkOptionMenu(self.date_frame, values=available_months, fg_color="#C4C4C4", text_color="black", button_color="#A0A0A0", corner_radius=14, width=160, height=35, font=("Inter", 14), command=self.on_date_change)
        self.end_month_menu.set(available_months[-1])
        self.end_month_menu.pack(side="left")

        # --- 3. СЕТКА ОТЧЁТОВ ---
        self.dashboard = ctk.CTkFrame(self.content, fg_color="transparent")
        self.dashboard.pack(fill="both", expand=True)

        top_row = ctk.CTkFrame(self.dashboard, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 20))

        # Карточка 1: Всего выдано
        card_total = ctk.CTkFrame(top_row, fg_color="#D9D9D9", corner_radius=16, height=220, border_width=1, border_color="black")
        card_total.pack(side="left", fill="both", expand=True, padx=(0, 10))
        card_total.pack_propagate(False)
        ctk.CTkLabel(card_total, text=localization.get("total_issued"), font=("Inter", 16, "bold"), text_color="black", justify="left").pack(anchor="w", padx=20, pady=(20, 5))
        
        self.lbl_total_issued = ctk.CTkLabel(card_total, text="0", font=("Inter", 36, "bold"), text_color="black")
        self.lbl_total_issued.pack(anchor="w", padx=20)
        
        self.bar_canvas = ctk.CTkCanvas(card_total, height=80, bg="#D9D9D9", highlightthickness=0)
        self.bar_canvas.pack(fill="x", padx=20, pady=10)

        # Средний мини-столбец
        mid_col = ctk.CTkFrame(top_row, fg_color="transparent")
        mid_col.pack(side="left", fill="y", padx=10)
        
        card_new_books = ctk.CTkFrame(mid_col, fg_color="#D9D9D9", corner_radius=16, width=180, height=105, border_width=1, border_color="black")
        card_new_books.pack(pady=(0, 10))
        card_new_books.pack_propagate(False)
        ctk.CTkLabel(card_new_books, text=localization.get("new_books"), font=("Inter", 14, "bold"), text_color="black").pack(anchor="w", padx=15, pady=(15, 0))
        self.lbl_new_books = ctk.CTkLabel(card_new_books, text="0", font=("Inter", 32, "bold"), text_color="black")
        self.lbl_new_books.pack(anchor="w", padx=15)

        card_new_readers = ctk.CTkFrame(mid_col, fg_color="#D9D9D9", corner_radius=16, width=180, height=105, border_width=1, border_color="black")
        card_new_readers.pack()
        card_new_readers.pack_propagate(False)
        ctk.CTkLabel(card_new_readers, text=localization.get("new_readers_caps"), font=("Inter", 14, "bold"), text_color="black", justify="left").pack(anchor="w", padx=15, pady=(15, 0))
        self.lbl_new_readers = ctk.CTkLabel(card_new_readers, text="0", font=("Inter", 32, "bold"), text_color="black")
        self.lbl_new_readers.pack(anchor="w", padx=15)

        # Карточка 3: Популярные жанры
        card_genres = ctk.CTkFrame(top_row, fg_color="#D9D9D9", corner_radius=16, height=220, border_width=1, border_color="black")
        card_genres.pack(side="left", fill="both", expand=True, padx=(10, 0))
        card_genres.pack_propagate(False)
        ctk.CTkLabel(card_genres, text=localization.get("popular_genres"), font=("Inter", 16, "bold"), text_color="black", justify="left").pack(anchor="w", padx=20, pady=(20, 5))
        
        self.pie_canvas = ctk.CTkCanvas(card_genres, width=100, height=100, bg="#D9D9D9", highlightthickness=0)
        self.pie_canvas.place(x=20, y=90)

        self.legend_frame = ctk.CTkFrame(card_genres, fg_color="transparent")
        self.legend_frame.place(x=130, y=85)

        # --- НИЖНИЙ РЯД КАРТОЧЕК ---
        bottom_row = ctk.CTkFrame(self.dashboard, fg_color="transparent")
        bottom_row.pack(fill="both", expand=True, pady=10)

        # Карточка 4: Активные читатели
        card_active = ctk.CTkFrame(bottom_row, fg_color="#D9D9D9", corner_radius=16, width=280, border_width=1, border_color="black")
        card_active.pack(side="left", fill="y", padx=(0, 10))
        card_active.pack_propagate(False)
        ctk.CTkLabel(card_active, text=localization.get("active_readers_caps"), font=("Inter", 16, "bold"), text_color="black").pack(anchor="w", padx=20, pady=(20, 10))
        
        stats_split = ctk.CTkFrame(card_active, fg_color="transparent")
        stats_split.pack(fill="x", padx=20, pady=10)
        
        stat_left = ctk.CTkFrame(stats_split, fg_color="transparent")
        stat_left.pack(side="left", expand=True)
        ctk.CTkLabel(stat_left, text=localization.get("active_label"), text_color="black", font=("Inter", 12), justify="center").pack()
        self.lbl_active_readers = ctk.CTkLabel(stat_left, text="0", font=("Inter", 36, "bold"), text_color="black")
        self.lbl_active_readers.pack(pady=5)
        
        ctk.CTkFrame(stats_split, width=1, height=80, fg_color="#A0A0A0").pack(side="left", padx=10)
        
        stat_right = ctk.CTkFrame(stats_split, fg_color="transparent")
        stat_right.pack(side="right", expand=True)
        ctk.CTkLabel(stat_right, text=localization.get("dropped_label"), text_color="black", font=("Inter", 12), justify="center").pack() 
        self.lbl_inactive_readers = ctk.CTkLabel(stat_right, text="0", font=("Inter", 36, "bold"), text_color="black")
        self.lbl_inactive_readers.pack(pady=5)

        # Карточка 5: Таблица задолженностей
        self.card_overdue = ctk.CTkFrame(bottom_row, fg_color="#D9D9D9", corner_radius=16, border_width=1, border_color="black")
        self.card_overdue.pack(side="left", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(self.card_overdue, text=localization.get("overdue").upper(), font=("Inter", 16, "bold"), text_color="black").pack(anchor="w", padx=20, pady=(20, 10))
        
        self.overdue_table = ctk.CTkFrame(self.card_overdue, fg_color="transparent")
        self.overdue_table.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        h_frame = ctk.CTkFrame(self.overdue_table, fg_color="#C4C4C4", corner_radius=0)
        h_frame.pack(fill="x")
        ctk.CTkLabel(h_frame, text=localization.get("inv_num"), text_color="black", font=("Inter", 12, "bold")).pack(side="left", padx=20, pady=5)
        ctk.CTkLabel(h_frame, text=localization.get("book_title"), text_color="black", font=("Inter", 12, "bold")).pack(side="right", padx=60, pady=5)

        self.refresh_reports()

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#BEAC64" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, text_color="white", font=("Inter", 20),
                            anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", pady=5)

    def on_date_change(self, choice):
        self.refresh_reports()

    def refresh_reports(self):
        start_m = self.start_month_menu.get()
        end_m = self.end_month_menu.get()

        data = database.get_reports_data(start_m, end_m)
        total_issued = data.get("total_issued", 0)
        histogram_data = data.get("histogram", [0]*6)
        new_books = data.get("new_books", 0)
        new_readers = data.get("new_readers", 0)
        genres = data.get("genres", [("Нет данных", 1)])
        active = data.get("active_readers", 0)
        inactive = data.get("inactive_readers", 0)

        self.lbl_total_issued.configure(text=f"{total_issued:,}".replace(",", " "))
        self.lbl_new_books.configure(text=str(new_books))
        self.lbl_new_readers.configure(text=str(new_readers))
        self.lbl_active_readers.configure(text=str(active))
        self.lbl_inactive_readers.configure(text=str(inactive))

        # --- Гистограмма ---
        self.bar_canvas.delete("all")
        width = 240
        height = 70
        self.bar_canvas.create_line(10, height, width, height, fill="black", width=1)
        
        if histogram_data and max(histogram_data) > 0:
            bar_width = 4
            spacing = width / (len(histogram_data) + 1)
            max_val = max(histogram_data)
            colors = ["#E6C619", "#C13C3C", "#2E9E4A", "#4A6550", "#BEAC64"]
            for i, val in enumerate(histogram_data):
                x = 10 + (i + 1) * spacing
                bar_h = (val / max_val) * (height - 10)
                color = colors[i % len(colors)]
                self.bar_canvas.create_line(x, height, x, height - bar_h, fill=color, width=bar_width)

        # --- Круговая диаграмма ---
        self.pie_canvas.delete("all")
        for widget in self.legend_frame.winfo_children():
            widget.destroy()

        colors = ["#2E9E4A", "#E6C619", "#C13C3C", "#A8ADA8"]
        start_angle = 0
        total_genres = sum([val for _, val in genres])

        for i, (genre_name, val) in enumerate(genres):
            color = colors[i % len(colors)]
            if total_genres > 0:
                extent = (val / total_genres) * 360
                self.pie_canvas.create_arc(5, 5, 95, 95, start=start_angle, extent=extent, fill=color, outline="")
                start_angle += extent
            
            l_row = ctk.CTkFrame(self.legend_frame, fg_color="transparent")
            l_row.pack(anchor="w", pady=2)
            ctk.CTkLabel(l_row, text="●", text_color=color, font=("Inter", 16)).pack(side="left")
            display_name = genre_name if len(genre_name) < 16 else genre_name[:14] + "..."
            ctk.CTkLabel(l_row, text=display_name, text_color="black", font=("Inter", 11)).pack(side="left", padx=5)

    def trigger_data_export(self, choice):
        try:
            if choice == "JSON":
                path = export_service.export_to_json()
            elif choice == "Excel":
                path = export_service.export_to_excel()
            elif choice == "PDF":
                path = export_service.export_to_pdf()
            
            self.export_btn.set(localization.get("export"))
            filename = os.path.basename(path)
            messagebox.showinfo(localization.get("exp_success_title"), localization.get("exp_success_msg").format(filename))
        except Exception as e:
            self.export_btn.set(localization.get("export"))
            messagebox.showerror(localization.get("exp_error_title"), localization.get("exp_error_msg").format(str(e)))
