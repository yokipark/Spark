import customtkinter as ctk

class LoadingPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        # Темно-зеленый фон из макета
        super().__init__(parent, fg_color="#36493B") 
        self.controller = controller

        # Центральный контейнер для логотипа
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.place(relx=0.5, rely=0.45, anchor="center")

        # Пока оставляем эмодзи книги. Потом ты легко заменишь этот Label на CTkImage с твоим прозрачным PNG!
        ctk.CTkLabel(self.center_frame, text="📖", font=("Helvetica", 80), text_color="#D1C4A3").pack(pady=(0, 10))
        ctk.CTkLabel(self.center_frame, text="S p a r k", font=("Itim", 56, "bold"), text_color="white").pack()

        # Полоса загрузки внизу
        self.progress_bar = ctk.CTkProgressBar(self, width=500, height=4, fg_color="#2A382D", progress_color="#D1C4A3", corner_radius=0)
        self.progress_bar.place(relx=0.5, rely=0.85, anchor="center")
        self.progress_bar.set(0) # Начинаем с 0

        # Текст "загрузка"
        ctk.CTkLabel(self, text="загрузка", font=("Helvetica", 14), text_color="#A0A0A0").place(relx=0.5, rely=0.88, anchor="center")

    def animate_loading(self):
        """Запускает таймеры, которые двигают полоску загрузки, а потом открывают LoginPage"""
        self.progress_bar.set(0.0)
        
        # self.after(миллисекунды, функция)
        self.after(500, lambda: self.progress_bar.set(0.3))
        self.after(1200, lambda: self.progress_bar.set(0.7))
        self.after(1800, lambda: self.progress_bar.set(1.0))
        
        # Через 2.5 секунды переключаем на страницу логина!
        self.after(2500, lambda: self.controller.show_frame("LoginPage"))
