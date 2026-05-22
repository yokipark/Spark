import customtkinter as ctk
import database
import localization
import os
import sqlite3
from PIL import Image
import services.export_service as export_service
from tkinter import messagebox

class IssueReturnPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF")
        self.controller = controller

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(os.path.dirname(current_dir), "assets")

        self.current_reader_id = None
        self.current_reader_name = None

        # ==========================================
        # 1. SIDEBAR (Ширина: 370px)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=370, corner_radius=0, fg_color="#294730")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.sidebar_inner = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_inner.pack(fill="both", expand=True, padx=32, pady=(50, 25))

        self.logo_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.logo_zone.pack(side="top", fill="x", pady=(0, 40))

        logo_path = os.path.join(self.assets_dir, "library_icon.png")
        try:
            pil_logo = Image.open(logo_path)
            ctk_logo = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(50, 50))
            ctk.CTkLabel(self.logo_zone, image=ctk_logo, text="").pack(side="left", padx=(0, 15))
        except:
            ctk.CTkLabel(self.logo_zone, text="📖", font=("Inter", 32)).pack(side="left", padx=(0, 15))

        text_frame = ctk.CTkFrame(self.logo_zone, fg_color="transparent")
        text_frame.pack(side="left", fill="y")
        ctk.CTkLabel(text_frame, text=localization.get("app_title_1", "Картотека"), font=("Inter", 24, "bold"), text_color="#FFFFFF").pack(anchor="w")
        ctk.CTkLabel(text_frame, text=localization.get("app_title_2", "библиотекаря"), font=("Inter", 14), text_color="#E6C619").pack(anchor="w")
        
        self.nav_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.nav_zone.pack(side="top", fill="x")

        self.create_nav_btn(localization.get("main"), command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), is_active=True, command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn(localization.get("settings"), command=lambda: controller.show_frame("SettingsPage"))

        self.profile_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.profile_zone.pack(side="bottom", fill="x")

        user_path = os.path.join(self.assets_dir, "User_circle.png")
        try:
            pil_user = Image.open(user_path)
            ctk_user = ctk.CTkImage(light_image=pil_user, dark_image=pil_user, size=(45, 45))
            ctk.CTkLabel(self.profile_zone, image=ctk_user, text="").pack(side="left", padx=(0, 15))
        except:
            ctk.CTkLabel(self.profile_zone, text="👤", font=("Inter", 24)).pack(side="left", padx=(0, 15))

        profile_text = ctk.CTkFrame(self.profile_zone, fg_color="transparent")
        profile_text.pack(side="left", fill="y")
        ctk.CTkLabel(profile_text, text="СЕЗИМАЙ", text_color="white", font=("Inter", 14, "bold")).pack(anchor="w")
        ctk.CTkLabel(profile_text, text=localization.get('librarian'), text_color="#BEAC64", font=("Inter", 14)).pack(anchor="w")

        # ==========================================
        # 2. ПРАВЫЙ КОНТЕЙНЕР (ОСНОВНАЯ ЗОНА)
        # ==========================================
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True, padx=42, pady=50)

        # --- ГЛОБАЛЬНАЯ ШАПКА ---
        self.header = ctk.CTkFrame(self.content, height=45, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.global_search = ctk.CTkEntry(self.header, placeholder_text=localization.get("search_placeholder", "Поиск по всей базе..."), width=510, height=42, corner_radius=14, fg_color="#C4C4C4", text_color="black", border_width=0, font=("Inter", 14))
        self.global_search.pack(side="left")

        self.add_btn = ctk.CTkButton(self.header, text=localization.get("add_book", "ДОБАВИТЬ КНИГУ"), fg_color="#BEAC64", text_color="black", width=193, height=42, corner_radius=14, font=("Inter", 14, "bold"), command=lambda: controller.show_frame("MainPage"))
        self.add_btn.pack(side="left", padx=(20, 0))

        self.export_btn = ctk.CTkOptionMenu(
            self.header, values=["Excel", "PDF", "JSON"], fg_color="#F5F4F2", button_color="#F5F4F2", button_hover_color="#D9D9D9",
            text_color="black", dropdown_text_color="black", dropdown_fg_color="#E8E8E8", dropdown_hover_color="#BEAC64",
            width=136, height=42, corner_radius=14, font=("Inter", 14, "bold"), command=self.trigger_data_export
        )
        self.export_btn.set(localization.get("export", "ЭКСПОРТ"))
        self.export_btn.pack(side="left", padx=(20, 0))

        self.status_label = ctk.CTkLabel(self.content, text="", font=("Inter", 14, "bold"), text_color="black")
        self.status_label.pack(pady=(0, 10))

        # --- ОСНОВНОЙ КОНТЕНТ (ДВЕ КОЛОНКИ) ---
        self.body = ctk.CTkFrame(self.content, fg_color="transparent")
        self.body.pack(fill="both", expand=True)

        # ==========================================
        # ЛЕВАЯ КОЛОНКА: ЧИТАТЕЛИ
        # ==========================================
        left_col = ctk.CTkFrame(self.body, fg_color="transparent")
        left_col.pack(side="left", fill="y", padx=(0, 40))

        ctk.CTkLabel(left_col, text=localization.get("readersx"), font=("Inter", 20), text_color="black").pack(anchor="w", pady=(0, 15))

        self.reader_search = ctk.CTkEntry(left_col, placeholder_text=localization.get("enter_fio_or_id", "Введите ФИО или ID..."), 
                                          width=416, height=52, corner_radius=16, fg_color="#D9D9D9", border_color="#B0B0B0", border_width=1, 
                                          font=("Inter", 15), text_color="black")
        self.reader_search.pack(pady=(0, 20))
        self.reader_search.bind("<KeyRelease>", self.search_reader_live)

        # Карточка пользователя
        self.user_card = ctk.CTkFrame(left_col, width=416, height=576, fg_color="#D9D9D9", corner_radius=24, border_width=1, border_color="#B0B0B0")
        self.user_card.pack()
        self.user_card.pack_propagate(False)

        try:
            pil_img = Image.open(user_path)
            ctk_icon = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(120, 120))
            ctk.CTkLabel(self.user_card, image=ctk_icon, text="").pack(pady=(40, 10))
        except:
            ctk.CTkLabel(self.user_card, text="👤", font=("Inter", 80), text_color="#BEAC64").pack(pady=(40, 10))

        self.reader_name_lbl = ctk.CTkLabel(self.user_card, text=localization.get("reader_name"), font=("Inter", 16, "bold"), text_color="black")
        self.reader_name_lbl.pack(pady=(0, 0))
        ctk.CTkLabel(self.user_card, text=localization.get("reader"), font=("Inter", 12), text_color="#777").pack(pady=(0, 30))

        ctk.CTkLabel(self.user_card, text=localization.get("user_books_title", "Книги в руках"), font=("Inter", 14, "bold"), text_color="black").pack(anchor="w", padx=40)
        self.user_books_frame = ctk.CTkFrame(self.user_card, fg_color="transparent")
        self.user_books_frame.pack(fill="both", expand=True, padx=40, pady=(10, 20))


        # ==========================================
        # ПРАВАЯ КОЛОНКА: КНИГА И ИСТОРИЯ
        # ==========================================
        right_col = ctk.CTkFrame(self.body, fg_color="transparent")
        right_col.pack(side="left", fill="both", expand=True)

        # --- КАРТОЧКА: КНИГА ---
        self.book_card = ctk.CTkFrame(right_col, width=481, height=360, fg_color="#D9D9D9", corner_radius=16, border_width=1, border_color="#B0B0B0")
        self.book_card.pack(anchor="nw", pady=(0, 20))
        self.book_card.pack_propagate(False)

        ctk.CTkLabel(right_col, text=localization.get("book_caps", "КНИГА"), font=("Inter", 24), text_color="black").pack(anchor="w", padx=30, pady=(20, 20))
        inputs_row = ctk.CTkFrame(self.book_card, fg_color="transparent")
        inputs_row.pack(fill="x", padx=30)
        inputs_row.grid_columnconfigure(0, weight=1)
        inputs_row.grid_columnconfigure(1, weight=1)

        # Код книги (Слева)
        frame_b1 = ctk.CTkFrame(inputs_row, fg_color="transparent")
        frame_b1.grid(row=0, column=0, sticky="w", padx=(0, 24)) # Половина от 48px
        ctk.CTkLabel(frame_b1, text=localization.get("book_code_label", "Код книги"), text_color="black", font=("Inter", 14)).pack(anchor="w", pady=(0, 5))
        self.action_book_id = ctk.CTkEntry(frame_b1, width=170, height=45, corner_radius=16, fg_color="#E8E8E8", border_color="#B0B0B0", border_width=1, font=("Inter", 15), text_color="black")
        self.action_book_id.pack()

        # ID Читателя (Справа, заменили Название по ТЗ)
        frame_b2 = ctk.CTkFrame(inputs_row, fg_color="transparent")
        frame_b2.grid(row=0, column=1, sticky="w", padx=(24, 0)) # Вторая половина от 48px
        ctk.CTkLabel(frame_b2, text=localization.get("reader_id_label", "ID Читателя"), text_color="black", font=("Inter", 14)).pack(anchor="w", pady=(0, 5))
        self.action_reader_id = ctk.CTkEntry(frame_b2, width=170, height=45, corner_radius=16, fg_color="#E8E8E8", border_color="#B0B0B0", border_width=1, font=("Inter", 15), text_color="black")
        self.action_reader_id.pack()

        # Кнопки (Друг под другом)
        btns_frame = ctk.CTkFrame(self.book_card, fg_color="transparent")
        btns_frame.pack(fill="x", padx=30, pady=(40, 0))


        ctk.CTkButton(btns_frame, text=localization.get("issue_btn", "ВЫДАЧА"), fg_color="#8A9E8A", text_color="black", font=("Inter", 16, "bold"), height=50, corner_radius=10, border_width=1, border_color="#5D6B5D", command=self.handle_issue).pack(fill="x", pady=(0, 15))
        ctk.CTkButton(btns_frame, text=localization.get("return_btn", "ВОЗВРАТ"), fg_color="#BEAC64", text_color="black", font=("Inter", 16, "bold"), height=50, corner_radius=10, border_width=1, border_color="#8A7A3E", command=self.handle_return).pack(fill="x")

        # --- КАРТОЧКА: ИСТОРИЯ ---
        self.history_card = ctk.CTkFrame(right_col, width=481, height=220, fg_color="#D9D9D9", corner_radius=16, border_width=1, border_color="#B0B0B0")
        self.history_card.pack(anchor="nw")
        self.history_card.pack_propagate(False)

        ctk.CTkLabel(self.history_card, text=localization.get("history", "История"), font=("Inter", 16), text_color="black").pack(anchor="w", padx=30, pady=(15, 10))

        self.global_history_frame = ctk.CTkFrame(self.history_card, fg_color="transparent")
        self.global_history_frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        self.update_global_history()


    # ==========================================
    # ЛОГИКА ИНТЕРФЕЙСА
    # ==========================================
    def search_reader_live(self, event=None):
        query = self.reader_search.get().strip()
        
        for widget in self.user_books_frame.winfo_children():
            widget.destroy()

        if not query:
            self.current_reader_id = None
            self.current_reader_name = None
            self.reader_name_lbl.configure(text="ФИО читателя")
            self.action_reader_id.delete(0, 'end')
            return

        readers = database.search_readers(query)
        if readers:
            r_id, r_name, _, _ = readers[0]
            self.current_reader_id = r_id
            self.current_reader_name = r_name
            
            # Автозаполнение ID Читателя справа
            self.action_reader_id.delete(0, 'end')
            self.action_reader_id.insert(0, str(r_id))
            self.reader_name_lbl.configure(text=f"{r_name}")
            
            # Подтягиваем КНИГИ В РУКАХ (Названия)
            held_books_invs = database.get_reader_current_books(r_id)
            for inv in held_books_invs:
                book_data = database.get_book_by_inv(inv)
                if book_data:
                    title = book_data[0]
                    ctk.CTkLabel(self.user_books_frame, text=title, font=("Inter", 16), text_color="black").pack(anchor="w", pady=2)
        else:
            self.current_reader_id = None
            self.current_reader_name = None
            self.reader_name_lbl.configure(text="Не найден")
            self.action_reader_id.delete(0, 'end')

    def update_global_history(self):
        for widget in self.global_history_frame.winfo_children():
            widget.destroy()

        transactions = database.get_recent_transactions(limit=5)
        if not transactions:
            ctk.CTkLabel(self.global_history_frame, text="Нет истории", font=("Inter", 14), text_color="#777").pack(anchor="w")
            return

        for row in transactions:
            inv_num = row[0]
            ctk.CTkLabel(self.global_history_frame, text=str(inv_num), font=("Inter", 20), text_color="black").pack(anchor="w", pady=2)

    def handle_issue(self):
        b_inv = self.action_book_id.get().strip()
        r_id = self.action_reader_id.get().strip()

        if not b_inv or not r_id:
            self.show_status("Для ВЫДАЧИ заполните оба поля (Код книги и ID Читателя)!", "#C13C3C")
            return

        reader_name = database.get_reader_by_id(r_id)
        if not reader_name:
            self.show_status(f"Пользователь с ID {r_id} не найден.", "#C13C3C")
            return

        book_data = database.get_book_by_inv(b_inv)
        if not book_data:
            self.show_status(f"Книга с кодом {b_inv} не найдена.", "#C13C3C")
            return
        
        title, status = book_data
        if status == 'Выдана':
            self.show_status("Эта книга уже выдана!", "#C13C3C")
            return

        database.process_issue_db(b_inv, title, r_id, reader_name)
        self.show_status(f"Выдано: '{title}' -> {reader_name}", "#2E9E4A")
        
        self.action_book_id.delete(0, 'end')
        self.search_reader_live() 
        self.update_global_history()
        self.trigger_global_refresh()

    def handle_return(self):
        b_inv = self.action_book_id.get().strip()

        if not b_inv:
            self.show_status("Для ВОЗВРАТА введите Код книги!", "#C13C3C")
            return

        book_data = database.get_book_by_inv(b_inv)
        if not book_data:
            self.show_status(f"Книга с кодом {b_inv} не найдена.", "#C13C3C")
            return
        
        title, status = book_data
        if status == 'В наличии':
            self.show_status("Эта книга уже числится в библиотеке.", "#C13C3C")
            return

        actual_reader_id, actual_reader_name = database.get_current_reader_of_book(b_inv)

        database.process_return_db(b_inv, title, actual_reader_id, actual_reader_name)
        self.show_status(f"Возвращено: '{title}'", "#2E9E4A")
        
        self.action_book_id.delete(0, 'end')
        self.search_reader_live() 
        self.update_global_history()
        self.trigger_global_refresh()

    def trigger_global_refresh(self):
        if "DashboardPage" in self.controller.frames:
            self.controller.frames["DashboardPage"].refresh_data()
        if "MainPage" in self.controller.frames:
            self.controller.frames["MainPage"].load_data()
        if "ReportsPage" in self.controller.frames:
            self.controller.frames["ReportsPage"].refresh_reports()
        if "ReaderPage" in self.controller.frames:
            self.controller.frames["ReaderPage"].load_data()

    def show_status(self, text, color):
        self.status_label.configure(text=text, text_color=color)
        self.after(4000, lambda: self.status_label.configure(text=""))

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#BEAC64" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, text_color="white", font=("Inter", 20), anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", pady=5)

    def trigger_data_export(self, choice):
        try:
            if choice == "JSON": path = export_service.export_to_json()
            elif choice == "Excel": path = export_service.export_to_excel()
            elif choice == "PDF": path = export_service.export_to_pdf()
            self.export_btn.set(localization.get("export"))
            messagebox.showinfo("Экспорт завершен", f"Успешно выгружено в:\\n{os.path.basename(path)}")
        except Exception as e:
            self.export_btn.set(localization.get("export"))
            messagebox.showerror("Ошибка", str(e))
