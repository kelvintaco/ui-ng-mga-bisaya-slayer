from tkinter import Tk
from main_window import MainWindow
import customtkinter


if __name__ == "__main__":
    masterctk = customtkinter.CTk()
    masterctk.title('Main Window')
    masterctk.geometry('650x200')
    customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

    main_window = MainWindow(masterctk)
    masterctk.resizable(False, False)
    masterctk.mainloop()
