import sqlite3
import json

# Wczytaj dane z pliku JSON
with open("stations.json", "r", encoding="utf-8") as f:
    stations = json.load(f)

# Połącz z bazą danych (plik zostanie utworzony, jeśli nie istnieje)
conn = sqlite3.connect("stations.db")
cursor = conn.cursor()

# Utwórz tabelę (jeśli nie istnieje)
cursor.execute("""
CREATE TABLE IF NOT EXISTS stations (
    id INTEGER PRIMARY KEY,
    stationName TEXT,
    city TEXT,
    latitude REAL,
    longitude REAL
)
""")

# Wstaw dane do tabeli
for station in stations:
    station_id = station["id"]
    name = station["stationName"]
    city = station["city"]["name"] if station["city"] else "brak"
    lat = station["gegrLat"]
    lon = station["gegrLon"]

    cursor.execute("""
        INSERT OR REPLACE INTO stations 
            (id, stationName, city, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
    """, (station_id, name, city, lat, lon))

# Zatwierdź zmiany i zamknij połączenie
conn.commit()
conn.close()

print("Dane zostały zapisane do bazy danych stations.db.")