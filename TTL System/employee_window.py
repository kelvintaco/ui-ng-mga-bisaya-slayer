import tkinter
from tkinter import messagebox, Entry, Button, Toplevel, Label
from customtkinter import CTkButton, CTkLabel, CTkFont,CTkEntry,CTkToplevel
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from leaveform import LeaveForm
 
class EmployeeWindow:
    
    def __init__(self, master, main_window):
        self.master = master
        self.main_window = main_window
        self.create_widgets()
        self.main_window.withdraw()
        
 
    def create_widgets(self):
        # Create the UI elements for the employee window
        global empEntry
        self.master.title("Employee Window")
        self.master.geometry("450x200")
        self.master.resizable(False, False)

        employeeID = CTkLabel(self.master, text = 'Employee ID',width=30, height=2)
        employeeID.grid(row=0,column=0,columnspan=7,sticky="nsew")
        employeeID.configure(font=('Times', 25))
 
        empEntry = CTkEntry(self.master,placeholder_text="Input ID")
        empEntry.grid(row=2,column=1,columnspan=5,sticky="nsew")
        
        self.time_in_button = CTkButton(self.master, text='Time In', command=self.time_in)
        self.time_in_button.grid(row=4,column=1,columnspan=2,sticky="nsew")
        
        self.time_out_button = CTkButton(self.master, text='Time Out', command=self.time_out)
        self.time_out_button.grid(row=4,column=4,columnspan=2,sticky="nsew")
 
        self.leave_form_button = CTkButton(self.master, text='Leave Form', command=self.leave_form)
        self.leave_form_button.grid(row=6,column=1,columnspan=5,sticky="nsew")
 
        self.back_button = CTkButton(self.master, text='Back', command=self.back)
        self.back_button.grid(row=8,column=1,columnspan=2,sticky="nsew")
 
        self.exit_button = CTkButton(self.master, text='Exit', command=self.close_window)
        self.exit_button.grid(row=8,column=4,columnspan=2,sticky="nsew")

        self.master.protocol("WM_DELETE_WINDOW", self.close_window)
 
        self.master.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        self.master.columnconfigure((1,2,3,4,5), weight=1)
        self.master.columnconfigure((0,6), weight=1)
        
 
    def time_in(self):
        global empid_value
        empid_value = empEntry.get()
        current_time = datetime.now()
        current_day = datetime.today()
 
        def get_leave_end_date():
            try:
                con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
                cursor = con.cursor()
 
                query = "SELECT end_date FROM tbl_leave WHERE emp_id = %s"
                cursor.execute(query, (empid_value,))
                result = cursor.fetchone()
                if result:
                    end_date = result[0]
                    return end_date
                else:
                    return None
 
            except mysql.connector.Error as err:
                print("Error: {}".format(err))
 
            finally:
                if con.is_connected():
                    cursor.close()
                    con.close()
 
        def get_leave_start_date():
            try:
                con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
                cursor = con.cursor()
 
                query = "SELECT start_date FROM tbl_leave WHERE emp_id = %s"
                cursor.execute(query, (empid_value,))
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
 
        try:
            con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
            cursor = con.cursor()
 
            query = "SELECT emp_id FROM tbl_employee WHERE emp_id = %s"
            cursor.execute(query, (empid_value,))
            result = cursor.fetchone()
            if result:
                confirm = messagebox.askyesno("Confirmation", f"Are you sure your employee ID is: {empid_value}?")
                if confirm:
                    query = "SELECT emp_id FROM tbl_leave WHERE emp_id = %s AND start_date <= %s AND end_date >= %s"
                    cursor.execute(query, (empid_value, current_time, current_day))
                    result = cursor.fetchone()
                    if result:
                        messagebox.showerror("Leave Conflict", f"Employee is already on leave from {get_leave_start_date()} to {get_leave_end_date()}")
                        empEntry.delete(0, tkinter.END)
                    else:
                        query = 'SELECT emp_id, date_of_time_in FROM tbl_timein WHERE emp_id = %s AND DATE(date_of_time_in) = DATE(NOW());'
                        cursor.execute(query, (empid_value,))
                        resulty = cursor.fetchall()
                        if resulty:
                            messagebox.showerror("Failed", "You have already timed in today!")
                            empEntry.delete(0, tkinter.END)
                        else:
                            query = "INSERT INTO tbl_timein(emp_id, time_of_time_in, date_of_time_in) VALUES (%s, %s, %s)"
                            cursor.execute(query, (empid_value, current_time, current_day,))
                            con.commit()
                            messagebox.showinfo("Success", "Timed in successfully!")
                            empEntry.delete(0, tkinter.END)
                else:
                    cursor.close()
                    empEntry.delete(0, tkinter.END)
            else:
                messagebox.showerror("Failed", "Employee ID not found!")
                empEntry.delete(0, tkinter.END)
 
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
                confirm = messagebox.askyesno("Confirmation", f"Are you sure your employee ID is: {empid_value}?")
                if confirm:
                    query = 'SELECT emp_id, date_of_time_out FROM tbl_timeout WHERE emp_id = %s AND DATE(date_of_time_out) = DATE(NOW());'
                    cursor.execute(query, (empid_value,))
                    resulty = cursor.fetchall()
                    if resulty:
                        messagebox.showerror("Failed", "You have already timed out today!")
                        empEntry.delete(0, tkinter.END)
                    else:
                        query = 'SELECT emp_id, date_of_time_in FROM tbl_timein WHERE emp_id = %s AND DATE(date_of_time_in) = DATE(NOW());'
                        cursor.execute(query, (empid_value,))
                        resultyz = cursor.fetchone()
                        if resultyz:
                            query = "INSERT INTO tbl_timeout(emp_id, time_of_time_out, date_of_time_out) VALUES (%s, %s, %s)"
                            cursor.execute(query, (empid_value, current_time, current_day,))
                            con.commit()
                            messagebox.showinfo("Success", "Timed out successfully!")
                            empEntry.delete(0, tkinter.END)
                        else:
                            messagebox.showerror("Failed", "You have not yet timed in today!")
                            empEntry.delete(0, tkinter.END)
                else:
                    cursor.close()
                    empEntry.delete(0, tkinter.END)
            else:
                messagebox.showerror("Failed", "Employee ID not found!")
                empEntry.delete(0, tkinter.END)
 
        except Error as err:
           print("Failed", "Error: {}".format(err))
        finally:
                if con.is_connected():
                    con.close()
                    print("Connection Closed.")

    def leave_form(self):
        LeaveForm(self.master)
        
        
    def back(self):
        self.master.destroy()
        self.main_window.deiconify()

    def close_window(self):
        confirmed = messagebox.askyesno("Exit", "Are you sure you want to close the application?")
        if confirmed:
            self.master.destroy()
            self.main_window.destroy()
