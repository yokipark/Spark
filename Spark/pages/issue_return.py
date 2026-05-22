import customtkinter as ctk
import database
import localization
import os
from PIL import Image
import services.export_service as export_service
from tkinter import messagebox  # для уведомления об успешном сохранении
class IssueReturnPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#FFFFFF")
        self.controller = controller

        # Настраиваем путь к папке assets
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
            logo_display = ctk.CTkLabel(self.logo_zone, image=ctk_logo, text="")
            logo_display.pack(side="left", padx=(0, 15))
        except Exception as e:
            print(f"Ошибка логотипа: {e}")
            ctk.CTkLabel(self.logo_zone, text="📖", font=("Inter", 32)).pack(side="left", padx=(0, 15))

        text_frame = ctk.CTkFrame(self.logo_zone, fg_color="transparent")
        text_frame.pack(side="left", fill="y")
        ctk.CTkLabel(text_frame, text="Картотека", font=("Inter", 24, "bold"), text_color="#FFFFFF").pack(anchor="w")
        ctk.CTkLabel(text_frame, text="библиотекаря", font=("Inter", 14), text_color="#E6C619").pack(anchor="w")
        
        # --- НАВИГАЦИЯ ---
        self.nav_zone = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        self.nav_zone.pack(side="top", fill="x")

        self.create_nav_btn(localization.get("main"), command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn(localization.get("books"), command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn(localization.get("readers"), command=lambda: controller.show_frame("ReaderPage"))
        self.create_nav_btn(localization.get("issue"), is_active=True, command=lambda: controller.show_frame("IssueReturnPage"))
        self.create_nav_btn(localization.get("reports"), command=lambda: controller.show_frame("ReportsPage"))
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
            user_display = ctk.CTkLabel(self.profile_zone, image=ctk_user, text="")
            user_display.pack(side="left", padx=(0, 15))
        except Exception as e:
            print(f"Ошибка аватара: {e}")
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

        # --- ВЕРХНЯЯ ШАПКА ---
        self.header = ctk.CTkFrame(self.content, height=45, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))
        
        self.search_bar = ctk.CTkEntry(self.header, placeholder_text=localization.get("search_placeholder"), width=510, height=42, corner_radius=14, fg_color="#C4C4C4", text_color="black", border_width=0, font=("Inter", 14))
        self.search_bar.pack(side="left")
        
        # Превращаем кнопку в выпадающее меню из 3-х вариантов
        self.export_btn = ctk.CTkOptionMenu(
            self.header, # или фрейм, куда пакуется кнопка (например, self.header_frame)
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
        # Информационный статус-лейбл для вывода сообщений
        self.status_label = ctk.CTkLabel(self.content, text="", font=("Inter", 14, "bold"), text_color="black")
        self.status_label.pack(pady=(0, 20))

        # --- ОСНОВНОЙ СПЛИТ-ИНТЕРФЕЙС ---
        self.body = ctk.CTkFrame(self.content, fg_color="transparent")
        self.body.pack(fill="both", expand=True)
        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_columnconfigure(1, weight=1)
        self.body.grid_rowconfigure(0, weight=1)

        # ------------------------------------------
        # ЛЕВАЯ КОЛОНКА: ОФОРМЛЕНИЕ ВЫДАЧИ КНИГИ
        # ------------------------------------------
        left_col = ctk.CTkFrame(self.body, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        ctk.CTkLabel(left_col, text=localization.get("issue").upper(), font=("Inter", 32, "bold"), text_color="black").pack(anchor="w", pady=(0, 20))

        # Контейнер для двух полей ввода, стоящих рядом (side-by-side)
        inputs_frame = ctk.CTkFrame(left_col, fg_color="transparent")
        inputs_frame.pack(fill="x", pady=(0, 20))
        
        # Поле: Код читателя
        id_frame1 = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        id_frame1.pack(side="left", padx=(0, 20))
        ctk.CTkLabel(id_frame1, text=localization.get("reader_id"), text_color="black", font=("Inter", 14)).pack(anchor="w", pady=(0, 5))
        self.reader_id_entry = ctk.CTkEntry(id_frame1, width=180, height=42, corner_radius=14, fg_color="#C4C4C4", border_width=0, font=("Inter", 14), text_color="black")
        self.reader_id_entry.pack()

        # Поле: Код книги
        id_frame2 = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        id_frame2.pack(side="left")
        ctk.CTkLabel(id_frame2, text=localization.get("inv_num"), text_color="black", font=("Inter", 14)).pack(anchor="w", pady=(0, 5))
        self.book_id_issue_entry = ctk.CTkEntry(id_frame2, width=180, height=42, corner_radius=14, fg_color="#C4C4C4", border_width=0, font=("Inter", 14), text_color="black")
        self.book_id_issue_entry.pack()

        # Кнопка подтверждения выдачи
        ctk.CTkButton(left_col, text=localization.get("issue"), fg_color="#8A9E8A", text_color="black", font=("Inter", 16, "bold"), height=50, corner_radius=14, border_width=1, border_color="#5D6B5D", command=self.handle_issue).pack(fill="x", pady=(20, 0))

        # ------------------------------------------
        # ПРАВАЯ КОЛОНКА: ОФОРМЛЕНИЕ ВОЗВРАТА КНИГИ
        # ------------------------------------------
        right_col = ctk.CTkFrame(self.body, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        # Карточка возврата (Серый блок с обводкой)
        book_card = ctk.CTkFrame(right_col, fg_color="#D9D9D9", corner_radius=16, border_width=1, border_color="black")
        book_card.pack(fill="x", pady=(55, 10))
        book_card.pack_propagate(False)
        book_card.configure(height=260) # Фиксируем высоту карточки для сохранения пропорций

        ctk.CTkLabel(book_card, text=localization.get("accept_return").upper(), font=("Inter", 24, "bold"), text_color="black").pack(anchor="w", padx=20, pady=(20, 15))

        book_inputs = ctk.CTkFrame(book_card, fg_color="transparent")
        book_inputs.pack(fill="x", padx=20, pady=(0, 15))

        # Поле: Код книги для возврата
        b_id_frame = ctk.CTkFrame(book_inputs, fg_color="transparent")
        b_id_frame.pack(side="left", padx=(0, 20))
        ctk.CTkLabel(b_id_frame, text=localization.get("inv_num"), text_color="black", font=("Inter", 14)).pack(anchor="w", pady=(0, 5))
        self.book_id_return_entry = ctk.CTkEntry(b_id_frame, width=180, height=42, corner_radius=14, fg_color="#FFFFFF", border_width=0, font=("Inter", 14), text_color="black")
        self.book_id_return_entry.pack()

        # Кнопка подтверждения возврата
        ctk.CTkButton(book_card, text=localization.get("accept_return"), fg_color="#B09B66", text_color="black", font=("Inter", 16, "bold"), height=50, corner_radius=14, border_width=1, border_color="#7A6B46", command=self.handle_return).pack(fill="x", padx=20, pady=(15, 20))

    # ==========================================
    # ЛОГИКА ВЗАИМОДЕЙСТВИЯ (Action Logic)
    # ==========================================
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
            self.show_status("Эта книга уже выдана!", "#C13C3C")
            return

        # Проводим транзакцию
        database.process_issue_db(b_inv, title, r_id, reader_name)
        self.show_status(f"Успех! Книга '{title}' выдана {reader_name}.", "#2E9E4A")
        
        self.reader_id_entry.delete(0, 'end')
        self.book_id_issue_entry.delete(0, 'end')

        # Обновляем все нужные экраны мгновенно!
        if "DashboardPage" in self.controller.frames:
            self.controller.frames["DashboardPage"].refresh_data()
        if "MainPage" in self.controller.frames:
            self.controller.frames["MainPage"].load_data()
        if "ReportsPage" in self.controller.frames:
            self.controller.frames["ReportsPage"].refresh_reports()

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

        # Оформляем возврат
        database.process_return_db(b_inv, title, 0, "Неизвестно")
        self.show_status(f"Успех! Книга '{title}' возвращена.", "#2E9E4A")
        
        self.book_id_return_entry.delete(0, 'end')

        # Обновляем все нужные экраны мгновенно!
        if "DashboardPage" in self.controller.frames:
            self.controller.frames["DashboardPage"].refresh_data()
        if "MainPage" in self.controller.frames:
            self.controller.frames["MainPage"].load_data()
        if "ReportsPage" in self.controller.frames:
            self.controller.frames["ReportsPage"].refresh_reports()
            
    def show_status(self, text, color):
        self.status_label.configure(text=text, text_color=color)
        self.after(4000, lambda: self.status_label.configure(text=""))

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#BEAC64" if is_active else "transparent"
        btn = ctk.CTkButton(self.nav_zone, text=text, fg_color=bg, text_color="white", font=("Inter", 20),
                            anchor="w", height=45, corner_radius=10, hover_color="#7C9A82", command=command)
        btn.pack(fill="x", pady=5)
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
