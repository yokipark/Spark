import customtkinter as ctk
import database
import localization
import os
from PIL import Image
import services.export_service as export_service
from tkinter import messagebox

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF")
        self.controller = controller
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(os.path.dirname(current_dir), "assets")

        # ==========================================
        # 1. SIDEBAR
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=370, corner_radius=0, fg_color="#294730")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.sidebar_inner = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_inner.pack(fill="both", expand=True, padx=32, pady=(50, 25))

        # --- ЗОНА ЛОГОТИПА ---
        self.logo_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.logo_zone.pack(side="top", fill="x", pady=(0, 40))
        
        logo_path = os.path.join(self.assets_dir, "library_icon.png")
        try:
            pil_logo = Image.open(logo_path)
            ctk_logo = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(50, 50))
            ctk.CTkLabel(self.logo_zone, image=ctk_logo, text="").pack(side="left", padx=(0, 15))
        except Exception as e:
            print(f"Ошибка логотипа: {e}")
            ctk.CTkLabel(self.logo_zone, text="📖", font=("Inter", 32)).pack(side="left", padx=(0, 15))

        text_frame = ctk.CTkFrame(self.logo_zone, fg_color="transparent")
        text_frame.pack(side="left", fill="y")
        ctk.CTkLabel(text_frame, text=localization.get("app_title_1"), font=("Inter", 24, "bold"), text_color="#FFFFFF").pack(anchor="w")
        ctk.CTkLabel(text_frame, text=localization.get("app_title_2"), font=("Inter", 14), text_color="#E6C619").pack(anchor="w")

        # --- НАВИГАЦИЯ ---
        self.nav_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.nav_zone.pack(side="top", fill="x")

        self.create_nav_btn(localization.get("main"), command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), is_active=True, command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn(localization.get("settings"), command=lambda: controller.show_frame("SettingsPage"))

        # --- ПРОФИЛЬ ---
        self.profile_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.profile_zone.pack(side="bottom", fill="x")

        user_path = os.path.join(self.assets_dir, "User_circle.png")
        if not os.path.exists(user_path):
            user_path = os.path.join(self.assets_dir, "user_circle.png")
        if not os.path.exists(user_path):
            user_path = os.path.join(self.assets_dir, "User_cicrle.png")
        try:
            pil_user = Image.open(user_path)
            ctk_user = ctk.CTkImage(light_image=pil_user, dark_image=pil_user, size=(45, 45))
            ctk.CTkLabel(self.profile_zone, image=ctk_user, text="").pack(side="left", padx=(0, 15))
        except:
            ctk.CTkLabel(self.profile_zone, text="👤", font=("Inter", 24)).pack(side="left", padx=(0, 15))
        
        p_text = ctk.CTkFrame(self.profile_zone, fg_color="transparent")
        p_text.pack(side="left")
        ctk.CTkLabel(p_text, text="СЕЗИМАЙ", text_color="white", font=("Inter", 14, "bold")).pack(anchor="w")
        ctk.CTkLabel(p_text, text=localization.get('librarian'), text_color="#BEAC64", font=("Inter", 14)).pack(anchor="w")

        # ==========================================
        # 2. RIGHT CONTENT
        # ==========================================
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=42, pady=50)

        # --- ШАПКА ---
        self.header = ctk.CTkFrame(self.content_container, height=45, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.search_bar = ctk.CTkEntry(self.header, placeholder_text=localization.get("search_placeholder"), width=510, height=42, corner_radius=14, fg_color="#C4C4C4", text_color="black", border_width=0, font=("Inter", 14))
        self.search_bar.pack(side="left")
        self.search_bar.bind("<KeyRelease>", self.perform_search)

        self.add_btn = ctk.CTkButton(self.header, text=localization.get("add_book"), fg_color="#BEAC64", text_color="black", width=193, height=42, corner_radius=14, font=("Inter", 14, "bold"), command=self.show_add_book_modal)
        self.add_btn.pack(side="left", padx=20)

        # Выпадающее меню экспорта
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

        # --- ТАБЛИЦА ---
        self.table_frame = ctk.CTkFrame(self.content_container, fg_color="#D9D9D9", corner_radius=16, border_width=1, border_color="black")
        self.table_frame.pack(fill="both", expand=True)

        self.headers = [localization.get("inv_num"), localization.get("book_title"), localization.get("author"), localization.get("genre"), localization.get("status"), localization.get("place")]
        self.load_data()

    # --- ЛОГИКА ТАБЛИЦЫ ---
    def perform_search(self, event):
        query = self.search_bar.get().strip()
        self.load_data(search_query=query)

    def load_data(self, search_query=""):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        for i, h in enumerate(self.headers):
            ctk.CTkLabel(self.table_frame, text=h, font=("Inter", 13, "bold"), text_color="black").grid(row=0, column=i, padx=20, pady=15, sticky="nsew")
            self.table_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkFrame(self.table_frame, height=1, fg_color="black").grid(row=1, column=0, columnspan=6, sticky="ew")

        books = database.search_books(search_query) if search_query else database.get_all_books()

        for row_idx, row_data in enumerate(books, start=2):
            for col_idx, item in enumerate(row_data):
                # Динамическая локализация текста статусов в таблице
                if item in ["В наличии", "Выдана"] or item in [localization.get("in_stock"), localization.get("borrowed")]:
                    is_stock = item in ["В наличии", localization.get("in_stock")]
                    color = "#80A488" if is_stock else "#B8A45F"
                    display_status = localization.get("in_stock") if is_stock else localization.get("borrowed")
                    
                    badge = ctk.CTkFrame(self.table_frame, fg_color=color, corner_radius=10)
                    badge.grid(row=row_idx, column=col_idx, padx=5, pady=5)
                    ctk.CTkLabel(badge, text=display_status, text_color="white", font=("Inter", 12)).pack(padx=10, pady=2)
                else:
                    ctk.CTkLabel(self.table_frame, text=str(item), text_color="black", font=("Inter", 13)).grid(row=row_idx, column=col_idx, padx=5, pady=10)
            ctk.CTkFrame(self.table_frame, height=1, fg_color="#A0A0A0").grid(row=row_idx*2+1, column=0, columnspan=6, sticky="ew")
    
    def show_add_book_modal(self):
        if hasattr(self, "modal_frame") and self.modal_frame.winfo_exists():
            return

        # Главный контейнер модального окна ( 797 x 597 ) возвращается на right_container
        self.modal_frame = ctk.CTkFrame(self.content_container, width=797, height=597, fg_color="#E8E8E8", corner_radius=9, border_width=1, border_color="#B0B0B0")
        self.modal_frame.place(relx=0.5, rely=0.5, anchor="center") 
        self.modal_frame.grid_propagate(False)

        # Контейнер-обертка для элементов
        fields_wrap = ctk.CTkFrame(self.modal_frame, width=797, height=597, fg_color="transparent")
        fields_wrap.place(x=0, y=0)

        # Координаты и зазоры по макету Figma
        x_col0, x_col1, x_col2 = 42, 310, 578
        y_row1_lbl = 40
        y_row1_entry = y_row1_lbl + 60
        y_row2_lbl = y_row1_entry + 95 + 46
        y_row2_entry = y_row2_lbl + 60

        # Функция генерации идеальных блоков с обводкой и тенями
        def create_field(parent, x, y, label_key, entry_width=177):
            # 1. Текстовый лейбл (идеально круглые углы через CTkButton)
            lbl = ctk.CTkButton(parent, width=entry_width, height=34, corner_radius=16,
                                text=localization.get(label_key), font=("Inter", 13),
                                fg_color="#D9D9D9", border_width=1, border_color="white",
                                text_color="black", text_color_disabled="black", state="disabled")
            lbl.place(x=x, y=y)

            # 2. 1-пиксельная линия-тень под инпутом
            shadow = ctk.CTkFrame(parent, width=entry_width, height=1, fg_color="#B0B0B0")
            shadow.place(x=x + 2, y=y + 60 + 95)

            # 3. Фрейм-подложка для инпута
            entry_background = ctk.CTkFrame(parent, width=entry_width, height=95, corner_radius=16,
                                            fg_color="#D9D9D9", border_width=1, border_color="#B0B0B0")
            entry_background.place(x=x, y=y + 60)
            entry_background.pack_propagate(False)

            # 4. Само поле ввода (прозрачное)
            entry = ctk.CTkEntry(entry_background, font=("Inter", 15), text_color="black", 
                                 fg_color="transparent", border_width=0)
            entry.pack(fill="both", expand=True, padx=15, pady=5)
            
            return entry

        # Отрисовка полей ввода (Ряд 1)
        self.entry_title = create_field(fields_wrap, x_col0, y_row1_lbl, "book_title", entry_width=245)
        self.entry_author = create_field(fields_wrap, x_col1, y_row1_lbl, "author", entry_width=245)
        self.entry_id = create_field(fields_wrap, x_col2, y_row1_lbl, "inv_num", entry_width=177)

        # Отрисовка полей ввода (Ряд 2)
        self.entry_genre = create_field(fields_wrap, x_col0, y_row2_lbl, "genre", entry_width=245)
        self.entry_place = create_field(fields_wrap, x_col1, y_row2_lbl, "place", entry_width=245)

        # --- КНОПКИ УПРАВЛЕНИЯ ---
        btn_cancel = ctk.CTkButton(fields_wrap, text="ОТМЕНА", font=("Inter", 20, "bold"), 
                                   fg_color="transparent", text_color="black", hover_color="#D9D9D9",
                                   width=160, height=70, command=self.modal_frame.destroy)
        btn_cancel.place(x=380, y=485)

        btn_add_shadow = ctk.CTkFrame(fields_wrap, width=211, height=1, fg_color="#8A7A3E")
        btn_add_shadow.place(x=545 + 2, y=485 + 70)

        btn_add = ctk.CTkButton(fields_wrap, width=211, height=70, text="ДОБАВИТЬ КНИГУ", 
                                fg_color="#BEAC64", text_color="white", hover_color="#A89755", 
                                corner_radius=16, border_width=1, border_color="#8A7A3E", 
                                font=("Inter", 18, "bold"), command=self.save_new_book)
        btn_add.place(x=545, y=485)


    def save_new_book(self):
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        inv_no = self.entry_id.get().strip()
        genre = self.entry_genre.get().strip()
        place = self.entry_place.get().strip()

        if title and author and inv_no and genre and place:
            database.add_book(inv_no, title, author, genre, place)
            self.load_data() 
            
            if "DashboardPage" in self.controller.frames:
                self.controller.frames["DashboardPage"].refresh_data()
            if "ReportsPage" in self.controller.frames:
                self.controller.frames["ReportsPage"].refresh_reports()
                
            # Уничтожаем окно напрямую
            self.modal_frame.destroy()
    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#BEAC64" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, text_color="white", font=("Inter", 20), anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", pady=5)

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
