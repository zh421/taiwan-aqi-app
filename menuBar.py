import tkinter as tk
import widgetsPage as wp
import morePage
from mainPage import MainPage
from settingPage import settingPage

class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=menu_file)
        menu_file.add_command(label="Setting", command=lambda: parent.show_frame(settingPage))
        menu_file.add_command(label="Main", command=lambda: parent.show_frame(MainPage))
        menu_file.add_separator()
        menu_file.add_command(label="Exit Application", command=lambda: parent.Quit_1application())


        # menu_orders = tk.Menu(self, tearoff=0)
        # self.add_cascade(label="Menu2", menu=menu_orders)

        # menu_pricing = tk.Menu(self, tearoff=0)
        # self.add_cascade(label="Menu3", menu=menu_pricing)
        # menu_pricing.add_command(label="Page Wid", command=lambda: parent.show_frame(wp.Some_Widgets))

        # menu_operations = tk.Menu(self, tearoff=0)
        # self.add_cascade(label="Menu4", menu=menu_operations)
        # menu_operations.add_command(label="Page Two", command=lambda: parent.show_frame(MainPage))
        # menu_positions = tk.Menu(menu_operations, tearoff=0)
        # menu_operations.add_cascade(label="Menu5", menu=menu_positions)
        # menu_positions.add_command(label="Page Three", command=lambda: parent.show_frame(morePage.PageThree))
        # menu_positions.add_command(label="Page Four", command=lambda: parent.show_frame(morePage.PageExample))

        # menu_help = tk.Menu(self, tearoff=0)
        # self.add_cascade(label="Menu6", menu=menu_help)
        # menu_help.add_command(label="Open New Window", command=lambda: parent.OpenNewWindow())
