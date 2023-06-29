import tkinter
import customtkinter
from tkinter import messagebox, Entry, Button, Toplevel,Label,Tk
from customtkinter import CTkButton, CTkLabel, CTkFont,CTkEntry,CTkToplevel
from employee_window import EmployeeWindow
from admin_window import AdminWindow

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Create the UI elements for the main window
        self.welcomeLabel = CTkLabel(self.master, text='WELCOME', font=CTkFont(size=35, weight="bold"), width=30, height=2)
        self.welcomeLabel.grid(row=0, column=1, columnspan=3, sticky='nsew')

        self.employee_button = CTkButton(self.master, text='Admin Window', command=self.admin_window)
        self.employee_button.grid(row=1, column=1, sticky='nsew')

        self.admin_button = CTkButton(self.master, text='Employee Window', command=self.employee_window)
        self.admin_button.grid(row=1, column=3, sticky='nsew')

        self.master.columnconfigure((1, 3), weight=7)
        self.master.columnconfigure((0, 4), weight=3)
        self.master.columnconfigure(2, weight=1)
        self.master.rowconfigure((0, 1), weight=1)
        self.master.rowconfigure(2, weight=1)

        def close_window():
            confirmed = messagebox.askyesno("Exit", "Are you sure you want to close the application?")
            if confirmed:
                self.master.destroy()
                

        self.master.protocol("WM_DELETE_WINDOW", close_window)

    def employee_window(self):
        self.master.withdraw()
        emp_window = CTkToplevel(self.master)
        emp_window.protocol("WM_DELETE_WINDOW", self.close_window)
        employee_window = EmployeeWindow(emp_window, self.master)


    def admin_window(self):
        def admin_login():
            adlog_window = CTkToplevel(self.master)
            adlog_window.title("Admin Access")
            adlog_window.geometry("400x200")
            adlog_window.resizable(False, False)

            label = CTkLabel(adlog_window, text="Welcome Admin!", width=30, height=2)
            label.grid(row=0, column=1, columnspan=5, sticky="nsew")
            label.configure(font=('Times', 25))

            tf = CTkEntry(adlog_window, show="*",placeholder_text="Input Password")
            tf.grid(row=2, column=1, columnspan=5, sticky="nsew")

            def close_admin_login():
                adlog_window.destroy()
                self.master.deiconify()

            def ad_login():
                password = tf.get()

                if password == "admin123":
                    adlog_window.destroy()
                    self.master.withdraw()
                    ad_window = CTkToplevel(self.master)
                    AdminWindow(ad_window, self.master)
                else:
                    messagebox.showerror("Failed", "Wrong password! Try again!")
                    tf.delete(0, tkinter.END)

            btn = CTkButton(adlog_window, text="Log In", command=ad_login)
            btn.grid(row=4, column=1, columnspan=5, sticky="nsew")

            login_back = CTkButton(adlog_window, text="Back", command=close_admin_login)
            login_back.grid(row=6, column=1,columnspan=2, sticky="nsew")

            exit_button = CTkButton(adlog_window, text='Exit', command=self.close_window)
            exit_button.grid(row=6, column=4,columnspan=2, sticky="nsew")

            adlog_window.protocol("WM_DELETE_WINDOW", self.close_window)

            adlog_window.rowconfigure((0,1,2,3,4,5,6,7), weight=1)
            adlog_window.columnconfigure((0,6), weight=2)
            adlog_window.columnconfigure((1,2,3,4,5), weight=1)
            
        self.master.withdraw()  # Hide the main window
        admin_login()

    def close_window(self):
        confirmed = messagebox.askyesno("Exit", "Are you sure you want to close the application?")
        if confirmed:
            self.master.destroy()

    


