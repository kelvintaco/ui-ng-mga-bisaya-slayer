import mysql.connector
from tkinter import *

def insert_data1():
    # Retrieve the input from the text box
    value = entry.get()

    # Establish the database connection
    con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')

    # Create a cursor object
    cursor = con.cursor()

    # Prepare the INSERT query for table1 with the column name and placeholder for the value
    query = "INSERT INTO tbl_timein (emp_id) VALUES (%s)"

    # Execute the INSERT query with the provided value
    cursor.execute(query, (value,))

    # Commit the changes to the database
    con.commit()

    # Close the cursor and database connection
    cursor.close()
    con.close()

def insert_data2():
    # Retrieve the input from the text box
    value = entry.get()

    # Establish the database connection
    con = mysql.connector.connect(host='localhost', port='3306', database='db_empdb', user='root', password='')

    # Create a cursor object
    cursor = con.cursor()

    # Prepare the INSERT query for table2 with the column name and placeholder for the value
    query = "INSERT INTO tbl_timeout (emp_id) VALUES (%s)"

    # Execute the INSERT query with the provided value
    cursor.execute(query, (value,))

    # Commit the changes to the database
    con.commit()

    # Close the cursor and database connection
    cursor.close()
    con.close()

# Create the Tkinter window
window = Tk()

# Create the text box
entry = Entry(window)
entry.pack()

# Create the button to insert into table1
button1 = Button(window, text="Insert into Table1", command=insert_data1)
button1.pack()

# Create the button to insert into table2
button2 = Button(window, text="Insert into Table2", command=insert_data2)
button2.pack()

# Start the Tkinter event loop
window.mainloop()
