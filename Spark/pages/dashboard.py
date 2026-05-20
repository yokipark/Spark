import customtkinter as ctk
import database
import localization
class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

        # --- SIDEBAR ---
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

        self.create_nav_btn(localization.get("main"), is_active=True, command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn(localization.get("settings"), command=lambda: controller.show_frame("SettingsPage"))

        self.profile_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.profile_zone.pack(side="bottom", fill="x")
        ctk.CTkLabel(self.profile_zone, text=f"👤 СЕЗИМАЙ\n{localization.get("librarian")}", text_color="white", justify="left").pack(side="left")

        # --- RIGHT CONTENT ---
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.create_header(self.right_container)

        # --- STATS CARDS ---
        stats = database.get_dashboard_stats()
        
        self.stats_frame = ctk.CTkFrame(self.right_container, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=10)
        
        # We save these as 'self.lbl_...' so we can change their text later!
        self.lbl_books = self.create_stat_card(self.stats_frame, localization.get("books_on_loan"), str(stats[0]), "✅", 0)
        self.lbl_overdue = self.create_stat_card(self.stats_frame, localization.get("overdue"), str(stats[1]), "❗", 1)
        self.lbl_readers = self.create_stat_card(self.stats_frame, localization.get("new_readers"), str(stats[2]), "👤", 2)

        # --- MIDDLE ROW ---
        self.middle_row = ctk.CTkFrame(self.right_container, fg_color="transparent")
        self.middle_row.pack(fill="both", expand=True, pady=10)
        self.middle_row.grid_columnconfigure(0, weight=3)
        self.middle_row.grid_columnconfigure(1, weight=1)

        self.graph_box = ctk.CTkFrame(self.middle_row, fg_color="#C4C4C4", corner_radius=15, border_width=2, border_color="#A0A0A0")
        self.graph_box.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        ctk.CTkLabel(self.graph_box, text=localization.get("weekly_activity"), font=("Helvetica", 16, "bold"), text_color="black").pack(pady=10)
        self.draw_weekly_chart(self.graph_box)

        self.actions_box = ctk.CTkFrame(self.middle_row, fg_color="#C4C4C4", corner_radius=15)
        self.actions_box.grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(self.actions_box, text=f"{localization.get("quick")}\n{localization.get("actions")}", font=("Helvetica", 16, "bold"), text_color="black").pack(pady=10)
        
        btn_issue = ctk.CTkButton(self.actions_box, text=localization.get("quick_issue"), fg_color="#304146", height=40, corner_radius=20, command=lambda: controller.show_frame("IssueReturnPage"))
        btn_issue.pack(pady=5, padx=20, fill="x")

        btn_return = ctk.CTkButton(self.actions_box, text=localization.get("accept_return"), fg_color="#304146", height=40, corner_radius=20, command=lambda: controller.show_frame("IssueReturnPage"))
        btn_return.pack(pady=5, padx=20, fill="x")

        btn_add_reader = ctk.CTkButton(self.actions_box, text=localization.get("add_reader"), fg_color="#304146", height=40, corner_radius=20, command=lambda: controller.show_frame("ReaderPage"))
        btn_add_reader.pack(pady=5, padx=20, fill="x")

        # --- TRANSACTIONS TABLE ---
        self.table_box = ctk.CTkFrame(self.right_container, fg_color="#C4C4C4", corner_radius=15, border_width=1, border_color="#A0A0A0")
        self.table_box.pack(fill="x", pady=10)
        ctk.CTkLabel(self.table_box, text=localization.get("recent_actions"), font=("Helvetica", 16, "bold"), text_color="black").pack(anchor="w", padx=20, pady=10)
        
        self.transactions_frame = ctk.CTkFrame(self.table_box, fg_color="transparent")
        self.transactions_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.load_recent_transactions()

    # --- THE MAGIC REFRESH METHOD ---
    def refresh_data(self):
        """Called by other pages to update the dashboard instantly without restarting"""
        # 1. Update the numbers in the cards
        stats = database.get_dashboard_stats()
        self.lbl_books.configure(text=str(stats[0]))
        self.lbl_overdue.configure(text=str(stats[1]))
        self.lbl_readers.configure(text=str(stats[2]))

        # 2. Clear the old table and reload it
        for widget in self.transactions_frame.winfo_children():
            widget.destroy()
        self.load_recent_transactions()

    # --- HELPERS ---
    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, text_color="white", 
                            anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", pady=5) 

    def create_stat_card(self, parent, title, value, icon, col):
        card = ctk.CTkFrame(parent, fg_color="#C4C4C4", height=100, corner_radius=15, border_width=2, border_color="#A0A0A0")
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=title, font=("Helvetica", 16), text_color="black").place(x=15, y=10)
        
        # We create the value label and RETURN it so we can change it later
        val_label = ctk.CTkLabel(card, text=value, font=("Helvetica", 42, "bold"), text_color="black")
        val_label.place(x=15, y=40)
        
        ctk.CTkLabel(card, text=icon, font=("Helvetica", 32)).place(relx=0.85, rely=0.6, anchor="center")
        return val_label

    def create_header(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        ctk.CTkEntry(header, placeholder_text=localization.get("search_placeholder"), width=400, height=40, corner_radius=20, fg_color="#C4C4C4", text_color="black").pack(side="left")
        ctk.CTkButton(header, text=localization.get("export"), fg_color="#D1C4A3", text_color="black", width=100, height=40).pack(side="right")
        ctk.CTkButton(header, text=localization.get("add_book"), fg_color="#7C9A82", text_color="black", height=40).pack(side="right", padx=10)

    def draw_weekly_chart(self, parent):
        canvas = ctk.CTkCanvas(parent, height=180, bg="#C4C4C4", highlightthickness=0, )
        canvas.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        for i, val in enumerate(["40", "30", "20", "10", "0"]):
            y = 20 + (i * 30)
            canvas.create_text(10, y, text=val, fill="#A0A0A0", font=("Helvetica", 10))
            canvas.create_line(30, y, 450, y, fill="#A0A0A0")

        days = ["п\nн", "в\nт", "с\nр", "ч\nт", "п\nт", "с\nб", "в\nс"]
        heights = [25, 33, 40, 5, 30, 35, 14] 
        colors = ["#2E9E4A", "#2E9E4A", "#2E9E4A", "#C13C3C", "#2E9E4A", "#2E9E4A", "#C13C3C"]

        for i in range(7):
            x0 = 50 + (i * 55)
            y0 = 140 - (heights[i] * 3)
            x1 = x0 + 25
            y1 = 140
            canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i], outline="")
            canvas.create_text(x0 + 12, 160, text=days[i], fill="black", font=("Helvetica", 10))

    def load_recent_transactions(self):
        headers = [
            localization.get("inv_num"),
            localization.get("book_title"),
            localization.get("reader_name"),
            localization.get("action"),
            localization.get("time")
            ]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.transactions_frame, text=h, font=("Helvetica", 12), text_color="gray").grid(row=0, column=i, padx=5, pady=2, sticky="w")
            self.transactions_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkFrame(self.transactions_frame, height=1, fg_color="gray").grid(row=1, column=0, columnspan=5, sticky="ew", pady=(0, 5))

        transactions = database.get_recent_transactions(limit=4) # Load up to 4 recent things
        
        if not transactions:
            transactions = [
                ("90021", "История искусств", "Кузнецова М.К", "Возврат", "08:55"),
                ("12005", "Мастер и Маргарита", "Иванов А.С.", "Выдача", "10:15")
            ]

        for row_idx, row_data in enumerate(transactions, start=2):
            for col_idx, item in enumerate(row_data):
                # Color code the action column
                color = "black"
                if col_idx == 3: # "Действие" column
                    color = "#2E9E4A" if item == "Возврат" else "#B8A45F"

                ctk.CTkLabel(self.transactions_frame, text=str(item), text_color=color, font=("Helvetica", 13)).grid(row=row_idx, column=col_idx, padx=5, pady=2, sticky="w")
            
            ctk.CTkFrame(self.transactions_frame, height=1, fg_color="#A0A0A0").grid(row=row_idx*2+1, column=0, columnspan=5, sticky="ew")import customtkinter as ctk
import database
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
        self.create_nav_btn("📊 Отчеты", command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn("⚙️ Настройки", command=lambda: controller.show_frame("SettingsPage"))

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
        
        # 1. Button: Быстрая выдача (No command yet)
        btn_issue = ctk.CTkButton(self.actions_box, text="Быстрая выдача", fg_color="#4A6550", height=40, corner_radius=20)
        btn_issue.pack(pady=5, padx=20, fill="x")

        # 2. Button: Принять возврат (No command yet)
        btn_return = ctk.CTkButton(self.actions_box, text="Принять возврат", fg_color="#4A6550", height=40, corner_radius=20)
        btn_return.pack(pady=5, padx=20, fill="x")

        # 3. Button: Добавить читателя (Command attached!)
        btn_add_reader = ctk.CTkButton(
            self.actions_box, 
            text="Добавить читателя", 
            fg_color="#4A6550", height=40, corner_radius=20, 
            command=self.show_add_reader_modal # <--- Attached here!
        )
        btn_add_reader.pack(pady=5, padx=20, fill="x")
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

 # --- MODAL: Add Reader ---

    def show_add_reader_modal(self):
        if hasattr(self, "modal") and self.modal.winfo_exists():
            return

        self.modal = ctk.CTkFrame(self.right_container, width=580, height=650, fg_color="#C4C4C4", corner_radius=20, border_width=1, border_color="#A0A0A0")
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        self.modal.pack_propagate(False)
        self.modal.grid_propagate(False)

        # BUTTON: Changed to call self.save_new_reader
        ctk.CTkButton(self.modal, text="Сохранить", fg_color="#7C9A82", width=180, height=35, command=self.save_new_reader).place(x=360, y=30)
        ctk.CTkButton(self.modal, text="Отмена", fg_color="transparent", text_color="black", hover_color="#A0A0A0", width=100, height=35, command=self.modal.destroy).place(x=250, y=30)

        # Profile Image
        profile_circle = ctk.CTkLabel(self.modal, text="👤", font=("Helvetica", 90), text_color="#7C9A82", width=130, height=130)
        profile_circle.place(x=80, y=120, anchor="center")

        # ENTRY: The text box to type the name!
        self.name_entry = ctk.CTkEntry(self.modal, placeholder_text="Введите ФИО", font=("Helvetica", 18), width=250, height=40, fg_color="#E0E0E0", text_color="black")
        self.name_entry.place(x=160, y=105, anchor="w")
        
        ctk.CTkLabel(self.modal, text="новый читатель", font=("Helvetica", 14), text_color="gray").place(x=160, y=150, anchor="w")

        # (I left the book tables blank here, since a new reader has no books yet)
        ctk.CTkLabel(self.modal, text="ТЕКУЩИЕ КНИГИ: Нет", font=("Helvetica", 14, "bold"), text_color="gray").place(x=40, y=210)
        ctk.CTkLabel(self.modal, text="ИСТОРИЯ ВЫДАЧ: Нет", font=("Helvetica", 14, "bold"), text_color="gray").place(x=40, y=360)

    def save_new_reader(self):
        """Gets text from the entry, saves to DB, and refreshes the table."""
        new_name = self.name_entry.get()
        
        if new_name.strip() != "":
            # 1. Save to SQLite
            database.add_reader(new_name)
            
            # 2. Refresh the UI Table to show the new person
            self.load_data()
            
            # 3. Close the modal
            self.modal.destroy()
        else:
            # Optionally change border color to red to show an error
            self.name_entry.configure(border_color="red", border_width=2)
