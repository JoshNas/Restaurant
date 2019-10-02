import tkinter as tk
from tkinter import messagebox, font as tkfont
from tkinter.messagebox import showinfo
import pandas as pd
import datetime as dt
from Database import database_interaction as dbi


def popup(message):
    showinfo("Error", message)


class App(tk.Tk):
    """This will be our base. The container our frames will be stacked on. We will chose which frame to start on then
    use the show_frame function, which will be called by the frames,  to move between them."""
    def __init__(self):
        tk.Tk.__init__(self)

        self.title_font = tkfont.Font(family='Helvetica', size=14, weight='bold')
        self.title('Restaurant')

        # the container is where we'll stack frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.grid(row=0, column=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.employee_list = dbi.get_employees()
        self.user = None
        self.pin = None
        self.current_table = None

        self.frames = {}
        for frame_name in (StartPage, LogInPage, TableSelection, OrderPage):
            page_name = frame_name.__name__
            # give container to frames as parent and self as controller to grant ability to use variables from here
            frame = frame_name(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('StartPage')

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    """Default will be to start with this frame. Our employee list will be used to populated buttons that will be
    clicked to move that employee to the LogInPage where they will enter there PIN."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        label = tk.Label(self, text="Welcome", font=controller.title_font)
        label.grid(row=0, column=0)

        employee_window = tk.Frame(self)
        employee_window.grid(row=1, column=0)

        font = ("Helvetica", 20)

        num = 0
        # Stack buttons in rows of 4, stopping when reach end of employee list as determined by KeyError
        for row in range(4):
            for column in range(4):
                try:
                    tk.Button(employee_window, text=controller.employee_list[num][1],
                              command=lambda n=num: self.select_user(n),
                              width=10, height=5, bd=5, bg='SteelBlue1', activebackground='SteelBlue3', font=font)\
                        .grid(row=row, column=column, sticky='nsew')
                    num += 1
                except IndexError:
                    break

    def select_user(self, user):
        self.controller.user = self.controller.employee_list[user][0]
        self.controller.pin = self.controller.employee_list[user][2]
        self.controller.show_frame('LogInPage')


class LogInPage(tk.Frame):
    """Employees will enter their PIN here to complete log in process. If incorrect PIN is entered a popup will alert
    them to this. There will be a button at bottom of page allowing user's to return to previous page."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.current_password = ''
        label = tk.Label(self, text='Enter PIN', font=controller.title_font)
        label.grid(row=0, column=0)
        button_window = tk.Canvas(self)
        button_window.grid(row=1, column=0)
        font = ("Helvetica", 20)

        num = 1
        # Create buttons to be used for entering PIN
        for row in range(3):
            for column in range(3):
                tk.Button(button_window, text=num, command=lambda n=num: self.get_password(n),
                          width=10, height=5, bd=5, bg='SteelBlue1', font=font, activebackground='SteelBlue3')\
                    .grid(row=row, column=column, sticky='nsew')
                num += 1
        # Return to user selection page
        tk.Button(self, text="Return to Selection", command=lambda: controller.show_frame("StartPage"),
                  bd=5, font=font).grid(row=3, column=0)

    def get_password(self, number):
        """Stores numbers selected. When 4 total numbers have been entered compares that to the PIN for the
        current selected employee. If the PIN is correct frame to select table will be shown. If it is incorrect
        an error message will be displayed and user can try again."""
        self.current_password += str(number)

        if len(self.current_password) == 4:
            if int(self.current_password) == self.controller.pin:
                #  slightly faster to convert int to str for compare than vice versa
                self.controller.show_frame('TableSelection')
            else:
                messagebox.showinfo("Error", "Invalid PIN")
                self.current_password = ''


class TableSelection(tk.Frame):
    """After successfully logging in the user will select the table they wish to add an order for. After doing this
    they will be shown the frame where they can select guests and enter orders."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select Table", font=controller.title_font)
        label.grid(row=0, column=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.button_window = tk.Canvas(self)

        font = ("Helvetica", 20)

        num = 1
        per_row = 4
        # Create table buttons
        for row in range(per_row):
            for column in range(4):
                tk.Button(self.button_window, text=f'Table {num}', command=lambda n=num: self.set_table(n),
                          bd=5, bg='SteelBlue1', font=font, activebackground='SteelBlue3')\
                    .grid(row=row, column=column, sticky='nsew')
                num += 1

        self.button_window.grid(row=1, column=0)

    def set_table(self, table):
        """Sets table then switches to order entry frame"""
        self.controller.current_table = table
        self.controller.show_frame('OrderPage')


class OrderPage(tk.Frame):
    """Here user's will enter orders for currently selected table, by guest number. They will have the ability to remove
    most recently entered order until none remain if desired. Once submitted the order is sent to MySQL database
    and can user can no longer remove items here. They will be able to add more to same row based on Primary Key ID."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.guest = None
        appetizers = pd.read_csv('Menus/appetizers.csv')
        entrees = pd.read_csv('Menus/entrees.csv')
        drinks = pd.read_csv('Menus/drinkmenu.csv')
        font = ('Helvetica', 10)

        # Store current order here
        self.order = []
        self.food_order = []
        self.drink_order = []

        # Used for remove last:
        self.last_item_type = ''

        self.guest_select = tk.Canvas(self)
        self.guest_select.grid(row=0, column=0, sticky='nsew')

        self.keypad = tk.Canvas(self)
        self.keypad.grid(row=0, column=1, sticky='nsew')

        self.appetizer_window = tk.Canvas(self.keypad)
        self.appetizer_window.grid(row=0, column=0, sticky='nsew')

        self.entree_window = tk.Canvas(self.keypad)
        self.entree_window.grid(row=1, column=0, sticky='nsew', pady=15)

        self.drink_window = tk.Canvas(self.keypad)
        self.drink_window.grid(row=2, column=0, sticky='nsew', pady=15)

        self.action_window = tk.Canvas(self.keypad)
        self.action_window.grid(row=3, column=0, sticky='nsew', pady=15)

        self.display_window = tk.Canvas(self)
        self.display_window.grid(row=0, column=2, sticky='nsew')

        self.order_window = tk.Text(self.display_window)
        self.order_window.grid(row=1, column=0)

        self.price_window = tk.Text(self.display_window)
        self.price_window.grid(row=2, column=0)

        # Create 16 guest buttons
        num = 1
        for row in range(16):
            tk.Button(self.guest_select, text=f'Guest {num}', command=lambda n=num: self.set_guest(n),
                      bd=5, bg='goldenrod3', font=font, activebackground='goldenrod4')\
                .grid(row=row, column=0, sticky='nsew')
            num += 1

        # Create appetizer buttons from csv using IndexError to know when reach end
        num = 0
        for row in range(4):
            for column in range(4):
                try:
                    tk.Button(self.appetizer_window, text=f'{appetizers.iloc[num][0]}',
                              command=lambda n=num: self.add_to_order(
                                  'food', appetizers.iloc[n][0], appetizers.iloc[n][1], self.guest),
                              width=15, bd=5, bg='tomato3', font=font, activebackground='tomato4')\
                        .grid(row=row, column=column, sticky='nsew')
                    num += 1
                except IndexError:
                    break

        # Create entree buttons from csv using IndexError to know when reach end
        num = 0
        for row in range(10):
            for column in range(4):
                try:
                    tk.Button(self.entree_window, text=f'{entrees.iloc[num][0]}',
                              command=lambda n=num: self.add_to_order(
                                  'food', entrees.iloc[n][0], entrees.iloc[n][1], self.guest),
                              width=15, bd=5, bg='SteelBlue1', font=font, activebackground='SteelBlue3')\
                        .grid(row=row, column=column, sticky='nsew')
                    num += 1
                except IndexError:
                    break

        # Create drink buttons from csv using IndexError to know when reach end
        num = 0
        for row in range(10):
            for column in range(4):
                try:
                    tk.Button(self.drink_window, text=f'{drinks.iloc[num][0]}',
                              command=lambda n=num: self.add_to_order(
                                  'drink', drinks.iloc[n][0], drinks.iloc[n][1], self.guest),
                              width=15, bd=5, bg='yellow3', font=font, activebackground='yellow4')\
                        .grid(row=row, column=column, sticky='nsew')
                    num += 1
                except IndexError:
                    break

        tk.Button(self.action_window, text='Remove Last', command=self.remove_order, width=15, bd=5, bg='maroon3',
                  font=font, activebackground='maroon4').grid(row=0, column=0)
        tk.Button(self.action_window, text='Submit', command=self.submit, width=15, bd=5, bg='maroon3',
                  font=font, activebackground='maroon4').grid(row=0, column=2)

    def set_guest(self, guest):
        self.guest = guest

    def add_to_order(self, item_type, item, price, guest):
        if guest:
            self.order.append([item, price, guest])
            self.order_window.insert(
                'end', f'{item} ${price} {"Guest:".rjust(40-(len(item)+len(str(price)))," ")}{guest}\n')
            if item_type == 'food':
                self.food_order.append((item, float(price), self.guest))
                self.last_item_type = 'food'
            if item_type == 'drink':
                self.drink_order.append((item, float(price), self.guest))
                self.last_item_type = 'drink'
        else:
            popup('Please select a Guest')

    def remove_order(self):
        try:
            self.order.pop()
            if self.last_item_type == 'food':
                self.food_order.pop()
            if self.last_item_type == 'drink':
                self.drink_order.pop()
            self.order_window.delete(0.0, 'end')
            for item, price, guest in self.order:
                self.order_window.insert(
                    'end', f'{item} ${price} {"Guest:".rjust(40-(len(item)+len(str(price)))," ")}{guest}\n')
        except IndexError:
            # if we try to remove from empty list
            popup('Order is empty')

    def clear_order(self):
        self.order = []
        self.food_order = []
        self.drink_order = []
        self.order_window.delete('1.0', 'end')

    def submit(self):
        """Submit order to open order database. Orders are stored in list to make remove order much easier. In this
        function we will convert them to a dictionary with guests as keys and items with price tuples as values."""

        #  unique id for order_id
        uid = str(self.controller.user) + str(dt.datetime.now().strftime('%M%S'))  # need to make better

        # unpack order tuple and add uid to each entry
        food = [[order[0], order[1], order[2], int(uid)] for order in self.food_order]
        drinks = [[order[0], order[1], order[2], int(uid)] for order in self.drink_order]

        dbi.create_order(uid, self.controller.user, self.controller.current_table)
        dbi.create_food_order(food)
        dbi.create_drink_order(drinks)

        #  clear order variables and window
        self.clear_order()

        dbi.get_orders()


if __name__ == "__main__":
    app = App()
    app.mainloop()

