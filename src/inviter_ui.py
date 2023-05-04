from tkinter import *
from main import UserInviter


class InviterGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("Telegram Inviter")
        self.window.geometry('400x450')
        self.add_buttons()
        self.window.mainloop()

    def add_buttons(self):
        btn1 = Button(self.window, text="Парсинг")
        btn1.grid(column=1, row=1)
        btn2 = Button(self.window, text="Инвайтинг", command=self.invite_users())
        btn2.grid(column=1, row=2)
        btn3 = Button(self.window, text="Спам смс")
        btn3.grid(column=1, row=3)

    def invite_users(self):
        print('invite_users')
        API_ID = Entry(self.window, width=10)
        API_HASH = Entry(self.window, width=10)

        print(API_ID.get(), API_HASH.get())
        # inviter = UserInviter(API_ID, API_HASH)


tg = InviterGUI()
