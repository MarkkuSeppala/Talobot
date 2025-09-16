def tallenna_puhdistettu_toimitussisalto_csv(puhdistettu_toimitussisalto, toimittaja, toimitussisalto_id):
    """
    Tallentaa puhdistetun toimitussisällön CSV-muotoon testausta varten.
    
    Args:
        puhdistettu_toimitussisalto: Puhdistettu toimitussisältö API-kyselymuodossa
        toimittaja: Toimittajan nimi
        toimitussisalto_id: Toimitussisällön ID
    """
    try:
        import csv
        import os
        from datetime import datetime
        
        # Luo data/puhd_toimis kansio jos se ei ole olemassa
        output_dir = "data/puhd_toimis"
        os.makedirs(output_dir, exist_ok=True)
        
        # Luo CSV-tiedoston nimi aikaleimalla
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"toimitussisalto_{toimittaja}_{toimitussisalto_id}_{timestamp}.csv"
        csv_path = os.path.join(output_dir, csv_filename)
        
        # Tarkista onko CSV-tiedosto jo olemassa ja lisää rivi siihen
        file_exists = os.path.exists(csv_path)
        
        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'toimitussisalto_id', 
                'toimittaja', 
                'timestamp',
                'puhdistettu_toimitussisalto'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Kirjoita otsikot vain jos tiedosto on uusi
            if not file_exists:
                writer.writeheader()
            
            # Kirjoita toimitussisältö
            writer.writerow({
                'toimitussisalto_id': toimitussisalto_id,
                'toimittaja': toimittaja,
                'timestamp': timestamp,
                'puhdistettu_toimitussisalto': puhdistettu_toimitussisalto
            })
        
        print(f"📄 Puhdistettu toimitussisältö tallennettu CSV-muotoon: {csv_path}")
        
    except Exception as e:
        print(f"❌ Virhe CSV-tallennuksessa: {str(e)}")

