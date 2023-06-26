import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import mysql.connector
import subprocess
import sys

def handle_confirmation():
    global empid
    empid = entryid.get()
    selected_value = radio_var.get()
    start_date = cal.selection_get().strftime('%Y-%m-%d')
    end_date = cal1.selection_get().strftime('%Y-%m-%d')
    insert_data(empid, selected_value, start_date, end_date)

def insert_data(empid, value, start_date, end_date):
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
            query0 = "SELECT emp_id FROM tbl_leave WHERE emp_id = %s AND start_date <= %s AND end_date >= %s"
            cursor.execute(query0, (empid, start_date, end_date))
            result1 = cursor.fetchone()
            if result1:
                messagebox.showerror("Leave Conflict", f"Employee is already on leave from {get_leave_start_date()} to. {get_leave_end_date()}")
            else:
                while cursor.nextset():
                    pass
                query = "INSERT INTO tbl_leave (emp_id, leave_type, start_date, end_date) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (empid, value, start_date, end_date))
                messagebox.showinfo("Success", "Inserted leave successfully!") 
                conn.commit()
                cursor.close()
        else:
            messagebox.showerror("Failed", "Employee ID not found!")
        
    except mysql.connector.Error as err:
        print("Error inserting data:", err)
    finally:
        if conn.is_connected():
            conn.close()

def get_leave_end_date():
    try:
        con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
        cursor = con.cursor()

        query = "SELECT end_date FROM tbl_leave WHERE emp_id = %s"
        cursor.execute(query, (empid,))
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
    

lftk = tk.Tk()
lftk.title('Leave Form')
lftk.geometry('600x600')

radio_var = tk.StringVar()

lab = tk.Label(lftk, text="Enter your employee no.")
lab.pack()

entryid = tk.Entry(lftk)
entryid.pack()

radio_button1 = ttk.Radiobutton(lftk, text="Sick Leave", variable=radio_var, value="Sick Leave")
radio_button1.pack()

radio_button2 = ttk.Radiobutton(lftk, text="Vacation Leave", variable=radio_var, value="Vacation Leave")
radio_button2.pack()

radio_button3 = ttk.Radiobutton(lftk, text="Maternity Leave", variable=radio_var, value="Maternity Leave")
radio_button3.pack()

tk.Label(lftk, text="Start Date").pack()
cal = Calendar(lftk, selectmode="day")
cal.pack()

tk.Label(lftk, text="End Date").pack()
cal1 = Calendar(lftk, selectmode="day")
cal1.pack()

confirmation_button = tk.Button(lftk, text="Confirm", command=handle_confirmation)
confirmation_button.pack()
def tawag():
    command = ['python', 'C:/Users/Booster/Documents/python/OOP_project/main.py']
    subprocess.run(command)

def goback():
    lftk.destroy()
    tawag()
    sys.exit()

backemp = tk.Button(lftk, text="Back", command=goback)
backemp.pack()
def close_window():
    confirmed = messagebox.askyesno("Exit", "Are you sure you want to close the application?")
    if confirmed:
        lftk.destroy()

lftk.protocol("WM_DELETE_WINDOW", close_window)
lftk.mainloop()
