
import customtkinter as ctk

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controller = controller

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#4A6550")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="📖 Картотека", font=("Helvetica", 24, "bold"), text_color="#E6C619").pack(pady=(30, 0))
        
        self.create_nav_btn("🏠 Главное", is_active=True, command=lambda: controller.show_frame("DashboardPage"))
        self.create_nav_btn("📋 Книжный фонд", command=lambda: controller.show_frame("MainPage"))
        self.create_nav_btn("👤 Читатель", command=lambda: controller.show_frame("ReaderPage"))
        
        profile_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        profile_frame.pack(side="bottom", pady=20, padx=20, fill="x")
        ctk.CTkLabel(profile_frame, text="👤 СЕЗИМАЙ\nБиблиотекарь", text_color="white", justify="left").pack(side="left")

        # Content
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Stats
        self.stats_frame = ctk.CTkFrame(self.right_container, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=10)
        self.create_stat_card(self.stats_frame, "Книг на руках", "127", "✅", 0)
        self.create_stat_card(self.stats_frame, "Просрочено", "54", "❗", 1)

    def create_nav_btn(self, text, is_active=False, command=None):
        bg = "#7C9A82" if is_active else "transparent"
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color=bg, anchor="w", height=45, corner_radius=10, command=command)
        btn.pack(fill="x", padx=10, pady=5)

    def create_stat_card(self, parent, title, value, icon, col):
        card = ctk.CTkFrame(parent, fg_color="#C4C4C4", height=150, corner_radius=15)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        ctk.CTkLabel(card, text=title, font=("Helvetica", 16), text_color="black").place(x=20, y=20)
        ctk.CTkLabel(card, text=value, font=("Helvetica", 48, "bold"), text_color="black").place(x=20, y=60)
