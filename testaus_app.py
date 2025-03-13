#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


from flask import Flask, request, render_template, render_template_string, Response, redirect, url_for, jsonify
import os
import sys




from config_data import (VALIOVITYYPIT_SIEVITALO_JSON, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT,  
                        IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON, PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNA2_JSON, ULKO_OVI_TIEDOT_2_JSON,
                        PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, 
                        PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_JSON_MUOTOON,
                        PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT,

                        PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT, PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON,
                        IKKUNATIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, IKKUNA2_KASTELLI_JSON, PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT,
                        PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT, PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT, PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT, 
                        PROMPT_KASTELLI_ULKO_OVI_TIEDOT_JSON_MUOTOON, IKKUNA_KASTELLI_JSON, TOIMITUSSISALTO_KASTELLI_TXT, ULKO_OVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT,
                        VALIOVITYYPIT_KASTELLI_TXT, VALIOVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, VALIOVITYYPIT_KASTELLI_JSON)

from api_run import api_run_sievitalo, api_run_kastelli
from utils.file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet, muuta_pdf_tekstiksi_2
from utils.tietosissallon_kasittely import jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi, clean_text2


import tkinter as tk
from tkinter import filedialog
import json





import tkinter as tk
from tkinter import filedialog

def lataa_pdf():
    def valitse_tiedosto():
        tiedosto = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if tiedosto:
            print(f"Tiedosto {tiedosto} ladattu onnistuneesti!")
            with open(tiedosto, 'rb') as file:
                pdf_data = file.read()
            root.destroy()
            global pdf_tiedosto
            pdf_tiedosto = pdf_data
    
    root = tk.Tk()
    root.title("Valitse PDF-tiedosto")
    root.geometry("300x150")
    
    button = tk.Button(root, text="Lataa PDF", command=valitse_tiedosto)
    button.pack(pady=20)
    
    root.mainloop()
    
    return pdf_tiedosto if 'pdf_tiedosto' in globals() else None




#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



# Käyttö:
pdf_tiedosto = lataa_pdf()
if pdf_tiedosto:
    print("PDF-tiedosto ladattu onnistuneesti.")
else:
    print("Ei tiedostoa valittu.")


teksti = muuta_pdf_tekstiksi_2(pdf_tiedosto)
#print( "muutettu teksti:", teksti)
kirjoita_txt_tiedosto(teksti, TOIMITUSSISALTO_KASTELLI_TXT)
#print(lue_txt_tiedosto(TOIMITUSSISALTO_KASTELLI_TXT))
teksti2 = lue_txt_tiedosto(TOIMITUSSISALTO_KASTELLI_TXT)
clean_text2(teksti2, PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT)
#print(lue_txt_tiedosto(PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT))
print(lue_txt_tiedosto(PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT))
api_run_kastelli()

#print(lue_json_tiedosto(IKKUNA_KASTELLI_JSON))
#print(lue_txt_tiedosto(ULKO_OVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT))
#print(lue_json_tiedosto(ULKO_OVI_TIEDOT_2_JSON))
print(lue_txt_tiedosto(VALIOVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT))
print(lue_json_tiedosto(VALIOVITYYPIT_KASTELLI_JSON))

# Käyttö:
# json_tiedosto = lataa_json()
# if json_tiedosto:
#     print("JSON-tiedosto ladattu ja tulostettu onnistuneesti.")
# else:
#     print("Ei tiedostoa valittu.")
