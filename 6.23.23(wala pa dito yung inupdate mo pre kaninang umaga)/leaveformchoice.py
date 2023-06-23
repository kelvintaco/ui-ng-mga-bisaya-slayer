import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk

def handle_confirmation():
    empid = entryid.get()
    selected_value = radio_var.get()
    insert_data(empid, selected_value)

def insert_data(empid, value):
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
            query = "INSERT INTO tbl_leave (emp_id, leave_type) VALUES (%s, %s)"
            cursor.execute(query, (empid, value,))
            conn.commit()

            messagebox.showinfo("Success", "Data inserted successfully!")
        else:
            messagebox.showerror("Failed", "Employee ID not found!")
    except mysql.connector.Error as err:
        print("Error inserting data:", err)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

lftk = tk.Tk()
lftk.title('Leave Form')
lftk.geometry('600x400')

radio_var = tk.StringVar()

entryid = tk.Entry(lftk)
entryid.pack()

radio_button1 = ttk.Radiobutton(lftk, text="Sick Leave", variable=radio_var, value="Sick Leave")
radio_button1.pack()

radio_button2 = ttk.Radiobutton(lftk, text="Vacation Leave", variable=radio_var, value="Vacation Leave")
radio_button2.pack()

radio_button3 = ttk.Radiobutton(lftk, text="Maternity Leave", variable=radio_var, value="Maternity Leave")
radio_button3.pack()

confirmation_button = tk.Button(lftk, text="Confirm", command=handle_confirmation)
confirmation_button.pack()

lftk.mainloop()