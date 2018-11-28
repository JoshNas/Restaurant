import tkinter as tk
from tkinter import messagebox, font as tkfont
import pandas as pd


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=14, weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.grid(row=0, column=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.employee_list = pd.read_csv('employees')
        self.user = None

        self.frames = {}
        for frame_name in (StartPage, LogInPage, OrderPage):
            page_name = frame_name.__name__
            frame = frame_name(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome", font=controller.title_font)
        label.grid(row=0, column=0)

        employee_window = tk.Frame(self)
        employee_window.grid(row=1, column=0)

        num = 0
        for row in range(8):
            for column in range(8):
                try:
                    tk.Button(employee_window, text=controller.employee_list['name'][num],
                              command=lambda n=num: self.select_user(n)).grid(row=row, column=column)
                    num += 1
                except KeyError:
                    break

    def select_user(self, user):
        self.controller.user = user
        self.controller.show_frame('LogInPage')


class LogInPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.current_password = ''
        label = tk.Label(self, text='Enter PIN', font=controller.title_font)
        label.grid(row=0, column=0)
        button_window = tk.Canvas(self)
        button_window.grid(row=1, column=0)

        num = 1
        for row in range(3):
            for column in range(3):
                tk.Button(button_window, text=num, command=lambda n=num: self.get_password(n))\
                    .grid(row=row, column=column, sticky='nsew')
                num += 1

        tk.Button(self, text="Return to Selection", command=lambda: controller.show_frame("StartPage"))\
            .grid(row=3, column=0)

    def get_password(self, pin):
        self.current_password += str(pin)
        if len(self.current_password) == 4:
            if str(self.controller.employee_list.at[self.controller.user, 'password']) == self.current_password:
                #  slightly faster to convert int to str for compare than vice versa
                self.controller.show_frame('OrderPage')
                self.current_password = ''  # is this necessary?
            else:
                messagebox.showinfo("Error", "Invalid PIN")
                self.current_password = ''


class OrderPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.table = None
        self.guest = None
        appetizers = pd.read_csv('appetizers.csv')
        entrees = pd.read_csv('entrees.csv')
        drinks = pd.read_csv('barmenu.csv')

        self.order = []

        self.selection_window = tk.Canvas(self)
        self.selection_window.grid(row=0, column=0, sticky='nsew')

        self.table_select = tk.Canvas(self.selection_window)
        self.table_select.grid(row=0, column=0, sticky='nsew')

        self.guest_select = tk.Canvas(self.selection_window)
        self.guest_select.grid(row=0, column=1, sticky='nsew')

        self.keypad = tk.Canvas(self)
        self.keypad.grid(row=0, column=1)

        self.appetizer_window = tk.Canvas(self.keypad)
        self.appetizer_window.grid(row=0, column=0, sticky='new')

        self.entree_window = tk.Canvas(self.keypad)
        self.entree_window.grid(row=1, column=0, sticky='new', pady=15)

        self.drink_window = tk.Canvas(self.keypad)
        self.drink_window.grid(row=2, column=0, sticky='nsew', pady=15)

        self.display_window = tk.Canvas(self)
        self.display_window.grid(row=0, column=3)

        self.info_window = tk.Canvas(self)
        self.info_window.grid(row=0, column=0)

        self.order_window = tk.Text(self.display_window)
        self.order_window.grid(row=1, column=0)

        self.order_window = tk.Text(self.display_window)
        self.order_window.grid(row=2, column=0)

        self.price_window = tk.Text(self.display_window)
        self.price_window.grid(row=3, column=1)

        # TODO: make number of tables adjustable by manager
        num = 1
        for row in range(16):
            tk.Button(self.table_select, text=f'Table {num}', command=lambda n=num: self.set_table(n))\
                .grid(row=row, column=0, sticky='nsew')
            num += 1

        num = 1
        for row in range(16):
            tk.Button(self.guest_select, text=f'Guest {num}', command=lambda n=num: self.set_guest(n)) \
                .grid(row=row, column=0, sticky='nsew')
            num += 1

        num = 0
        for row in range(3):
            for column in range(6):
                try:
                    tk.Button(self.appetizer_window, text=f'{appetizers.iloc[num][0]}',
                              command=lambda n=num: self.add_to_order(appetizers.iloc[n][0], appetizers.iloc[n][1]),
                              width=15).grid(row=row, column=column, sticky='nsew')
                    num += 1
                except IndexError:
                    break

        num = 0
        for row in range(6):
            for column in range(6):
                try:
                    tk.Button(self.entree_window, text=f'{entrees.iloc[num][0]}',
                              command=lambda n=num: self.add_to_order(entrees.iloc[n][0], entrees.iloc[n][1]),
                              width=15).grid(row=row, column=column, sticky='nsew')
                    num += 1
                except IndexError:
                    break

        num = 0
        for row in range(4):
            for column in range(6):
                try:
                    tk.Button(self.drink_window, text=f'{drinks.iloc[num][0]}',
                              command=lambda n=num: self.add_to_order(drinks.iloc[n][0], drinks.iloc[n][1]),
                              width=15).grid(row=row, column=column, sticky='nsew')
                    num += 1
                except IndexError:
                    break

    def set_table(self, table):
        self.table = table

    def set_guest(self, guest):
        self.guest = guest

    def add_to_order(self, item, price):
        self.order.append([item, price])
        self.order_window.insert('end', f'{item} {price}\n')



if __name__ == "__main__":
    app = App()
    app.geometry('1220x820')
    app.mainloop()
