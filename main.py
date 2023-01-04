import os
import random
import sys
import threading
import time
import tkinter
import tkinter.messagebox
import tkinter.ttk as ttk

import tkmacosx
import ttkthemes
from mttkinter import mtTkinter
from PIL import Image

import splashscreen

THEME = "Clearlooks"


def calculate_standard_drink(abv, volume):
    """Calculate the number of standard drink in a drink"""
    return round(abv * volume / 1000, 2)


splash = splashscreen.SplashScreen(Image.open(os.path.join("splashscreen.png")),
                                   most_common_color_idx=random.randint(0, 4),
                                   theme=THEME,
                                   )
splash.tk.call('wm', 'iconphoto', splash._w, tkinter.PhotoImage(file=os.path.join("icon.png")))
class Drunkmeter(ttkthemes.ThemedTk, mtTkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Drunkmeter")
        # Configure the rows and columns to be resizable
        for row in range(5):
            self.rowconfigure(row, weight=1)
        for col in range(3):
            self.columnconfigure(col, weight=1)
        self.build_ui()
        
    def build_ui(self):
        self.abv_label = tkinter.Label(self, text="ABV (%)")
        self.abv_label.grid(row=0, column=0)

        self.vol_label = tkinter.Label(self, text="Volume (ml)")
        self.vol_label.grid(row=0, column=1, columnspan=2)

        self.vol_var = tkinter.DoubleVar()
        self.abv_var = tkinter.DoubleVar()

        self.abv_entry = tkinter.Entry(self, textvariable=self.abv_var)
        self.abv_entry.grid(row=1, column=0)

        vol_entry = tkinter.Entry(self, textvariable=self.vol_var)
        vol_entry.grid(row=1, column=1)

        self.result_label = tkinter.Label(self, text="Result: ")
        self.result_label.grid(row=1, column=2)
        
        self.calculate_btn = tkmacosx.Button(self, text="Calculate", command=self.calculate)
        self.calculate_btn.configure(bg="#FFC000", fg="black",
                                activebackground="#ffd558", activeforeground="black")
        self.calculate_btn.grid(row=2, column=0, columnspan=3, padx=10)

        # Display a grid displaying the alcohol dosage according to psychonautwiki
        self.dosage_label = tkinter.Label(self, text="Alcohol dosage (Standard drinks)")
        self.dosage_label.grid(row=3, column=0, columnspan=3)

        dosage_table = tkinter.Listbox(self)
        dosage_table.grid(row=4, column=0, columnspan=3)
        # Set the dosage table items to be unselectable and to display 5 items
        dosage_table.config(selectmode="none", height=5, width=30)

        dosage_table.insert(tkinter.END, "Threshold: 1 standard drink")
        dosage_table.insert(tkinter.END, "Light: 1-3 standard drinks")
        dosage_table.insert(tkinter.END, "Common: 3-5 standard drinks")
        dosage_table.insert(tkinter.END, "Strong: 5-6 standard drinks")
        dosage_table.insert(tkinter.END, "Heavy: 6+ standard drinks")

    def calculate(self):
        try:
            if self.abv_var.get() >= 100:
                tkinter.messagebox.showerror(
                    "Error", "ABV must be less than 100%", icon="error", parent=self)
                return
            elif self.abv_var.get() <= 0:
                tkinter.messagebox.showerror(
                    "Error", "ABV must be greater than 0%", icon="error", parent=self)
                return
            elif self.vol_var.get() <= 0:
                tkinter.messagebox.showerror(
                    "Error", "Volume must be greater than 0", icon="error", parent=self)
                return
            standard_drinks = calculate_standard_drink(self.abv_var.get(), self.vol_var.get())
            result = f"{standard_drinks} standard drink{standard_drinks > 1 and 's' or ''}"
        except ValueError as e:
            # tkinter.messagebox.showerror("Error", str(e), icon="error", parent=tk)
            result = "Invalid input"

        self.result_label.config(text="Result: {}".format(result))
            
loading_texts = ["Loading wines", "Opening cans of beers",
                    "Loading spirits", "Mixing cocktails", "Pouring shots"]
win = Drunkmeter(theme=THEME)
win.eval('tk::PlaceWindow %s center' % win.winfo_pathname(win.winfo_id()))

def loading_thread():
    # Focus to the loading window
    splash.focus_force()
    win.withdraw()
    if sys.platform in ['win32', 'cygwin']:
        win.wm_attributes("-disabled", True)
    time.sleep(0.5)
    for i, text in enumerate(loading_texts):
        splash.loading_status = text
        time.sleep(0.5)
    
    if sys.platform in ['win32', 'cygwin']:
        win.wm_attributes("-disabled", False)
    time.sleep(0.5)
    splash.withdraw()
    win.deiconify()

splash.loading_status = "Loading..."
threading.Thread(target=loading_thread, name="SplashScreen Thread").start()
splash.mainloop()