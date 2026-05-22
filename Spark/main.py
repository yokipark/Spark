import customtkinter as ctk
import database  

from pages.login import LoginPage
from pages.book_fund import MainPage
from pages.dashboard import DashboardPage
from pages.readers import ReaderPage
from pages.issue_return import IssueReturnPage
from pages.reports import ReportsPage
from pages.settings import SettingsPage
from pages.loading import LoadingPage
database.init_db() 

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Картотека")
        self.geometry("1440x1024")
        
        # Главный контейнер
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # Создаем все экраны
        self.init_frames()
        
        # Запускаем загрузочный экран!
        self.show_frame("LoadingPage")
        self.frames["LoadingPage"].animate_loading()

    def init_frames(self):
        """Создает (или пересоздает) все страницы"""
        # ВНИМАНИЕ: Если у тебя есть ReportsPage, добавь его в эти скобки!
        for PageClass in (LoadingPage, LoginPage, MainPage, DashboardPage, ReaderPage, IssueReturnPage, ReportsPage, SettingsPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """Переключает видимый экран"""
        frame = self.frames[page_name]
        frame.tkraise()

    def rebuild_ui(self):
        """Удаляет старые окна и рисует их заново с новым языком!"""
        # Удаляем старые фреймы
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()
        
        # Рисуем заново
        self.init_frames()
        
        # Возвращаем пользователя на страницу настроек
        self.show_frame("SettingsPage")
    def change_global_theme(self, mode):
        """Переключает тему CustomTkinter и обновляет fg_color у всех фреймов"""
        if mode == "dark":
            ctk.set_appearance_mode("dark")
            bg_color = "#6D6D6D"  # Твой кастомный темный цвет
        else:
            ctk.set_appearance_mode("light")
            bg_color = "#FFFFFF"  # Стандартный белый

        # Проходимся по всем инициализированным страницам в системе
        for page_name, page_instance in self.frames.items():
            try:
                page_instance.configure(fg_color=bg_color)
            except Exception as e:
                print(f"Не удалось перекрасить фрейм {page_name}: {e}")
if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
