import tkinter as tk
from tkinter import messagebox
import mysql.connector

def handle_confirmation():
    selected_value = radio_var.get()
    insert_data(selected_value)

def insert_data(value):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_empdb"
        )
        cursor = conn.cursor()

        query = "INSERT INTO tbl_leave (leave_type) VALUES (%s)"
        cursor.execute(query, (value,))
        conn.commit()

        messagebox.showinfo("Success", "Data inserted successfully!")

    except mysql.connector.Error as err:
        print("Error inserting data:", err)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

window = tk.Tk()

radio_var = tk.StringVar()

radio_button1 = tk.Radiobutton(window, text="Sick Leave", variable=radio_var, value="Sick Leave")
radio_button1.pack()

radio_button2 = tk.Radiobutton(window, text="Vacation Leave", variable=radio_var, value="Vacation Leave")
radio_button2.pack()

radio_button2 = tk.Radiobutton(window, text="Maternity Leave", variable=radio_var, value="Maternity Leave")
radio_button2.pack()

confirmation_button = tk.Button(window, text="Confirm", command=handle_confirmation)
confirmation_button.pack()

window.mainloop()
