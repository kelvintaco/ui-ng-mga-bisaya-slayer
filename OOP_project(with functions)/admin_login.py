import tkinter
from tkinter import messagebox, Entry, Button, Toplevel, Label
from tkinter import ttk
from admin_window import AdminWindow

class AdminLogin:
    
    def __init__(self, master, main_window):
        self.master = master
        self.main_window = main_window
        self.create_widgets()
        self.master.withdraw()
        self.main_window.withdraw()
        
    def create_widgets(self):
        global adlog_window
        adlog_window = tkinter.Tk()
        adlog_window.title("Admin Access")
        adlog_window.geometry("650x200")

        label = Label(adlog_window, text="Welcome Admin!", width=30, height=2)
        label.pack()
        label.config(font=('Times 25',25))

        tf = Entry(adlog_window, show="*")
        tf.pack()

        def ad_login():
            password = tf.get()

            if password == "admin123":
                adlog_window.destroy(), self.master.withdraw()
                ad_window = Toplevel(self.master)
                admin_login = AdminWindow(ad_window, self.master)
            else:
                messagebox.showerror("Failed", "Wrong password! Try again!")
                tf.delete(0, tkinter.END)

        btn = Button(adlog_window, text="Log In", command=ad_login)
        btn.pack()

        login_back = Button(adlog_window, text="Back", command=self.back)
        login_back.pack()

        self.exit_button = Button(adlog_window, text='Exit', command=self.close_window)
        self.exit_button.pack()

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=2)

    def back(self):
        adlog_window.destroy()
        self.master.destroy()
        self.main_window.deiconify()

    def close_window(self):
        confirmed = messagebox.askyesno("Exit", "Are you sure you want to close the application?")
        if confirmed:
            self.master.destroy()
            self.main_window.destroy()
    