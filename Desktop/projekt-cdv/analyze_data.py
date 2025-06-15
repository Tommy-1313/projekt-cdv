"""
Moduł do analizy statystycznej danych pomiarowych z GIOŚ.
Autor: Tomek Łukasiewicz
"""

import requests
import statistics

BASE_URL = "https://api.gios.gov.pl/pjp-api/rest"


def get_sensors_for_station(station_id):
    """
    Pobierz listę sensorów dla podanej stacji.
    """
    url = f"{BASE_URL}/station/sensors/{station_id}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []


def get_data_for_sensor(sensor_id):
    """
    Pobierz dane pomiarowe z konkretnego sensora.
    """
    url = f"{BASE_URL}/data/getData/{sensor_id}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}


def analyze(values):
    """
    Analizuj dane: średnia, minimum, maksimum.
    """
    values = [
        (v['value'], v['date']) for v in values if v['value'] is not None
    ]

    if not values:
        print("Brak danych pomiarowych.")
        return

    only_values = [v[0] for v in values]
    avg = round(statistics.mean(only_values), 2)
    min_val, min_date = min(values)
    max_val, max_date = max(values)

    print(f"Średnia: {avg}")
    print(f"Min: {min_val} ({min_date})")
    print(f"Max: {max_val} ({max_date})")


if __name__ == "__main__":
    station_id = 114  # <- Możesz zmienić na dowolny ID
    sensors = get_sensors_for_station(station_id)

    if not sensors:
        print("Brak sensorów dla tej stacji.")
    else:
        sensor = sensors[0]
        print(f"Analiza parametru: {sensor['param']['paramName']}")
        data = get_data_for_sensor(sensor['id'])
        analyze(data.get("values", []))