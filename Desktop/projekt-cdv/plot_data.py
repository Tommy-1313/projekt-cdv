"""
Generowanie wykresu dla wybranego sensora i parametru (np. PM10).
Autor: Tomek Łukasiewicz
"""

import os
import requests
import matplotlib.pyplot as plt
from datetime import datetime

BASE_URL = "https://api.gios.gov.pl/pjp-api/rest"


def get_sensors_for_station(station_id):
    """
    Zwróć listę sensorów dla danej stacji.
    """
    url = f"{BASE_URL}/station/sensors/{station_id}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []


def get_data_for_sensor(sensor_id):
    """
    Zwróć dane pomiarowe z konkretnego sensora.
    """
    url = f"{BASE_URL}/data/getData/{sensor_id}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}


def plot_sensor_data(sensor_id, param_name):
    """
    Tworzy wykres pomiarów dla jednego sensora.
    """
    data = get_data_for_sensor(sensor_id)
    values = [
        (v["date"], v["value"])
        for v in data.get("values", [])
        if v["value"] is not None
    ]

    if not values:
        print("Brak danych do wykresu.")
        return

    print(f"Pobrano {len(values)} pomiarów dla {param_name}")
    print("Przykładowe dane:", values[:3])

    dates = [
        datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d, _ in values
    ]
    measurements = [v for _, v in values]

    plt.figure(figsize=(10, 5))
    plt.plot(
        dates, measurements,
        marker="o", linestyle="-", color="blue"
    )
    plt.title(f"Pomiar: {param_name}")
    plt.xlabel("Data i godzina")
    plt.ylabel("Wartość")
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)

    folder = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(folder, f"wykres_{param_name}.png")
    print("Ścieżka do zapisu:", filename)

    plt.savefig(filename)
    plt.show()
    print(f"Wykres zapisany jako: {filename}")


if __name__ == "__main__":
    station_id = 400

    sensors = get_sensors_for_station(station_id)

    if not sensors:
        print("Brak sensorów.")
    else:
        print("Dostępne sensory:")
        for s in sensors:
            print(
                f"- {s['param']['paramName']} "
                f"({s['param']['paramCode']})"
            )

        for sensor in sensors:
            if sensor['param']['paramCode'] == "PM10":
                sensor_id = sensor['id']
                param_name = sensor['param']['paramName']
                plot_sensor_data(sensor_id, param_name)
                break