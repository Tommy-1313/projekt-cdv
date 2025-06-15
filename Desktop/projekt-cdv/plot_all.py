"""
Moduł generujący wykresy pomiarów i linię trendu dla stacji GIOŚ.
Autor: Tomek Łukasiewicz
"""

import os
import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

BASE_URL = "https://api.gios.gov.pl/pjp-api/rest"


def get_sensors_for_station(station_id):
    """
    Zwróć listę sensorów dla podanej stacji.
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
    Tworzy wykres pomiarów dla sensora z linią trendu.
    """
    data = get_data_for_sensor(sensor_id)
    values = [
        (v["date"], v["value"])
        for v in data.get("values", [])
        if v["value"] is not None
    ]

    if not values:
        print(f"Brak danych do wykresu: {param_name}")
        return

    print(f"{param_name} – {len(values)} pomiarów")

    # Przetwarzanie dat i wartości
    dates = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d, _ in values]
    measurements = [v for _, v in values]

    # Regresja liniowa
    x_numeric = mdates.date2num(dates)
    y = np.array(measurements)
    a, b = np.polyfit(x_numeric, y, 1)
    trendline = a * x_numeric + b

    # Tworzenie wykresu
    plt.figure(figsize=(12, 5))
    plt.plot(
        dates, measurements,
        marker="o", linestyle="-", label="Pomiar", color="darkblue"
    )
    plt.plot(
        dates, trendline,
        linestyle="--", label="Trend", color="red"
    )
    plt.title(f"Pomiar: {param_name}")
    plt.xlabel("Data i godzina")
    plt.ylabel("Wartość")
    plt.grid(True)
    plt.tight_layout()

    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%Y-%m-%d %H:%M")
    )
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=6))
    plt.xticks(rotation=45)
    plt.legend()

    folder = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(folder, f"wykres_{param_name}.png")
    plt.savefig(filename)
    plt.close()
    print(f"Zapisano wykres: {filename}")


def plot_all_for_station(station_id):
    """
    Generuj wykresy dla wszystkich sensorów danej stacji.
    """
    print(f"\nGeneruję wykresy dla stacji ID: {station_id}")
    sensors = get_sensors_for_station(station_id)

    if not sensors:
        print("Brak sensorów dla tej stacji.")
        return

    for sensor in sensors:
        param_name = sensor['param']['paramName']
        sensor_id = sensor['id']
        plot_sensor_data(sensor_id, param_name)


if __name__ == "__main__":
    station_id = 400  # <- zmień na dowolny ID stacji
    plot_all_for_station(station_id)