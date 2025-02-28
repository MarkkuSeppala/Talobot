import tkinter as tk
from tkinter import scrolledtext
import subprocess

# Funktiot jokaisen lohkon suorittamiseen
def suorita_lohko1():
    tulos = subprocess.run(["python", "C:/Graafinen/lohko1.py"], capture_output=True, text=True)
    tulostus.insert(tk.END, tulos.stdout + "\n")

def suorita_lohko2():
    tulos = subprocess.run(["python", "C:/Graafinen/lohko2.py."], capture_output=True, text=True)
    tulostus.insert(tk.END, tulos.stdout + "\n")
    
def suorita_lohko3():
    tulos = subprocess.run(["python", "C:/Graafinen/lohko3.py"], capture_output=True, text=True)
    tulostus.insert(tk.END, tulos.stdout + "\n")

def suorita_lohko4():
    tulos = subprocess.run(["python", "C:/Graafinen/lohko4.py"], capture_output=True, text=True)
    tulostus.insert(tk.END, tulos.stdout + "\n")

# Luo käyttöliittymä
root = tk.Tk()
root.title("Lohkojen Suoritus")

# Luo painikkeet
btn_lohko1 = tk.Button(root, text="Suorita Lohko 1. Hakee ohjelmakirjastot", command=suorita_lohko1)
btn_lohko1.pack()

btn_lohko2 = tk.Button(root, text="Suorita Lohko 2. Muuttaa pdf-tiedoston tekstitiedostoksi", command=suorita_lohko2)
btn_lohko2.pack()

btn_lohko3 = tk.Button(root, text="Suorita Lohko 3. Poistaa turhaa tietoa", command=suorita_lohko3)
btn_lohko3.pack()

btn_lohko4 = tk.Button(root, text="Suorita Lohko 4. Tulostaa ikkunaluettelon", command=suorita_lohko4)
btn_lohko4.pack()

# Luo tulostusalue
tulostus = scrolledtext.ScrolledText(root, width=130, height=20)
tulostus.pack()

root.mainloop()
