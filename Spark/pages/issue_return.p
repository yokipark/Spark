import customtkinter as ctk
import database
import localization

class IssueReturnPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

        # ==========================================
        # SIDEBAR (New 370px Layout with Spark Logo)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=370, corner_radius=0, fg_color="#4A6550")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.sidebar_inner = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_inner.pack(fill="both", expand=True, padx=32, pady=(50, 25))

        # ZONE A: SPARK Logo
        self.logo_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.logo_zone.pack(side="top", fill="x", pady=(0, 40)) # 40px gap below the logo

        ctk.CTkLabel(self.logo_zone, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(anchor="w")
        ctk.CTkLabel(self.logo_zone, text="библиотекаря", font=("Helvetica", 14), text_color="#E6C619").pack(anchor="w")
        
        # ZONE B: Buttons
        self.nav_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.nav_zone.pack(side="top", fill="x")

        self.create_nav_btn(localization.get("main"), command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), is_active=True, command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn(localization.get("settings"),  command=lambda: controller.show_frame("SettingsPage"))

        # ZONE C: Profile
        self.profile_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.profile_zone.pack(side="bottom", fill="x")
        ctk.CTkLabel(self.profile_zone, text="👤 СЕЗИМАЙ\nБиблиотекарь", text_color="white", justify="left").pack(side="left")

        # ==========================================
        # RIGHT CONTENT
        # ==========================================
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Header
        self.header = ctk.CTkFrame(self.content, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 10))
        self.search_bar = ctk.CTkEntry(self.header, placeholder_text="Поиск по всей базе...", width=450, height=40, corner_radius=20)
        self.search_bar.pack(side="left", padx=10)
        ctk.CTkButton(self.header, text="ЭКСПОРТ ⌄", fg_color="#D1C4A3", text_color="black", height=40).pack(side="right", padx=10)

        # Status Label (Shows success/error messages)
        self.status_label = ctk.CTkLabel(self.content, text="", font=("Helvetica", 14, "bold"), text_color="black")
        self.status_label.pack(pady=(0, 10))

        # Split Layout
        self.body = ctk.CTkFrame(self.content, fg_color="transparent")
        self.body.pack(fill="both", expand=True, pady=10)
        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_columnconfigure(1, weight=1)

        # --- LEFT COLUMN: Reader & Issue Info ---
        left_col = ctk.CTkFrame(self.body, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(left_col, text="ЧИТАТЕЛЬ", font=("Helvetica", 22, "bold"), text_color="black").pack(anchor="w", pady=(0, 10))

        inputs_frame = ctk.CTkFrame(left_col, fg_color="transparent")
        inputs_frame.pack(fill="x", pady=(0, 20))
        
        id_frame1 = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        id_frame1.pack(side="left", padx=(0, 20))
        ctk.CTkLabel(id_frame1, text="Код читателя", text_color="black").pack(anchor="w")
        self.reader_id_entry = ctk.CTkEntry(id_frame1, width=180, height=40, corner_radius=10, fg_color="#C4C4C4")
        self.reader_id_entry.pack()

        id_frame2 = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        id_frame2.pack(side="left")
        ctk.CTkLabel(id_frame2, text="Код книги", text_color="black").pack(anchor="w")
        self.book_id_issue_entry = ctk.CTkEntry(id_frame2, width=180, height=40, corner_radius=10, fg_color="#C4C4C4")
        self.book_id_issue_entry.pack()

        # Action Button for Issue
        ctk.CTkButton(left_col, text="Оформить выдачу", fg_color="#8A9E8A", text_color="black", font=("Helvetica", 16, "bold"), height=50, command=self.handle_issue).pack(fill="x", pady=(20, 0))

        # --- RIGHT COLUMN: Book Return ---
        right_col = ctk.CTkFrame(self.body, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        book_card = ctk.CTkFrame(right_col, fg_color="#C4C4C4", corner_radius=15)
        book_card.pack(fill="x", pady=(35, 10))

        ctk.CTkLabel(book_card, text="ВОЗВРАТ КНИГИ", font=("Helvetica", 22, "bold"), text_color="black").pack(anchor="w", padx=20, pady=(20, 10))

        book_inputs = ctk.CTkFrame(book_card, fg_color="transparent")
        book_inputs.pack(fill="x", padx=20, pady=(0, 20))

        b_id_frame = ctk.CTkFrame(book_inputs, fg_color="transparent")
        b_id_frame.pack(side="left", padx=(0, 20))
        ctk.CTkLabel(b_id_frame, text="Код книги", text_color="black").pack(anchor="w")
        self.book_id_return_entry = ctk.CTkEntry(b_id_frame, width=180, height=40, corner_radius=10, fg_color="#D9D9D9")
        self.book_id_return_entry.pack()

        # Action Button for Return
        ctk.CTkButton(book_card, text="Оформить возврат", fg_color="#B09B66", text_color="black", font=("Helvetica", 16, "bold"), height=50, command=self.handle_return).pack(fill="x", padx=20, pady=(5, 20))

    # --- ACTION LOGIC ---

    def handle_issue(self):
        r_id = self.reader_id_entry.get().strip()
        b_inv = self.book_id_issue_entry.get().strip()

        if not r_id or not b_inv:
            self.show_status("Пожалуйста, заполните оба поля!", "#C13C3C")
            return

        reader_name = database.get_reader_by_id(r_id)
        if not reader_name:
            self.show_status(f"Читатель с ID {r_id} не найден.", "#C13C3C")
            return

        book_data = database.get_book_by_inv(b_inv)
        if not book_data:
            self.show_status(f"Книга с № {b_inv} не найдена.", "#C13C3C")
            return
        
        title, status = book_data
        if status == 'Выдана':
            self.show_status("Эта книга уже выдана кому-то другому!", "#C13C3C")
            return

       # Process the issue
        database.process_issue_db(b_inv, title, r_id, reader_name)
        self.show_status(f"Успех! Книга '{title}' выдана {reader_name}.", "#2E9E4A")
        
        # Clear entries
        self.reader_id_entry.delete(0, 'end')
        self.book_id_issue_entry.delete(0, 'end')

       # Refresh Dashboard
        if "DashboardPage" in self.controller.frames:
            self.controller.frames["DashboardPage"].refresh_data()
            
        # Refresh Book Fund (MainPage)
        if "MainPage" in self.controller.frames:
            self.controller.frames["MainPage"].load_data()

    def handle_return(self):
        b_inv = self.book_id_return_entry.get().strip()

        if not b_inv:
            self.show_status("Введите инвентарный № книги!", "#C13C3C")
            return

        book_data = database.get_book_by_inv(b_inv)
        if not book_data:
            self.show_status(f"Книга с № {b_inv} не найдена.", "#C13C3C")
            return
        
        title, status = book_data
        if status == 'В наличии':
            self.show_status("Эта книга уже числится в библиотеке.", "#C13C3C")
            return

        # Process the return (We assume ID 0 for generic returns if we don't force reader ID here)
        database.process_return_db(b_inv, title, 0, "Неизвестно")
        self.show_status(f"Успех! Книга '{title}' возвращена.", "#2E9E4A")
        
        self.book_id_return_entry.delete(0, 'end')

        # Refresh Dashboard
        if "DashboardPage" in self.controller.frames:
            self.controller.frames["DashboardPage"].refresh_data()
            
        # Refresh Book Fund (MainPage)
        if "MainPage" in self.controller.frames:
            self.controller.frames["MainPage"].load_data()

            
    def show_status(self, text, color):
        self.status_label.configure(text=text, text_color=color)
        # Clear the message after 4 seconds
        self.after(4000, lambda: self.status_label.configure(text=""))

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, text_color="white", 
                            anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", pady=5)
