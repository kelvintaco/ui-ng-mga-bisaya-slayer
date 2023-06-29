import tkinter as tk
import customtkinter
from customtkinter import CTkButton, CTkLabel, CTkFont,CTkEntry,CTkToplevel,CTkRadioButton
from tkinter import messagebox
from tkcalendar import Calendar
import mysql.connector
from datetime import datetime
import sys


class LeaveForm:
    def __init__(self, master,):
        self.master = master
        #self.main_window = main_window
        self.create_widgets()

    def create_widgets(self):
        self.master = CTkToplevel()
        self.master.grab_set()
        self.master.title('Leave Form')
        self.master.geometry('430x530')
        self.master.resizable(False, False)
        self.radio_var = tk.StringVar()

        lab = CTkLabel(self.master, text="Enter your Employee ID", width=30, height=2)
        lab.grid(row=0, column=0, columnspan=13, sticky='nsew', padx=10, pady=10)
        lab.configure(font=('Times', 25))

        self.entryid = CTkEntry(self.master,placeholder_text="Input ID")
        self.entryid.grid(row=1, column=0, columnspan=13, sticky='nsew', padx=10, pady=10)

        radio_button1 = CTkRadioButton(self.master, text="Sick Leave", variable=self.radio_var, value="Sick Leave")
        radio_button1.grid(row=2, column=4, columnspan=5, sticky='nsew', padx=10, pady=10)

        radio_button2 = CTkRadioButton(self.master, text="Vacation Leave", variable=self.radio_var, value="Vacation Leave")
        radio_button2.grid(row=3, column=4, columnspan=5, sticky='nsew', padx=10, pady=10)

        radio_button3 = CTkRadioButton(self.master, text="Maternity Leave", variable=self.radio_var, value="Maternity Leave")
        radio_button3.grid(row=4, column=4, columnspan=5, sticky='nsew', padx=10, pady=10)

        CTkLabel(self.master, text="Start Date").grid(row=5, column=0, columnspan=6, sticky='nsew', padx=10, pady=10)
        self.cal = Calendar(self.master, selectmode="day")
        self.cal.grid(row=6, column=0, columnspan=6, sticky='nsew', padx=10, pady=10)

        CTkLabel(self.master, text="End Date").grid(row=5, column=6, columnspan=6, sticky='nsew', padx=10, pady=10)
        self.cal1 = Calendar(self.master, selectmode="day")
        self.cal1.grid(row=6, column=6, columnspan=6, sticky='nsew', padx=10, pady=10)

        confirmation_button = CTkButton(self.master, text="Confirm", command=self.handle_confirmation)
        confirmation_button.grid(row=9, column=0, columnspan=13, sticky='nsew', padx=10, pady=10)

        backemp = CTkButton(self.master, text="Back", command=self.back)
        backemp.grid(row=10, column=0, columnspan=13, sticky='nsew', padx=10)

        self.master.protocol("WM_DELETE_WINDOW", self.close_window)
        self.master.mainloop()

        for i in range(11):
            self.master.rowconfigure(i, weight=1)

        for i in range(13):
            self.master.columnconfigure(i, weight=1)



    def handle_confirmation(self):
        global empid,current_date
        empid = self.entryid.get()
        selected_value = self.radio_var.get()
        start_date = self.cal.selection_get().strftime('%Y-%m-%d')
        end_date = self.cal1.selection_get().strftime('%Y-%m-%d')
        current_date = datetime.today().strftime("%Y-%m-%d")

        self.insert_data(empid, selected_value, start_date, end_date)

    def insert_data(self, empid, value, start_date, end_date):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="db_empdb"
            )
            cursor = conn.cursor()
    
            queryv = "SELECT emp_id FROM tbl_employee WHERE emp_id = %s"
            cursor.execute(queryv, (empid,))
            result = cursor.fetchone()
            if result:
                if self.radio_var.get() == "":
                    messagebox.showerror("Failed", "Please select a leave type")
                else:
                    confirm = messagebox.askyesno("Confirmation", f"Are you sure your employee ID is: {empid}?")
                    if confirm:
                        if end_date < start_date:
                            messagebox.showerror("Invalid Dates", "The leave end date cannot be earlier than the start date.")
                            self.entryid.delete(0, tk.END)
                        else:
                            if start_date and end_date >= current_date:
                                while cursor.nextset():
                                    pass
                                query0 = "SELECT emp_id FROM tbl_leave WHERE emp_id = %s AND start_date <= %s AND end_date >= %s"
                                cursor.execute(query0, (empid, start_date, end_date))
                                result1 = cursor.fetchone()
                                if result1:
                                    messagebox.showerror("Leave Conflict", f"Employee is already on leave from {self.get_leave_start_date()} to {self.get_leave_end_date()}")
                                    self.entryid.delete(0, tk.END)
                                else:
                                    query1 = "SELECT emp_id FROM tbl_leave WHERE emp_id = %s AND end_date >= %s"
                                    cursor.execute(query1, (empid, start_date))
                                    result2 = cursor.fetchone()
    
                                    while cursor.nextset():
                                            pass
                                    if result2:
                                        messagebox.showerror("Leave Conflict", f"Employee is already on leave beyond the requested start date.")
                                        self.entryid.delete(0, tk.END)
                                    else:
                                        
                                        query = "INSERT INTO tbl_leave (emp_id, leave_type, start_date, end_date) VALUES (%s, %s, %s, %s)"
                                        cursor.execute(query, (empid, value, start_date, end_date))
                                        messagebox.showinfo("Success", "Inserted leave successfully!") 
                                        conn.commit()
                                        cursor.close()
                                        self.entryid.delete(0, tk.END)
                            else:
                                messagebox.showerror("Failed", "Date already passed, Please input valid date")
                                self.entryid.delete(0, tk.END)
                    else:
                        cursor.close()
                        self.entryid.delete(0, tk.END)
                        
            else:
                messagebox.showerror("Failed", "Employee ID not found!")
                self.entryid.delete(0, tk.END)
            
        except mysql.connector.Error as err:
            print("Error inserting data:", err)
        finally:
            if conn.is_connected():
                conn.close()

    def get_leave_start_date(self):
        empid = self.entryid.get()
        try:
            con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
            cursor = con.cursor()

            query = "SELECT start_date FROM tbl_leave WHERE emp_id = %s"
            cursor.execute(query, (empid,))
            result = cursor.fetchone()
            if result:
                start_date = result[0]
                return start_date
            else:
                return None

        except mysql.connector.Error as err:
            print("Error: {}".format(err))

        finally:
            if con.is_connected():
                cursor.close()
                con.close()

    def back(self):
        self.master.destroy()

    def close_window(self):
        confirmed = messagebox.askyesno("Exit", "Are you sure you want to close the application?")
        if confirmed:
            self.master.destroy()
            sys.exit()


