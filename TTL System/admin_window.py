from tkinter import messagebox, Entry, Button, Toplevel, Label
from customtkinter import CTkButton, CTkLabel, CTkFont,CTkEntry,CTkToplevel,CTkRadioButton
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
import tkinter
 
class AdminWindow:
    def __init__(self, master,main_window):
        self.master = master
        self.main_window = main_window
        self.create_widgets()
 
    def create_widgets(self):
        self.master.title("Admin Window")
        self.master.geometry("500x300")
        self.master.resizable(False, False)
        global adwin_entry
 
        self.label1 = CTkLabel(self.master, text="Search Employee ID:", width=30, height=2)
        self.label1.grid(row=0, column=0, columnspan=7, sticky="nsew")
        self.label1.configure(font=('Times', 25))
 
        adwin_entry = CTkEntry(self.master, placeholder_text="Input ID")
        adwin_entry.grid(row=2, column=1, columnspan=5, sticky="nsew")
 
        self.time_in_records_button = CTkButton(self.master, text='Time In Records', command=self.show_time_in_records)
        self.time_in_records_button.grid(row=4, column=1, columnspan=2, sticky="nsew")
 
        self.time_out_records_button = CTkButton(self.master, text='Time Out Records', command=self.show_time_out_records)
        self.time_out_records_button.grid(row=4, column=4, columnspan=2, sticky="nsew")
 
        self.leave_records_button = CTkButton(self.master, text='Leave Records', command=self.show_leave_records)
        self.leave_records_button.grid(row=6, column=1, columnspan=5, sticky="nsew")
 
        self.button_create = CTkButton(self.master, text="Insert New Employee", command=self.create_employee)
        self.button_create.grid(row=10, column=1, columnspan=2, sticky="nsew")
 
        self.button_view = CTkButton(self.master, text="View All Employees", command=self.showemployees)
        self.button_view.grid(row=8, column=1, columnspan=5, sticky="nsew")
 
        self.del_b = CTkButton(self.master, text="Delete Employee", command=self.bura_emp)
        self.del_b.grid(row=10, column=4, columnspan=2, sticky="nsew")
 
        def back():
            self.master.destroy()
            self.main_window.deiconify()
 
 
        self.back_button = CTkButton(self.master, text='Back', command=back)
        self.back_button.grid(row=12, column=1, columnspan=2, sticky="nsew")
 
        def close_window():
            confirmed = messagebox.askyesno("Exit", "Are you sure you want to close the application?")
            if confirmed:
                self.master.destroy()
                self.main_window.destroy()
 
        self.close_button = CTkButton(self.master, text='Close', command=close_window)
        self.close_button.grid(row=12, column=4, columnspan=2, sticky="nsew")
 
 
        self.master.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight=1)
        self.master.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
 
        self.master.protocol("WM_DELETE_WINDOW", close_window)
 
 
    def show_time_in_records(self):
        try:
            con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
 
            cursor = con.cursor()
 
            queryv = "SELECT emp_id FROM tbl_employee WHERE emp_id = %s"
            cursor.execute(queryv, (adwin_entry.get(),))
            result = cursor.fetchone()
            if result:
                queryv = "SELECT emp_id FROM tbl_timein WHERE emp_id = %s"
                cursor.execute(queryv, (adwin_entry.get(),))
                result = cursor.fetchone()
                if result:
                    while cursor.nextset():
                        pass
                    timerec = CTkToplevel()
                    timerec.title("Time in Records")
                    timerec.geometry("1000x200")
                    timerec.grab_set()
                    tree=ttk.Treeview(timerec)
 
                    query = """SELECT e.emp_id, e.first_name, e.last_name, t.time_of_time_in, t.date_of_time_in
                    FROM tbl_employee e
                    RIGHT JOIN tbl_timein t
                    ON e.emp_id=t.emp_id WHERE e.emp_id = %s"""
                    cursor.execute(query, (adwin_entry.get(),))
                    rows=cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    tree["columns"] = columns
                    tree.heading("#0", text="Index")
                    for col in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=100, anchor="center")
                    for i, row in enumerate(rows):
                        tree.insert("", "end", text=str(i), values=row)
                    tree.grid(row=0, column=0, sticky="nsew")
 
                    scrollbar = ttk.Scrollbar(timerec, orient="vertical", command=tree.yview)
                    scrollbar.grid(row=0, column=1, sticky="ns")
 
                    tree.configure(yscrollcommand=scrollbar.set)
 
                    timerec.grid_rowconfigure(0, weight=1)
                    timerec.grid_columnconfigure(0, weight=1)
                    con.commit()
                    cursor.close() 
                else:
                    messagebox.showerror("Failed", f"No records found for employee ID no.: {adwin_entry.get()}")
                    adwin_entry.delete(0, tkinter.END)
            else:
                cursor.close()
                messagebox.showerror("Failed", "Employee ID not found!")
                adwin_entry.delete(0, tkinter.END)
 
        except Error as err:
            print("Access Failed! {}".format(err))
        finally:
            if con.is_connected():
                con.close()
                print("Connection Successful!")
 
    def show_time_out_records(self):
        try:
            con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
 
            cursor = con.cursor()
 
            queryv = "SELECT emp_id FROM tbl_employee WHERE emp_id = %s"
            cursor.execute(queryv, (adwin_entry.get(),))
            result = cursor.fetchone()
            if result:
                queryv = "SELECT emp_id FROM tbl_timeout WHERE emp_id = %s"
                cursor.execute(queryv, (adwin_entry.get(),))
                result = cursor.fetchone()
                if result:
                    while cursor.nextset():
                        pass
                    timerec = CTkToplevel()
                    timerec.title("Time out Records")
                    timerec.geometry("1000x200")
                    timerec.grab_set()
                    tree=ttk.Treeview(timerec)
 
                    query = """SELECT e.emp_id, e.first_name, e.last_name, t.time_of_time_out, t.date_of_time_out
                    FROM tbl_employee e
                    RIGHT JOIN tbl_timeout t
                    ON e.emp_id=t.emp_id WHERE e.emp_id = %s"""
                    cursor.execute(query, (adwin_entry.get(),))
                    rows=cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    tree["columns"] = columns
                    tree.heading("#0", text="Index")
                    for col in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=100, anchor="center")
                    for i, row in enumerate(rows):
                        tree.insert("", "end", text=str(i), values=row)
                    tree.grid(row=0, column=0, sticky="nsew")
 
                    scrollbar = ttk.Scrollbar(timerec, orient="vertical", command=tree.yview)
                    scrollbar.grid(row=0, column=1, sticky="ns")
 
                    tree.configure(yscrollcommand=scrollbar.set)
 
                    timerec.grid_rowconfigure(0, weight=1)
                    timerec.grid_columnconfigure(0, weight=1)
                    con.commit()
                    cursor.close() 
                else:
                    messagebox.showerror("Failed", f"No records found for employee ID no.: {adwin_entry.get()}")
                    adwin_entry.delete(0, tkinter.END)
            else:
                cursor.close()
                messagebox.showerror("Failed", "Employee ID not found!")
                adwin_entry.delete(0, tkinter.END)
 
        except Error as err:
            print("Access Failed! {}".format(err))
        finally:
            if con.is_connected():
                con.close()
                print("Connection Successful!")
 
    def show_leave_records(self):
        try:
            con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
 
            cursor = con.cursor()
 
            queryv = "SELECT emp_id FROM tbl_employee WHERE emp_id = %s"
            cursor.execute(queryv, (adwin_entry.get(),))
            result = cursor.fetchone()
            while cursor.nextset():
                         pass
            if result:
                queryv = "SELECT emp_id FROM tbl_leave WHERE emp_id = %s"
                cursor.execute(queryv, (adwin_entry.get(),))
                result = cursor.fetchone()
                if result:
                    while cursor.nextset():
                         pass
                    timerec = CTkToplevel()
                    timerec.title("Leave Records")
                    timerec.geometry("1000x200")
                    timerec.grab_set()
                    tree=ttk.Treeview(timerec)
 
                    query = """SELECT e.emp_id, e.first_name, e.last_name, t.leave_type, t.start_date, t.end_date
                    FROM tbl_employee e
                    RIGHT JOIN tbl_leave t
                    ON e.emp_id=t.emp_id WHERE e.emp_id = %s
                    ORDER BY emp_id ASC;"""
                    cursor.execute(query, (adwin_entry.get(),))
                    rows=cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    tree["columns"] = columns
                    tree.heading("#0", text="Index")
                    for col in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=100, anchor="center")
                    for i, row in enumerate(rows):
                        tree.insert("", "end", text=str(i), values=row)
                    tree.grid(row=0, column=0, sticky="nsew")
 
                    scrollbar = ttk.Scrollbar(timerec, orient="vertical", command=tree.yview)
                    scrollbar.grid(row=0, column=1, sticky="ns")
 
                    tree.configure(yscrollcommand=scrollbar.set)
 
                    timerec.grid_rowconfigure(0, weight=1)
                    timerec.grid_columnconfigure(0, weight=1)
                    con.commit()
                    cursor.close() 
                    adwin_entry.delete(0, tkinter.END)
                else:
                    messagebox.showerror("Failed", f"No records found for employee ID no.: {adwin_entry.get()}")
                    adwin_entry.delete(0, tkinter.END)
            else:
                cursor.close()
                messagebox.showerror("Failed", "Employee ID not found!")
                adwin_entry.delete(0, tkinter.END)
 
        except Error as err:
            print("Access Failed! {}".format(err))
        finally:
            if con.is_connected():
                con.close()
                print("Connection Successful!")
 
    def showemployees(self):
        timerec = CTkToplevel()
        timerec.title("Employees")
        timerec.geometry("1000x200")
        timerec.grab_set()
 
        try:
            con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
            query = "SELECT * FROM tbl_employee ORDER BY emp_id ASC;"
            tree=ttk.Treeview(timerec)
            cur = con.cursor()
            cur.execute(query)
            rows=cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            tree["columns"] = columns
            tree.heading("#0", text="Row No")
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor="center")
            for i, row in enumerate(rows):
                tree.insert("", "end", text=str(i+1), values=row)
            tree.grid(row=0, column=0, sticky="nsew")
 
            scrollbar = ttk.Scrollbar(timerec, orient="vertical", command=tree.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")
            tree.configure(yscrollcommand=scrollbar.set)
 
            timerec.grid_rowconfigure(0, weight=1)
            timerec.grid_columnconfigure(0, weight=1)
            con.commit()
            cur.close()
        except Error as err:
            print("Access Failed! {}".format(err))
        finally:
            if con.is_connected():
                con.close()
                print("Connection Successful!")
 
    def create_employee(self):
        global empid_Entry, fname_Entry, lname_Entry, gend_Entry
        cr_ui = CTkToplevel()
        cr_ui.title("Insert New Employee")
        cr_ui.geometry("180x270")
        cr_ui.grab_set()
 
        CTkLabel(cr_ui,text="Employee ID").pack()
        empid_Entry = CTkEntry(cr_ui,placeholder_text="Input ID")
        empid_Entry.pack()
        CTkLabel(cr_ui,text="Employee First Name").pack()
        fname_Entry = CTkEntry(cr_ui,placeholder_text="Input First Name")
        fname_Entry.pack()
        CTkLabel(cr_ui,text="Employee Last Name").pack()
        lname_Entry = CTkEntry(cr_ui,placeholder_text="Input Last Name")
        lname_Entry.pack()
 
        def on_text_changed(*args):
            text = gend_Entry.get()
            entry_var.set(text.upper())
 
        CTkLabel(cr_ui,text="Employee Gender").pack()
        entry_var = tkinter.StringVar()
        entry_var.trace("w", on_text_changed)
 
        gend_Entry = CTkEntry(cr_ui, textvariable=entry_var)
        gend_Entry.pack()
 
        create = CTkButton(cr_ui, text="Submit", command=self.create_emp)
        create.pack()
 
        def close_window_insert():
            confirmed = messagebox.askyesno("Exit", "Are you sure you want to close the insert window?")
            if confirmed:
                cr_ui.destroy()
 
        cr_ui.protocol("WM_DELETE_WINDOW", close_window_insert)
 
    def create_emp(self):
        entered = empid_Entry.get()
        if entered.isdigit():
            genda = gend_Entry.get()
            if entered.isalpha():
 
                if genda in ["MALE", "FEMALE", "NONBINARY", "NON-BINARY", "NON BINARY"]:
                    try:
                        value1 = empid_Entry.get()
                        value2 = fname_Entry.get()
                        value3 = lname_Entry.get()
                        value4 = gend_Entry.get()
                        con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
                        cursor = con.cursor()
 
                        queryv = "SELECT emp_id FROM tbl_employee WHERE emp_id = %s"
                        cursor.execute(queryv, (value1,))
                        result = cursor.fetchone()
                        if result:
                            messagebox.showerror("Failed", "Employee ID already in the database!")
                            empid_Entry.delete(0, tkinter.END)
                            fname_Entry.delete(0, tkinter.END)
                            lname_Entry.delete(0, tkinter.END)
                            gend_Entry.delete(0, tkinter.END)
                        else:
                            query = "INSERT INTO tbl_employee (emp_id, first_name, last_name, gender) VALUES (%s, %s, %s, %s)"
                            cursor.execute(query, (value1, value2, value3, value4))
                            con.commit()
                            messagebox.showinfo("Success", "Employee inserted successfully!")
                            empid_Entry.delete(0, tkinter.END)
                            fname_Entry.delete(0, tkinter.END)
                            lname_Entry.delete(0, tkinter.END)
                            gend_Entry.delete(0, tkinter.END)
 
 
                    except mysql.connector.Error as err:
                        print("Access Failed! {}".format(err))
                    finally:
                        if con.is_connected():
                            con.close()
                            print("Connection Closed.")
                else:
                    messagebox.showerror("Failed", "Please enter MALE, FEMALE, or NON-BINARY in the Gender Area")
                    empid_Entry.delete(0, tkinter.END)
                    fname_Entry.delete(0, tkinter.END)
                    lname_Entry.delete(0, tkinter.END)
                    gend_Entry.delete(0, tkinter.END)
            else:
                messagebox.showwarning("Failed", "Please enter text in First and Last Name Area!")
                empid_Entry.delete(0, tkinter.END)
                fname_Entry.delete(0, tkinter.END)
                lname_Entry.delete(0, tkinter.END)
                gend_Entry.delete(0, tkinter.END)    
        else:
            messagebox.showerror("Failed", "Please only enter digits on the Employee ID Area")
            empid_Entry.delete(0, tkinter.END)
            fname_Entry.delete(0, tkinter.END)
            lname_Entry.delete(0, tkinter.END)
            gend_Entry.delete(0, tkinter.END)
 
 
    def bura_emp(self):
        global empid_del
        del_ui = CTkToplevel()
        del_ui.title("Delete Employee")
        del_ui.geometry("200x100")
        del_ui.grab_set()
 
        labela = CTkLabel(del_ui, text="Enter the employee ID to delete").pack()
        empid_del = CTkEntry(del_ui,placeholder_text="Input ID")
        empid_del.pack()
 
        b_del = CTkButton(del_ui, text="Submit", command=self.burahin).pack()
 
        def close_window_delete():
            confirmed = messagebox.askyesno("Exit", "Are you sure you want to close the delete window?")
            if confirmed:
                del_ui.destroy()
        del_ui.protocol("WM_DELETE_WINDOW", close_window_delete)
 
 
    def burahin(self):
        try:
            emp_id = empid_del.get()
            con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
            cursor = con.cursor()
 
            queryv = "SELECT emp_id FROM tbl_employee WHERE emp_id = %s"
            cursor.execute(queryv, (emp_id,))
            result = cursor.fetchone()
 
            if result:
                confirm = messagebox.askyesno("Confirmation", f"Are you sure your employee ID is: {empid_Entry}?")
                if confirm:
 
                    query1 = "DELETE FROM tbl_employee WHERE emp_id = %s"
                    cursor.execute(query1, (emp_id,))
                    con.commit()
 
                    query2 = "DELETE FROM tbl_timein WHERE emp_id = %s"
                    cursor.execute(query2, (emp_id,))
                    con.commit()
 
                    query3 = "DELETE FROM tbl_timeout WHERE emp_id = %s"
                    cursor.execute(query3, (emp_id,))
                    con.commit()
 
                    query4 = "DELETE FROM tbl_leave WHERE emp_id = %s"
                    cursor.execute(query4, (emp_id,))
                    con.commit()
 
                    messagebox.showinfo("Success", "Employee and employee records deleted!")
                    empid_del.delete(0, tkinter.END)
                else:
                    cursor.close()
                    empid_del.delete(0, tkinter.END)
            else:
                messagebox.showerror("Failed", "Employee ID not found!")
                empid_del.delete(0, tkinter.END)
 
        except Error as err:
            print("Deletion Failed! {}".format(err))
        finally:
            if con.is_connected():
                con.close()
                print("Connection Closed.")
    
    

        