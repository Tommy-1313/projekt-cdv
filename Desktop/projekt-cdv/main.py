import requests
import json

# URL API do pobrania wszystkich stacji
url = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"

response = requests.get(url)

if response.status_code == 200:
    stations = response.json()
    print(f"Znaleziono {len(stations)} stacji.")

    # Zapisz do pliku
    with open("stations.json", "w", encoding="utf-8") as f:
        json.dump(stations, f, ensure_ascii=False, indent=2)

    print("Zapisano dane do pliku stations.json")
else:
    print("Błąd pobierania danych:", response.status_code)