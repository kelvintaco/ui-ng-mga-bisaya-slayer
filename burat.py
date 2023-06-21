import tkinter as tk
from tkcalendar import Calendar, DateEntry

def get_selected_date():
    selected_date = cal.get_date()
    print(f"Selected date: {selected_date}")

window = tk.Tk()

cal = Calendar(window)
cal.pack()

selected_date_button = tk.Button(window, text="Get Selected Date", command=get_selected_date)
selected_date_button.pack()

window.mainloop()