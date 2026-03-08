import customtkinter as ctk


app = ctk.CTk()
app.title("Картотека - Вход")
app.geometry("1440x1024")

app.configure(fg_color="#4A6550")
login_frame= ctk.CTkFrame(master=app, width=516, height=732, fg_color="#cfd2d0", corner_radius=20)


login_frame.place(relx=0.5, rely=0.5, anchor="center")
title= ctk.CTkLabel( login_frame, text="Картотека", font=("Helvetica", 28, "bold"),
    text_color="black"
)

title.place(x=250, y=190, anchor="center")

subtitle= ctk.CTkLabel(login_frame,text="Библиотекаря", font=("Helvetica", 16),
    text_color="black"
)
subtitle.place(x=250, y=220, anchor="center")

# ID text
idsotrudnika= ctk.CTkLabel( master=login_frame, text="ID сотрудника", font=("Helvetica", 12),
    text_color="black"
)
idsotrudnika.place(x=60, y=300, anchor="w")

idEntry = ctk.CTkEntry( login_frame, width=380, height=45, fg_color="#bebebe",       # Darker gray for entry background
    border_color="#bebebe",  text_color="black", corner_radius=10
)
idEntry.place(x=250, y=335, anchor="center")


password= ctk.CTkLabel( login_frame, text="Пароль", font=("Helvetica", 12), text_color="#000000"
)
password.place(x=60, y=390, anchor="w")

password_entry = ctk.CTkEntry(login_frame, width=380, height=45, fg_color="#bebebe", border_color="#bebebe", text_color="black", corner_radius=10,

)
password_entry.place(x=250, y=425, anchor="center")

# Login buttton

loginButton = ctk.CTkButton(login_frame,
    text="ВОЙТИ",
    width=360,height=50,
    font=("Helvetica", 18, "bold"),fg_color="#304146", hover_color="#1f2c30",
    text_color="white",
    corner_radius=15
)
loginButton.place(x=250, y=550, anchor="center")

app.mainloop()
