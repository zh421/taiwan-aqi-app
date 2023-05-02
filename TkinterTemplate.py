import tkinter as tk
from tkinter import messagebox
import menuBar
import widgetsPage as wp
import openWindow as ow
from service import getApiKey
from morePage import PageThree, PageExample
from settingPage import settingPage
from mainPage import MainPage

"""
Useful Links:
https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter Most useful in my opinion
https://www.tutorialspoint.com/python/python_gui_programming.htm
https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html
https://www.youtube.com/watch?v=HjNHATw6XgY&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk
"""

# You can also use a pandas dataframe for pokemon_info.
# you can convert the dataframe using df.to_numpy.tolist()


class MyApp(tk.Toplevel):

    def __init__(self, loginPage, *args, **kwargs):
        global loginPageVar
        loginPageVar=loginPage

        tk.Toplevel.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self, height=800, width=1024)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        # self.resizable(0, 0) prevents the app from being resized
        # self.geometry("1024x600") fixes the applications size
        self.frames = {}
        pages = (wp.Some_Widgets, settingPage, MainPage, PageThree, PageExample)
        for F in pages:
            frame = F(main_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        # 登入後跳轉的畫面
        apiKey=getApiKey()
        if not apiKey: # no APIKey in APP
            self.show_frame(settingPage)
        else:
            self.show_frame(MainPage)
        menubar = menuBar.MenuBar(self)
        tk.Tk.config(self, menu=menubar)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def OpenNewWindow(self):
        ow.OpenNewWindow()

    # def Quit_application(self):
    #     self.destroy()

    def Quit_1application(self):
        loginPageVar.destroy()



