"""
Pobiera dane stacji z API GIOŚ i zapisuje je do lokalnej bazy SQLite.
Autor: Tomek Łukasiewicz
"""

import sqlite3
import requests


def download_stations():
    """
    Pobierz listę stacji pomiarowych z API GIOŚ.
    """
    url = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print("Błąd pobierania danych z API GIOŚ")
    return []


def refresh_database(stations):
    """
    Nadpisz bazę danych SQLite nowymi danymi o stacjach.
    """
    conn = sqlite3.connect("stations.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS stations")

    cursor.execute("""
        CREATE TABLE stations (
            id INTEGER PRIMARY KEY,
            stationName TEXT,
            city TEXT,
            latitude REAL,
            longitude REAL
        )
    """)

    for station in stations:
        station_id = station["id"]
        name = station["stationName"]
        city = (
            station["city"]["name"] if station["city"]
            else "Nieznane"
        )
        lat = station["gegrLat"]
        lon = station["gegrLon"]

        cursor.execute(
            """
            INSERT INTO stations (
                id, stationName, city, latitude, longitude
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (station_id, name, city, lat, lon)
        )

    conn.commit()
    conn.close()
    print(f"Zapisano {len(stations)} stacji do bazy.")


if __name__ == "__main__":
    stations = download_stations()
    if stations:
        refresh_database(stations)