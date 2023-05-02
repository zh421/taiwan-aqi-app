from morePage import GUI 
import tkinter as tk
from tkinter import ttk
import asset.style as st
import webbrowser
from mainPage import MainPage

def gotoEPA():
    webbrowser.open("https://data.epa.gov.tw/api-term")

def setApiKey(apiKey):
    if len(apiKey) >0:
                    credentials = open("info/api.txt", "w+")
                    credentials.write(apiKey)
                    credentials.close()
                    tk.messagebox.showinfo("Information", "apiKey已紀錄")

class settingPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        # UI
        label1 = tk.Label(self.main_frame, font=("Verdana", 20), text="設置")
        label1.pack(side="top")

        frame_setting_form = tk.Frame(self.main_frame, bg="white", relief="groove", bd=2)  
        frame_setting_form.pack(pady=100)

        label_api = tk.Label(frame_setting_form, st.text_styles, text="行政院環境環保署api:")
        label_api.grid(row=1, padx=10, column=0)

        entry_api = ttk.Entry(frame_setting_form, width=45, cursor="xterm")
        entry_api.grid(row=1, pady=25, padx=10, column=1)

        button = ttk.Button(frame_setting_form, text="行政院環境環保署api申請", command=lambda: gotoEPA())
        button.grid(row=2, pady=25, padx=10, column=0, sticky='w')

        button = ttk.Button(frame_setting_form, text="確認", command=lambda: setApiKey(entry_api.get()))
        button.grid(row=2, pady=25, padx=10, column=1, sticky='e')

        button = ttk.Button(frame_setting_form, text="前往查詢頁面", command=lambda: controller.show_frame(MainPage))
        button.grid(row=3, pady=5, padx=10, column=1, sticky='e')