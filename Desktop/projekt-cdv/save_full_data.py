"""
Pobieranie stacji, sensorów i pomiarów z API GIOŚ oraz zapis do SQLite.
Autor: Tomek Łukasiewicz
"""

import sqlite3
import requests

BASE_URL = "https://api.gios.gov.pl/pjp-api/rest"


def get_stations():
    """
    Zwróć listę wszystkich stacji z API GIOŚ.
    """
    url = f"{BASE_URL}/station/findAll"
    response = requests.get(url)
    return response.json()


def get_sensors(station_id):
    """
    Zwróć listę sensorów dla podanej stacji.
    """
    url = f"{BASE_URL}/station/sensors/{station_id}"
    response = requests.get(url)
    return response.json()


def get_measurements(sensor_id):
    """
    Zwróć dane pomiarowe dla danego sensora.
    """
    url = f"{BASE_URL}/data/getData/{sensor_id}"
    response = requests.get(url)
    return response.json()


def create_tables():
    """
    Tworzy tabele 'sensors' i 'measurements' w bazie SQLite.
    """
    conn = sqlite3.connect("stations.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS sensors")
    cursor.execute("DROP TABLE IF EXISTS measurements")

    cursor.execute("""
        CREATE TABLE sensors (
            id INTEGER PRIMARY KEY,
            station_id INTEGER,
            param_name TEXT,
            param_code TEXT,
            FOREIGN KEY(station_id) REFERENCES stations(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER,
            value REAL,
            date TEXT,
            FOREIGN KEY(sensor_id) REFERENCES sensors(id)
        )
    """)

    conn.commit()
    conn.close()


def save_data():
    """
    Pobiera i zapisuje sensory i pomiary do bazy danych.
    """
    stations = get_stations()
    conn = sqlite3.connect("stations.db")
    cursor = conn.cursor()

    for station in stations:
        station_id = station["id"]
        sensors = get_sensors(station_id)

        for sensor in sensors:
            sensor_id = sensor["id"]
            param = sensor["param"]
            param_name = param["paramName"]
            param_code = param["paramCode"]

            cursor.execute(
                """
                INSERT INTO sensors (
                    id, station_id, param_name, param_code
                ) VALUES (?, ?, ?, ?)
                """,
                (sensor_id, station_id, param_name, param_code)
            )

            measurements = get_measurements(sensor_id).get("values", [])
            for m in measurements:
                if m["value"] is not None:
                    cursor.execute(
                        """
                        INSERT INTO measurements (
                            sensor_id, value, date
                        ) VALUES (?, ?, ?)
                        """,
                        (sensor_id, m["value"], m["date"])
                    )

        print(f"Zapisano sensory i pomiary dla stacji ID {station_id}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    print("Tworzenie tabel...")
    create_tables()
    print("Tabele utworzone.")
    print("Pobieranie i zapisywanie danych...")
    save_data()
    print("Gotowe – baza zawiera pełne dane.")