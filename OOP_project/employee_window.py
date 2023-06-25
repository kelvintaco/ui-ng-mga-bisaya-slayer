from tkinter import messagebox, Entry, Button, Toplevel
from datetime import datetime

class EmployeeWindow:
    def __init__(self, master, main_window):
        self.master = master
        self.main_window = main_window
        self.create_widgets()

    def create_widgets(self):
        # Create the UI elements for the employee window
        self.time_in_button = Button(self.master, text='Time In', command=self.time_in)
        self.time_in_button.pack()

        self.time_out_button = Button(self.master, text='Time Out', command=self.time_out)
        self.time_out_button.pack()

        self.leave_form_button = Button(self.master, text='Leave Form', command=self.leave_form)
        self.leave_form_button.pack()

        self.back_button = Button(self.master, text='Back', command=self.back)
        self.back_button.pack()

        self.close_button = Button(self.master, text='Close', command=self.close_window)
        self.close_button.pack()

        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)
        self.master.rowconfigure(3, weight=1)
        self.master.rowconfigure(4, weight=1)
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)

    def time_in(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        messagebox.showinfo("Time In", f"Time In recorded: {current_time}")

    def time_out(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        messagebox.showinfo("Time Out", f"Time Out recorded: {current_time}")

    def leave_form(self):
        messagebox.showinfo("Leave Form", "Leave form functionality")

    def back(self):
        self.master.destroy()
        self.main_window.deiconify()

    def close_window(self):
        confirmed = messagebox.askyesno("Exit", "Are you sure you want to close the application?")
        if confirmed:
            self.master.destroy()
            self.main_window.destroy()
