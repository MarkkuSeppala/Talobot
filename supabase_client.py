from supabase import create_client, Client

# Lisää omat API-avaimesi
supabase_url = "https://gukkfrcbnbiqgaydeflc.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd1a2tmcmNibmJpcWdheWRlZmxjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIwMzA4MDUsImV4cCI6MjA1NzYwNjgwNX0.VOMhTyi9xfwDj3UVov2Gz2vA5SPb_lsdeBzfKmW_tNE"

# Luo yhteys
supabase: Client = create_client(supabase_url, supabase_key)

print("Yhteys Supabaseen onnistui!")


def add_user(email, name):
    response = supabase.table("users").insert({"email": email, "name": name}).execute()
    if response.data:
        print(f"Käyttäjä {name} lisätty onnistuneesti!")
    else:
        print("Virhe lisättäessä käyttäjää.")

# Esimerkki
#add_user("test@example.com", "Matti Meikäläinen")




def get_user_id(email):
    response = supabase.table("users").select("id").eq("email", email).execute()
    if response.data:
        return response.data[0]['id']
    return None

def get_user_name(email):
    response = supabase.table("users").select("name").eq("email", email).execute()
    if response.data:
        return response.data[0]['name']
    return None

user_id = get_user_name("test@example.com")
print(user_id)

# def update_user(user_id, new_name):
#     response = supabase.table("users").update({"name": new_name}).eq("id", user_id).execute()
#     if response.data:
#         print(f"Käyttäjä päivitetty: {new_name}")
#     else:
#         print("Virhe päivityksessä.")

# #Esimerkki
# update_user("1", "Pekka Pekkanen")



# user_id = get_user_id("test@example.com")  # Käyttäjän sähköpostiosoite
# if user_id:
#     update_user(user_id, "Pekka Pekkanen")
# else:
#     print("Käyttäjää ei löytynyt!")



# from flask import Flask, jsonify
# from supabase import create_client, Client

# app = Flask(__name__)

# supabase_url = "https://gukkfrcbnbiqgaydeflc.supabase.co"
# supabase_key = "your-anon-key"
# supabase: Client = create_client(supabase_url, supabase_key)

# @app.route('/users')
# def get_users():
#     response = supabase.table("users").select("*").execute()
#     return jsonify(response.data)

# if __name__ == '__main__':
#     app.run(debug=True)

