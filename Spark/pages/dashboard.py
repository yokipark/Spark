import customtkinter as ctk
import database
import localization
import os
from PIL import Image
import services.export_service as export_service
from tkinter import messagebox  # для уведомления об успешном сохранении
class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF")
        self.controller = controller

        # Настраиваем пуленепробиваемый путь к папке assets
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(os.path.dirname(current_dir), "assets")

        # ==========================================
        # 1. SIDEBAR (Width: 370px)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=370, corner_radius=0, fg_color="#294730")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) 

        self.sidebar_inner = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_inner.pack(fill="both", expand=True, padx=32, pady=(50, 25))

        # --- ЗОНА ЛОГОТИПА И ТЕКСТА ---
        self.logo_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.logo_zone.pack(side="top", fill="x", pady=(0, 40)) 

        # 1. Иконка слева
        logo_path = os.path.join(self.assets_dir, "library_icon.png")
        try:
            pil_logo = Image.open(logo_path)
            ctk_logo = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(50, 50))
            logo_display = ctk.CTkLabel(self.logo_zone, image=ctk_logo, text="")
            logo_display.pack(side="left", padx=(0, 15))
        except Exception as e:
            print(f"Ошибка логотипа: {e}")
            ctk.CTkLabel(self.logo_zone, text="📖", font=("Inter", 32)).pack(side="left", padx=(0, 15))

        # 2. Текст справа от иконки
        text_frame = ctk.CTkFrame(self.logo_zone, fg_color="transparent")
        text_frame.pack(side="left", fill="y")
        ctk.CTkLabel(text_frame, text="Картотека", font=("Inter", 24, "bold"), text_color="#FFFFFF").pack(anchor="w")
        ctk.CTkLabel(text_frame, text="библиотекаря", font=("Inter", 14), text_color="#E6C619").pack(anchor="w", pady=(0, 0))


        # --- НАВИГАЦИЯ ---
        self.nav_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.nav_zone.pack(side="top", fill="x")

        self.create_nav_btn(localization.get("main"), is_active=True, command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), command=lambda: controller.show_frame("ReportsPage"))
        self.create_nav_btn(localization.get("settings"), command=lambda: controller.show_frame("SettingsPage"))

        # --- ЗОНА ПРОФИЛЯ ---
        self.profile_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.profile_zone.pack(side="bottom", fill="x")

        # Загрузка аватарки
        user_path = os.path.join(self.assets_dir, "User_circle.png")
        if not os.path.exists(user_path):
            user_path = os.path.join(self.assets_dir, "User_cicrle.png") 

        try:
            pil_user = Image.open(user_path)
            ctk_user = ctk.CTkImage(light_image=pil_user, dark_image=pil_user, size=(45, 45))
            user_display = ctk.CTkLabel(self.profile_zone, image=ctk_user, text="")
            user_display.pack(side="left", padx=(0, 15))
        except Exception as e:
            print(f"Ошибка аватара: {e}")
            ctk.CTkLabel(self.profile_zone, text="👤", font=("Inter", 24)).pack(side="left", padx=(0, 15))

        # Фрейм для вертикального выравнивания текста профиля
        profile_text_frame = ctk.CTkFrame(self.profile_zone, fg_color="transparent")
        profile_text_frame.pack(side="left", fill="y")
        ctk.CTkLabel(profile_text_frame, text="СЕЗИМАЙ", text_color="white", font=("Inter", 14, "bold")).pack(anchor="w")
        ctk.CTkLabel(profile_text_frame, text=localization.get('librarian'), text_color="#BEAC64", font=("Inter", 14)).pack(anchor="w")

        # ==========================================
        # 2. RIGHT CONTAINER (Responsive Grid Layout)
        # ==========================================
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.pack(side="right", fill="both", expand=True)

        # --- 1. ШАПКА И ПОИСК ---
        self.header_frame = ctk.CTkFrame(self.right_container, height=45, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=42, pady=(50, 0))

        self.search_bar = ctk.CTkEntry(self.header_frame, placeholder_text=localization.get("search_placeholder"), width=510, height=42, corner_radius=14, fg_color="#C4C4C4", text_color="black", border_width=0, font=("Inter", 14))
        self.search_bar.pack(side="left")

        self.add_book_btn = ctk.CTkButton(self.header_frame, text=localization.get("add_book"), fg_color="#BEAC64", text_color="black", width=193, height=42,command=self.show_add_book_modal, corner_radius=14, font=("Inter", 14, "bold"))
        self.add_book_btn.pack(side="left", padx=(20, 0))

        # Превращаем кнопку в выпадающее меню из 3-х вариантов
        self.export_btn = ctk.CTkOptionMenu(
            self.header_frame, # или фрейм, куда пакуется кнопка (например, self.header_frame)
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
        self.export_btn.set(localization.get("export")) # Устанавливаем изначальный текст "Экспорт"
        self.export_btn.pack(side="left", padx=(20, 0)) # или side="right" в зависимости от страницы

        # --- 2. СТАТИСТИКА ---
        self.stats_frame = ctk.CTkFrame(self.right_container, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=42, pady=(50, 0))
        self.stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        stats = database.get_dashboard_stats()
        
        self.lbl_books = self.create_stat_card(self.stats_frame, localization.get("books_on_loan"), str(stats[0]), "check.png", col=0)
        self.lbl_overdue = self.create_stat_card(self.stats_frame, localization.get("overdue"), str(stats[1]), "alert.png", col=1)
        self.lbl_readers = self.create_stat_card(self.stats_frame, localization.get("new_readers"), str(stats[2]), "user_icon.png", col=2)


        # --- 3. СРЕДНИЙ РЯД ---
        self.middle_frame = ctk.CTkFrame(self.right_container, fg_color="transparent")
        self.middle_frame.pack(fill="both", expand=True, padx=42, pady=(50, 0))
        self.middle_frame.grid_columnconfigure(0, weight=2)
        self.middle_frame.grid_columnconfigure(1, weight=1)
        self.middle_frame.grid_rowconfigure(0, weight=1)

        # Graph Box
        self.graph_box = ctk.CTkFrame(self.middle_frame, fg_color="#D9D9D9", corner_radius=16, border_width=1, border_color="black")
        self.graph_box.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        self.graph_box.pack_propagate(False)
        
        ctk.CTkLabel(self.graph_box, text=localization.get("weekly_activity"), font=("Inter", 32), text_color="black").pack(pady=(15, 5), anchor="w", padx=20)
        self.draw_weekly_chart(self.graph_box)

        # Quick Actions Box
        self.actions_box = ctk.CTkFrame(self.middle_frame, fg_color="#D9D9D9", corner_radius=16, border_width=1, border_color="black")
        self.actions_box.grid(row=0, column=1, sticky="nsew")
        self.actions_box.pack_propagate(False)
        
        ctk.CTkLabel(self.actions_box, text=f"{localization.get('quick')} \n {localization.get('actions')}", font=("Inter", 32), text_color="black").pack(pady=(9, 9))
        
        btn_issue = ctk.CTkButton(self.actions_box, text=localization.get("quick_issue"), fg_color="#304146", height=45, corner_radius=20, border_width=1, border_color="#1F2A2E", font=("Inter", 14), command=lambda: controller.show_frame("IssueReturnPage"))
        btn_issue.pack(pady=8, padx=20, fill="x")

        btn_return = ctk.CTkButton(self.actions_box, text=localization.get("accept_return"), fg_color="#304146", height=45, corner_radius=20, border_width=1, border_color="#1F2A2E", font=("Inter", 14), command=lambda: controller.show_frame("IssueReturnPage"))
        btn_return.pack(pady=8, padx=20, fill="x")

        btn_add_reader = ctk.CTkButton(self.actions_box, text=localization.get("add_reader"), fg_color="#304146", height=45, corner_radius=20, border_width=1, border_color="#1F2A2E", font=("Inter", 14), command=lambda: controller.show_frame("ReaderPage"))
        btn_add_reader.pack(pady=8, padx=20, fill="x")


        # --- 4. ТАБЛИЦА ТРАНЗАКЦИЙ ---
        self.table_box = ctk.CTkFrame(self.right_container, height=222, fg_color="#D9D9D9", corner_radius=16, border_width=1, border_color="black")
        self.table_box.pack(fill="both", expand=True, padx=42, pady=(50, 42))
        self.table_box.pack_propagate(False)
        
        ctk.CTkLabel(self.table_box, text=localization.get("recent_actions"), font=("Inter", 32), text_color="black").pack(anchor="w", padx=20, pady=(10, 5))
        
        self.transactions_frame = ctk.CTkFrame(self.table_box, fg_color="transparent")
        self.transactions_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        self.load_recent_transactions()


    # --- REFRESH MAPPED ---
    def refresh_data(self):
        stats = database.get_dashboard_stats()
        self.lbl_books.configure(text=str(stats[0]))
        self.lbl_overdue.configure(text=str(stats[1]))
        self.lbl_readers.configure(text=str(stats[2]))

        for widget in self.transactions_frame.winfo_children():
            widget.destroy()
        self.load_recent_transactions()
        self.draw_weekly_chart(self.graph_box)

    # --- NAVIGATION GENERATOR ---
    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#BEAC64" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, text_color="white", font=("Inter", 20),
                            anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", pady=5)

    # --- STAT CARD CONFIGURATION ---
    def create_stat_card(self, parent, title, value, icon_filename, col):
        card = ctk.CTkFrame(parent, fg_color="#D9D9D9", height=162, corner_radius=16, border_width=1, border_color="black")
        card.grid(row=0, column=col, sticky="nsew", padx=(0, 20 if col < 2 else 0))
        card.pack_propagate(False)
        
        ctk.CTkLabel(card, text=title, font=("Inter", 16), text_color="black").place(x=15, y=10)
        val_label = ctk.CTkLabel(card, text=value, font=("Inter", 42, "bold"), text_color="black")
        val_label.place(x=15, y=55)
        
        asset_path = os.path.join(self.assets_dir, icon_filename)
        try:
            pil_img = Image.open(asset_path)
            ctk_icon = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(40, 40))
            icon_display = ctk.CTkLabel(card, image=ctk_icon, text="")
            icon_display.place(relx=0.82, rely=0.6, anchor="center")
        except Exception as e:
            fallback_label = ctk.CTkLabel(card, text="⚙️", font=("Inter", 24))
            fallback_label.place(relx=0.82, rely=0.6, anchor="center")
            
        return val_label

    # --- CANVAS CHART ENGINE ---
    def draw_weekly_chart(self, parent):
        for widget in parent.winfo_children():
            if isinstance(widget, ctk.CTkCanvas):
                widget.destroy()
            
        canvas = ctk.CTkCanvas(parent, height=220, bg="#D9D9D9", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        for i, val in enumerate(["40", "30", "20", "10", "0"]):
            y = 25 + (i * 35)
            canvas.create_text(15, y, text=val, fill="#707070", font=("Inter", 10))
            canvas.create_line(35, y, 540, y, fill="#A0A0A0")

       
        days = localization.get("graph_days")
        heights = database.get_weekly_activity() 

        for i in range(7):
            x0 = 60 + (i * 65)
            bar_height = min(heights[i], 40) 
            y0 = 165 - (bar_height * 3.5) 
            x1 = x0 + 30
            y1 = 165
            
            if heights[i] == 0:
                canvas.create_rectangle(x0, 163, x1, y1, fill="#A0A0A0", outline="")
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill="#2E9E4A", outline="")
                
            canvas.create_text(x0 + 15, 190, text=days[i], fill="black", font=("Inter", 10))

    # --- AUDIT STREAM ---
    def load_recent_transactions(self):
        headers = [
            localization.get("inv_num"),
            localization.get("book_title"),
            localization.get("reader_name"),
            localization.get("actions"),
            localization.get("time")
        ]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.transactions_frame, text=h, font=("Inter", 12, "bold"), text_color="gray").grid(row=0, column=i, padx=5, pady=5, sticky="w")
            self.transactions_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkFrame(self.transactions_frame, height=1, fg_color="gray").grid(row=1, column=0, columnspan=5, sticky="ew", pady=(0, 5))

        transactions = database.get_recent_transactions(limit=4)
        if not transactions:
            transactions = [
                ("90021", "История искусств", "Кузнецова М.К", "Возврат", "08:55"),
                ("12005", "Мастер и Маргарита", "Иванов А.С.", "Выдача", "10:15")
            ]

        for row_idx, row_data in enumerate(transactions, start=2):
            for col_idx, item in enumerate(row_data):
                color = "black"
                if col_idx == 3:
                    color = "#2E9E4A" if item == "Возврат" else "#B8A45F"

                ctk.CTkLabel(self.transactions_frame, text=str(item), text_color=color, font=("Inter", 13)).grid(row=row_idx, column=col_idx, padx=5, pady=4, sticky="w")
            
            ctk.CTkFrame(self.transactions_frame, height=1, fg_color="#A0A0A0").grid(row=row_idx*2+1, column=0, columnspan=5, sticky="ew")
    def trigger_data_export(self, choice):
        """Вызывается автоматически при выборе формата в выпадающем меню кнопки Экспорт"""
        try:
            if choice == "JSON":
                path = export_service.export_to_json()
            elif choice == "Excel":
                path = export_service.export_to_excel()
            elif choice == "PDF":
                path = export_service.export_to_pdf()
            
            # Возвращаем текст кнопки обратно на "Экспорт"
            self.export_btn.set(localization.get("export"))
            
            # Показываем красивое системное уведомление об успешном экспорте
            filename = os.path.basename(path)
            messagebox.showinfo("Экспорт завершен", f"Данные успешно выгружены в файл:\\n{filename}\\n\\nИщите файл в папке 'exports/'")
        except Exception as e:
            self.export_btn.set(localization.get("export"))
            messagebox.showerror("Ошибка экспорта", f"Не удалось выполнить экспорт:\\n{str(e)}")
    def show_add_book_modal(self):
        if hasattr(self, "modal_frame") and self.modal_frame.winfo_exists():
            return

        self.modal_frame = ctk.CTkFrame(self.right_container, fg_color="#E8E8E8", corner_radius=15, border_width=1, border_color="#B0B0B0")
        self.modal_frame.place(relx=0.5, rely=0.4, anchor="center") 
        self.modal_frame.pack_propagate(False)
        self.modal_frame.configure(width=750, height=350)

        inner = ctk.CTkFrame(self.modal_frame, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(inner, text=localization.get("book_title"), text_color="black", font=("Inter", 13)).grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w")
        ctk.CTkLabel(inner, text=localization.get("author"), text_color="black", font=("Inter", 13)).grid(row=0, column=1, padx=10, pady=(0, 5), sticky="w")
        ctk.CTkLabel(inner, text=localization.get("inv_num"), text_color="black", font=("Inter", 13)).grid(row=0, column=2, padx=10, pady=(0, 5), sticky="w")

        self.entry_title = ctk.CTkEntry(inner, width=220, height=45, fg_color="#D9D9D9", text_color="black", font=("Inter", 14))
        self.entry_title.grid(row=1, column=0, padx=10, pady=(0, 20))
        
        self.entry_author = ctk.CTkEntry(inner, width=220, height=45, fg_color="#D9D9D9", text_color="black", font=("Inter", 14))
        self.entry_author.grid(row=1, column=1, padx=10, pady=(0, 20))
        
        self.entry_id = ctk.CTkEntry(inner, width=150, height=45, fg_color="#D9D9D9", text_color="black", font=("Inter", 14))
        self.entry_id.grid(row=1, column=2, padx=10, pady=(0, 20))

        ctk.CTkLabel(inner, text=localization.get("genre"), text_color="black", font=("Inter", 13)).grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")
        ctk.CTkLabel(inner, text=localization.get("place"), text_color="black", font=("Inter", 13)).grid(row=2, column=1, padx=10, pady=(0, 5), sticky="w")

        self.entry_genre = ctk.CTkEntry(inner, width=220, height=45, fg_color="#D9D9D9", text_color="black", font=("Inter", 14))
        self.entry_genre.grid(row=3, column=0, padx=10, pady=(0, 30))
        
        self.entry_place = ctk.CTkEntry(inner, width=220, height=45, fg_color="#D9D9D9", text_color="black", font=("Inter", 14))
        self.entry_place.grid(row=3, column=1, padx=10, pady=(0, 30))

        ctk.CTkButton(inner, text=localization.get("add_book"), font=("Inter", 16, "bold"), fg_color="#B8A45F", text_color="black", width=160, height=50, corner_radius=10, command=self.save_new_book).grid(row=4, column=2, sticky="e")
        ctk.CTkButton(inner, text=localization.get("cancel"), fg_color="transparent", text_color="gray", hover_color="#D9D9D9", font=("Inter", 16), command=self.modal_frame.destroy).grid(row=4, column=1, sticky="e", padx=10)

    def save_new_book(self):
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        inv_no = self.entry_id.get().strip()
        genre = self.entry_genre.get().strip()
        place = self.entry_place.get().strip()

        if title and author and inv_no and genre and place:
            database.add_book(inv_no, title, author, genre, place)
            
            # МГНОВЕННО ОБНОВЛЯЕМ КНИЖНЫЙ ФОНД (MainPage)
            if "MainPage" in self.controller.frames:
                self.controller.frames["MainPage"].load_data()
            
            # Обновляем текущий Дашборд (статистика, график, транзакции)
            self.refresh_data()
            
            # Обновляем Отчеты
            if "ReportsPage" in self.controller.frames:
                self.controller.frames["ReportsPage"].refresh_reports()
                
            self.modal_frame.destroy()
    
