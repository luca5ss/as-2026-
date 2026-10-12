import os
import requests

# Údaje se načtou bezpečně ze systému, na GitHubu nikdo neuvidí tvá hesla
ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID", "TVOJE_ACCOUNT_ID")
DATABASE_ID = os.environ.get("CF_DATABASE_ID", "TVOJE_DATABASE_ID")
API_TOKEN = os.environ.get("CF_API_TOKEN", "TVUJ_API_TOKEN")

url = f"https://cloudflare.com{ACCOUNT_ID}/d1/database/{DATABASE_ID}/query"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "sql": """
        SELECT zaci.jmeno, zaci.prijmeni, krouzky.nazev, prihlasky.zaplaceno 
        FROM prihlasky
        JOIN zaci ON prihlasky.id_zaka = zaci.id_zaka
        JOIN krouzky ON prihlasky.id_krouzku = krouzky.id_krouzku;
    """
}

try:
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if data.get("success"):
        results = data["result"][0]["results"]  # Oprava indexu pro Cloudflare D1 JSON response
        print("--- SEZNAM PŘIHLÁŠEK Z CLOUDU ---")
        for radek in results:
            print(f"{radek['jmeno']} {radek['prijmeni']} -> {radek['nazev']} ({radek['zaplaceno']})")
    else:
        print("Cloudflare vrátil chybu:", data.get("errors"))
except Exception as e:
    print(f"Nepodařilo se připojit: {e}")
