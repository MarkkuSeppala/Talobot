from SQL_kyselyt import *
from SQL_kyselyt_tuotteet_tauluun import *
from config_data import *
from utils.file_handler import *
from utils.tietosissallon_kasittely import *



#get_all_tables()
#get_all_table_structures()
#tulosta_toimitussisallot()
#tulosta_kayttajat()
#tulosta_toimittajat()
#hae_toimittaja_uuidlla("18845722-122c-4d87-81aa-a8b696b69faf")
#hae_toimitussisalto_txt_url_uuidlla(uuid: str)

#hae_kaikki_ikkunat()
#hae_paivan_ikkunat("07.04.2025")
#hae_toimitussisallon_ikkunat(840)

#hae_toimittajan_sisallot(2)
#hae_toimitussisalto(912)
#print("toimittaja_uuid", hae_toimittajan_id_nimella("Sievitalo"))
#hae_paivan_toimitussisallot("01.04.2025")
#hae_paivan_toimitussisallot("30.03.2025")

#hae_paivan_ulko_ovet("30.03.2025")
#hae_paivan_ulko_ovet("07.04.2025")
#tulosta_kaikki_ulko_ovet(10) #parametri -> montako viimeisintä ulko-ovetta tulostetaan. Tyhjä -> tulostetaan kaikki ulko-ovet.
#hae_toimitussisallon_ulko_ovet(840) 

#hae_paivan_valiovet("07.04.2025")
#hae_toimitussisallon_valiovet(840)
#print(hae_uuid_toimitussisalto_idlla(914))
#print(hae_pdf_url_uuidlla(uuid=hae_uuid_toimitussisalto_idlla(914)))

#nayta_toimitussisalto_tuotteet()
#hae_toimitussisallon_tuotteet(842)
#hae_toimitussisallon_tuotteet_2(958)
#hae_kaikki_vertailut()
#hae_vertailun_toimitussisalto_1_tiedot(3)

#kirjoita_json_tiedostoon(hae_toimitussisallon_ikkunat(839), TESTI_1_TXT)
#kirjoita_json_tiedostoon(hae_toimitussisallon_tuotteet(840), TESTI_1_TXT)


# tallenna_toimitussisalto_json(tuotteet: list = None, ikkunat: list = None, ulko_ovet: list = None, valiovet: list = None, toimitussisalto_id: int = None, tiedosto: str = None) -> bool:
#tallenna_toimitussisalto_json(hae_toimitussisallon_tuotteet_2(840), hae_toimitussisallon_ikkunat(840), hae_toimitussisallon_ulko_ovet(840), hae_toimitussisallon_valiovet(840), 840, TESTI_1_TXT)
#toimitussisalto_id = 960
#tulosta_toimitussisalto_taulukkona(hae_toimitussisallon_tuotteet_2(toimitussisalto_id), hae_toimitussisallon_ikkunat(toimitussisalto_id), 
#                                  hae_toimitussisallon_ulko_ovet(toimitussisalto_id), hae_toimitussisallon_valiovet(toimitussisalto_id), TESTI_1_TXT, toimitussisalto_id)   




#------------kantaan muutoksia tekevät kyselyt------------
#update_table()
#add_user(email, password)
#aktivoi_kayttaja(kayttaja_id)
#lisaa_toimittaja(toimittaja_nimi)
#update_toimitussisallot_table
#paivita_ulko_ovet_taulu()
#muuta_toimitussisallot_taulun_sarakkeen_nimi("txt_sisalto", "txt_url") #muuttaa sarakkeen nimen txt_sisalto -> txt_url
#poista_toimitussisallot_ennen("01.04.2025")
#poista_toimitussisalto_materiaalit_ja_palvelut_taulu()
#poista_toimitussisalto_tuotteet_taulu()
#luo_toimitussisalto_tuotteet_taulu()
#luo_vertailut_taulu()




#-------------tuotteet-tauluun liittyvät kyselyt------------
#tuo_tuotteet_sheetista("https://docs.google.com/spreadsheets/d/e/2PACX-1vRUnUDHjtkbxzT_J--kq8H0VN9q-0I4P2wf-7jV_uofZHyVZT5CyqTv-u1V4jXvG4TKieo4Tv76gM5N/pub?gid=0&single=true&output=csv")
#tyhjenna_tuotteet_taulu()
#muuta_tuotteet_taulun_hinta_sarake_nullable()
#muuta_tuotteet_taulun_sarakkeen_nimi() #muuttaa sarakkeen nimen tuote -> tuote_tarkennus
#lisaa_tuotteet_taulun_viite_tuote_id_sarake()
#korjaa_tuotteet_taulun_null_arvot()
#poista_tuotteet_taulu()
#luo_tuotteet_taulu_uudelleen(), get_all_table_structures()
#korjaa_tuotteet_taulu()
#nayta_tuotteet()
#nayta_tuote(121)
#tallenna_tuotteet_tiedostoon("C:\Talobot")
#tallenna_tuotteet_ID_ja_nimi_tiedostoon("C:\Talobot")
#print(hae_tuotteet_prompt1_str_id_ja_nimi())
#tarkista_prompt1_arvot()
#print(hae_tuotteet_ja_tarkennus_prompt1_str())
#print(hae_tuotteet_prompt1_str())




