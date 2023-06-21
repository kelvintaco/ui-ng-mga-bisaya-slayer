import tkinter as tk
from tkinter import messagebox

def handle_radio_button():
    selected_value = radio_var.get()
    print("Selected value:", selected_value)

def handle_confirmation():
    selected_value = radio_var.get()
    messagebox.showinfo("Confirmation", "Selected value: {}".format(selected_value))

window = tk.Tk()

radio_var = tk.StringVar()
radio_button1 = tk.Radiobutton(window, text="Option 1", variable=radio_var, value="Option 1", command=handle_radio_button)
radio_button1.pack()

radio_button2 = tk.Radiobutton(window, text="Option 2", variable=radio_var, value="Option 2", command=handle_radio_button)
radio_button2.pack()

confirmation_button = tk.Button(window, text="Confirm", command=handle_confirmation)
confirmation_button.pack()

window.mainloop()