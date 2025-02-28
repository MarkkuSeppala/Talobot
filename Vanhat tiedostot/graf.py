import tkinter as tk
import os
import sie 
from datetime import datetime

# Luo pääikkuna
root = tk.Tk()
root.title("Tulostusikkuna")

# Luo tekstikenttä tulostuksille
output_text = tk.Text(root, height=50, width=100, wrap="word")
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Lisää pystysuuntainen vierityspalkki
scrollbar = tk.Scrollbar(root, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Kytke tekstikenttä vierityspalkkiin
output_text.config(yscrollcommand=scrollbar.set)



def tulosta_viesti(viesti, aika=""):
    """ Lisää viesti graafiseen ikkunaan ja rullaa näkymä alas. """
    output_text.insert(tk.END, f"{viesti} {aika}\n")  
    output_text.see(tk.END)  # Vieritä alas uusimman viestin kohdalle

# Luo painikkeet jokaiselle lohkolle
btn_lohko1 = tk.Button(root, text="Suorita Lohko 1", command=sie.suorita_lohko1)
btn_lohko1.pack()

btn_lohko2 = tk.Button(root, text="Suorita Lohko 2", command=sie.suorita_lohko2)
btn_lohko2.pack()

btn_lohko3 = tk.Button(root, text="Suorita Lohko 3", command=sie.suorita_lohko3)
btn_lohko3.pack()

btn_lohko4 = tk.Button(root, text="Suorita Lohko 4", command=sie.suorita_lohko4)
btn_lohko4.pack()

btn_lohko5 = tk.Button(root, text="Suorita Lohko 5", command=sie.suorita_lohko5)
btn_lohko5.pack()


root.mainloop()
