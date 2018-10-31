import tkinter as tk
from tkinter import messagebox, font as tkfont
import pandas as pd


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.grid(row=0, column=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.employee_list = pd.read_csv('employees')
        self.current_user = ''

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

    # def select_user(self, user):
    #     global user_id
    #     user_id = user
    #     self.show_frame('LogInPage')
    #
    # def get_password(self, pin):
    #     global current_password
    #     current_password += pin
    #     if len(current_password) == 4:
    #         if self.employee_list['password'][user_id] == int(current_password):
    #             self.show_frame("StopWatch")
    #             current_password = ''
    #         else:
    #             messagebox.showinfo("Error", "Invalid PIN")
    #             current_password = ''


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Log in Page", font=controller.title_font)
        label.grid(row=0, column=0)

        employee_window = tk.Frame(self)
        employee_window.grid(row=1, column=0)

        row_count, column_count = 0, 0
        for employee in controller.employee_list['name']:
            tk.Button(employee_window, text=employee, command=lambda: self.select_user(employee))\
                .grid(row=row_count, column=column_count)

    def select_user(self, controller, user):
        controller.current_user = user
        controller.show_frame('LogInPage')

        # button1 = tk.Button(employee_window, text=employee_list['name'][0],
        #                     command=lambda: controller.select_user(0))
        # button1.grid(row=0, column=0)
        # button2 = tk.Button(employee_window, text=employee_list['name'][1],
        #                     command=lambda: controller.select_user(1))
        # button2.grid(row=0, column=1)
        # tk.Button(employee_window, text='Employee 2').grid(row=0, column=1)
        # tk.Button(employee_window, text='Employee 3').grid(row=1, column=0)
        # tk.Button(employee_window, text='Employee 4').grid(row=1, column=1)
        #
        # button1 = tk.Button(self, text="Log in",
        #                     command=lambda: controller.show_frame("LogInPage"))
        # button1.grid(row=2, column=0)


class LogInPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='Enter PIN', font=controller.title_font)
        label.grid(row=0, column=0)
        button_window = tk.Canvas(self)
        button_window.grid(row=1, column=0)
        button1 = tk.Button(button_window, text='1', command=lambda: controller.get_password('1'))
        button1.grid(row=1, column=0, sticky='nsew')
        button2 = tk.Button(button_window, text='2', command=lambda: controller.get_password('2'))
        button2.grid(row=1, column=1, sticky='nsew')
        button3 = tk.Button(button_window, text='3', command=lambda: controller.get_password('3'))
        button3.grid(row=1, column=2, sticky='nsew')
        button4 = tk.Button(button_window, text='4', command=lambda: controller.get_password('4'))
        button4.grid(row=2, column=1, sticky='nsew')
        button5 = tk.Button(button_window, text='1', command=lambda: controller.get_password('5'))
        button5.grid(row=2, column=1, sticky='nsew')
        button6 = tk.Button(button_window, text='2', command=lambda: controller.get_password('6'))
        button6.grid(row=2, column=2, sticky='nsew')
        button7 = tk.Button(button_window, text='3', command=lambda: controller.get_password('7'))
        button7.grid(row=3, column=0, sticky='nsew')
        button8 = tk.Button(button_window, text='4', command=lambda: controller.get_password('8'))
        button8.grid(row=3, column=1, sticky='nsew')
        button9 = tk.Button(button_window, text='4', command=lambda: controller.get_password('9'))
        button9.grid(row=3, column=2, sticky='nsew')

        button = tk.Button(self, text="Return to Selection",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=3, column=0)


class OrderPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


if __name__ == "__main__":
    app = App()
    app.mainloop()
