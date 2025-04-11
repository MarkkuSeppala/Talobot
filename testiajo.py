import PyPDF2
from utils.file_handler import *

# def lue_pdf_tiedostosta():
#     """
#     Pyytää käyttäjältä PDF-tiedoston nimen ja palauttaa sen sisällön.
    
#     Returns:
#         str: PDF-tiedoston sisältö
#     """
#     try:
#         # Pyydetään käyttäjältä tiedoston nimi
#         tiedosto_nimi = input("Anna PDF-tiedoston nimi: ")
        
#         # Avataan PDF-tiedosto
#         with open(tiedosto_nimi, 'rb') as pdf_file:
#             pdf_reader = PyPDF2.PdfReader(pdf_file)
            
#             # Kerätään kaikki sivujen tekstit
#             pdf_sisalto = ""
#             for page in pdf_reader.pages:
#                 pdf_sisalto += page.extract_text() + "\n"
                
#             return pdf_sisalto
                
#     except Exception as e:
#         print(f"Virhe PDF-tiedoston lukemisessa: {e}")
#         return None

# if __name__ == "__main__":
#     pdf_sisalto = lue_pdf_tiedostosta()
#     if pdf_sisalto:
#         print(pdf_sisalto)


# pdf = muuta_pdf_tekstiksi(lue_pdf_tiedostosta())
# print(pdf)


from docling.document_converter import DocumentConverter

source = "C:/Testi toimitussisällöt/Kastelli Ritari.pdf"  # document per local path or URL
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())  # output: "## Docling Technical Report[...]"