import tkinter
from tkinter import messagebox, Entry, Button, Toplevel, Label
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import subprocess
import sys

class EmployeeWindow:
    
    def __init__(self, master, main_window):
        self.master = master
        self.main_window = main_window
        self.create_widgets()
        self.main_window.withdraw()
        

    def create_widgets(self):
        # Create the UI elements for the employee window
        global empEntry

        employeeID = Label(self.master, text = 'Employee ID')
        employeeID.pack()

        empEntry = Entry(self.master)
        empEntry.pack()
        
        self.time_in_button = Button(self.master, text='Time In', command=self.time_in)
        self.time_in_button.pack()
        
        self.time_out_button = Button(self.master, text='Time Out', command=self.time_out)
        self.time_out_button.pack()

        self.leave_form_button = Button(self.master, text='Leave Form', command=self.leave_form)
        self.leave_form_button.pack()

        self.back_button = Button(self.master, text='Back', command=self.back)
        self.back_button.pack()

        self.exit_button = Button(self.master, text='Exit', command=self.close_window)
        self.exit_button.pack()

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
        empid_value = empEntry.get()
        current_time = datetime.now()
        current_day = datetime.today()
        try:
            con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
            cursor = con.cursor()

            query = "SELECT emp_id FROM tbl_employee WHERE emp_id = %s"
            cursor.execute(query, (empid_value,))
            result = cursor.fetchone()
            if result:
                query = "SELECT emp_id FROM tbl_leave WHERE emp_id = %s AND start_date <= %s AND end_date >= %s"
                cursor.execute(query, (empid_value, current_time, current_day))
                result = cursor.fetchone()
                if result:
                    messagebox.showerror("Leave Conflict", "Employee is already on leave")
                else:
                    query = 'SELECT emp_id, date_of_time_in FROM tbl_timein WHERE emp_id = %s AND DATE(date_of_time_in) = DATE(NOW());'
                    cursor.execute(query, (empid_value,))
                    resulty = cursor.fetchall()
                    if resulty:
                        messagebox.showerror("Failed", "You have already timed in today!")
                    else:
                        query = "INSERT INTO tbl_timein(emp_id, time_of_time_in, date_of_time_in) VALUES (%s, %s, %s)"
                        cursor.execute(query, (empid_value, current_time, current_day,))
                        con.commit()
                        messagebox.showinfo("Success", "Timed in successfully!")
            else:
                messagebox.showerror("Failed", "Employee ID not found!")

        except Error as err:
            print("Failed", "Error: {}".format(err))
        finally:
            if con.is_connected():
                con.close()
                print("Connection Closed.")


    def time_out(self):
        empid_value = empEntry.get()
        current_time = datetime.now()
        current_day = datetime.today()
        try:
            con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
            cursor = con.cursor()
            #pang verify
            query = "SELECT emp_id FROM tbl_employee WHERE emp_id = %s"
            cursor.execute(query, (empid_value,))
            result = cursor.fetchone()
            if result:
                query = 'SELECT emp_id, date_of_time_out FROM tbl_timeout WHERE emp_id = %s AND DATE(date_of_time_out) = DATE(NOW());'
                cursor.execute(query, (empid_value,))
                resulty = cursor.fetchall()
                if resulty:
                    messagebox.showerror("Failed", "You have already timed out today!")
                else:
                    query = 'SELECT emp_id, date_of_time_in FROM tbl_timein WHERE emp_id = %s AND DATE(date_of_time_in) = DATE(NOW());'
                    cursor.execute(query, (empid_value,))
                    resultyz = cursor.fetchone()
                    if resultyz:
                        query = "INSERT INTO tbl_timeout(emp_id, time_of_time_out, date_of_time_out) VALUES (%s, %s, %s)"
                        cursor.execute(query, (empid_value, current_time, current_day,))
                        con.commit()
                        messagebox.showinfo("Success", "Timed out successfully!")
                    else:
                        messagebox.showerror("Failed", "You have not yet timed in today!")
            else:
                messagebox.showerror("Failed", "Employee ID not found!")

        except Error as err:
           print("Failed", "Error: {}".format(err))
        finally:
                if con.is_connected():
                    con.close()
                    print("Connection Closed.")

    def leave_form(self):
        self.master.destroy()
        self.main_window.destroy()
        command = ['python', 'C:/Users/Booster/Documents/python/OOP_project/leaveform.py']

        subprocess.run(command)
        sys.exit()    

    def back(self):
        self.master.destroy()
        self.main_window.deiconify()

    def close_window(self):
        confirmed = messagebox.askyesno("Exit", "Are you sure you want to close the application?")
        if confirmed:
            self.master.destroy()
            self.main_window.destroy()
