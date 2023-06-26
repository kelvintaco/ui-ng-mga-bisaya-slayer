from tkinter import messagebox, Entry, Button, Toplevel, Label
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
import tkinter

class AdminWindow:
    def __init__(self, master, main_window):
        self.master = master
        self.main_window = main_window
        self.create_widgets()
        self.main_window.withdraw()

    def create_widgets(self):
        global adwin_entry
        
        '''def validate_text(action, text):
            if action == '1':
                if text.isstring():
                    return True
                else:
                    return False'''

        adwin_entry = Entry(self.master)
        adwin_entry.pack()

        self.time_in_records_button = Button(self.master, text='Time In Records', command=self.show_time_in_records)
        self.time_in_records_button.pack()

        self.time_out_records_button = Button(self.master, text='Time Out Records', command=self.show_time_out_records)
        self.time_out_records_button.pack()

        self.leave_records_button = Button(self.master, text='Leave Records', command=self.show_leave_records)
        self.leave_records_button.pack()

        self.button_create = Button(self.master, text="Insert New Employee", command=self.create_employee)
        self.button_create.pack()
        
        button_view = Button(self.master, text="View Employees", command=self.showemployees)
        button_view.pack()

        del_b = tkinter.Button(self.master, text="Delete Employee", command=self.bura_emp).pack()

        self.back_button = Button(self.master, text='Back', command=self.back)
        self.back_button.pack()

        
        def close_window():
            confirmed = messagebox.askyesno("Exit", "Are you sure you want to close the application?")
            if confirmed:
                self.master.destroy()
                self.main_window.destroy()

        self.close_button = Button(self.master, text='Close', command=close_window)
        self.close_button.pack()
                
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
                    timerec = Toplevel(self.master)
                    timerec.title("Time in Records")
                    timerec.geometry("600x200")
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
            else:
                cursor.close()
                messagebox.showerror("Failed", "Employee ID not found!")

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
                    timerec = Toplevel(self.master)
                    timerec.title("Time out Records")
                    timerec.geometry("600x200")
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
            else:
                cursor.close()
                messagebox.showerror("Failed", "Employee ID not found!")

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
            if result:
                queryv = "SELECT emp_id FROM tbl_leave WHERE emp_id = %s"
                cursor.execute(queryv, (adwin_entry.get(),))
                result = cursor.fetchone()
                if result:
                    timerec = Toplevel(self.master)
                    timerec.title("Leave Records")
                    timerec.geometry("600x200")
                    timerec.grab_set()
                    tree=ttk.Treeview(timerec)
                    
                    query = """SELECT e.emp_id, e.first_name, e.last_name, t.leave_type, t.start_date, t.end_date
                    FROM tbl_employee e
                    RIGHT JOIN tbl_leave t
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
            else:
                cursor.close()
                messagebox.showerror("Failed", "Employee ID not found!")

        except Error as err:
            print("Access Failed! {}".format(err))
        finally:
            if con.is_connected():
                con.close()
                print("Connection Successful!")

    def showemployees(self):
        timerec = Toplevel(self.master)
        timerec.title("Employees")
        timerec.geometry("600x200")
        timerec.grab_set()

        try:
            con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
            query = "SELECT * FROM tbl_employee"
            tree=ttk.Treeview(timerec)
            cur = con.cursor()
            cur.execute(query)
            rows=cur.fetchall()
            columns = [desc[0] for desc in cur.description]
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
            cur.close()
        except Error as err:
            print("Access Failed! {}".format(err))
        finally:
            if con.is_connected():
                con.close()
                print("Connection Successful!")

    def create_employee(self):
        global empid_Entry, fname_Entry, lname_Entry, gend_Entry
        self.master = Toplevel(self.master)
        self.master.title("Insert New Employee")
        self.master.geometry("300x400")
        self.master.grab_set()

        Label(self.master,text="Employee ID").pack()
        empid_Entry = ttk.Entry(self.master)
        empid_Entry .pack()
        Label(self.master,text="Employee First Name").pack()
        fname_Entry = ttk.Entry(self.master)
        fname_Entry.pack()
        Label(self.master,text="Employee Last Name").pack()
        lname_Entry = ttk.Entry(self.master)
        lname_Entry.pack()

        def on_text_changed(*args):
            text = gend_Entry.get()
            entry_var.set(text.upper())

        Label(self.master,text="Employee Gender").pack()
        entry_var = tkinter.StringVar()
        entry_var.trace("w", on_text_changed)

        gend_Entry = ttk.Entry(self.master, textvariable=entry_var)
        gend_Entry.pack()

        create = Button(self.master, text="Submit", command=self.create_emp)
        create.pack()

    def create_emp(self):
        entered = empid_Entry.get()
        if entered.isdigit():
            genda = gend_Entry.get()
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
                    else:
                        query = "INSERT INTO tbl_employee (emp_id, first_name, last_name, gender) VALUES (%s, %s, %s, %s)"
                        cursor.execute(query, (value1, value2, value3, value4))
                        con.commit()
                        messagebox.showinfo("Success", "Employee inserted successfully!")

                except mysql.connector.Error as err:
                    print("Access Failed! {}".format(err))
                finally:
                    if con.is_connected():
                        con.close()
                        print("Connection Closed.")
            else:
                messagebox.showerror("Failed", "Please enter MALE, FEMALE, or NON-BINARY in the gender area")
        else:
            messagebox.showerror("Failed", "Please only enter digits on the Employee ID area")

    def bura_emp(self):
        global empid_del
        del_ui = Toplevel(self.master)
        del_ui.title("Delete Employee")
        del_ui.geometry("300x400")
        del_ui.grab_set()

        labela = Label(del_ui, text="Enter the employee ID to delete").pack()
        empid_del = Entry(del_ui)
        empid_del.pack()

        b_del = Button(del_ui, text="Submit", command=self.burahin).pack()

    def burahin(self):
        try:
            emp_id = empid_del.get()
            con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')
            cursor = con.cursor()

            queryv = "SELECT emp_id FROM tbl_employee WHERE emp_id = %s"
            cursor.execute(queryv, (emp_id,))
            result = cursor.fetchone()
            if result:
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
            else:
                messagebox.showerror("Failed", "Employee ID not found!")

        except Error as err:
            print("Deletion Failed! {}".format(err))
        finally:
            if con.is_connected():
                con.close()
                print("Connection Closed.")
    
    def back(self):
        adwin_entry.destroy()
        self.main_window.deiconify()