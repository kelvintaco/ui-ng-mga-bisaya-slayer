from tkinter import messagebox, Entry, Button, Toplevel
from tkinter import ttk

class AdminWindow:
    def __init__(self, master, main_window):
        self.master = master
        self.main_window = main_window
        self.create_widgets()

    def create_widgets(self):
        # Create the UI elements for the admin window
        self.login_button = Button(self.master, text='Login', command=self.login)
        self.login_button.pack()

        self.time_in_records_button = Button(self.master, text='Time In Records', command=self.show_time_in_records)
        self.time_in_records_button.pack()

        self.time_out_records_button = Button(self.master, text='Time Out Records', command=self.show_time_out_records)
        self.time_out_records_button.pack()

        self.leave_records_button = Button(self.master, text='Leave Records', command=self.show_leave_records)
        self.leave_records_button.pack()

        self.back_button = Button(self.master, text='Back', command=self.back)
        self.back_button.pack()

        self.close_button = Button(self.master, text='Close', command=self.close_window)
        self.close_button.pack()

    def login(self):
        messagebox.showinfo("Admin Login", "Admin login functionality")

    def show_time_in_records(self):
        messagebox.showinfo("Time In Records", "Show time in records functionality")

    def show_time_out_records(self):
        messagebox.showinfo("Time Out Records", "Show time out records functionality")

    def show_leave_records(self):
        messagebox.showinfo("Leave Records", "Show leave records functionality")

    def back(self):
        self.master.destroy()
        self.main_window.deiconify()

    def close_window(self):
        confirmed = messagebox.askyesno("Exit", "Are you sure you want to close the application?")
        if confirmed:
            self.master.destroy()
            self.main_window.destroy()
