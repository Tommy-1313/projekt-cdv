"""
Moduł pomocniczy do filtrowania, pobierania i analizy danych GIOŚ.
Autor: Tomek Łukasiewicz
"""

import sqlite3
import requests
import statistics
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

BASE_URL = "https://api.gios.gov.pl/pjp-api/rest"


def filter_by_city(city_name):
    """Zwróć stacje zawierające nazwę miasta."""
    conn = sqlite3.connect("stations.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, stationName, city FROM stations WHERE city LIKE ?",
        ('%' + city_name + '%',),
    )
    results = cursor.fetchall()
    conn.close()
    return results


def filter_by_location(center_address, radius_km):
    """Zwróć stacje w promieniu od adresu."""
    geolocator = Nominatim(user_agent="cdv_app")
    location = geolocator.geocode(center_address)

    if not location:
        print("Nie znaleziono adresu.")
        return []

    center_point = (location.latitude, location.longitude)

    conn = sqlite3.connect("stations.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, stationName, city, latitude, longitude FROM stations"
    )
    all_stations = cursor.fetchall()
    conn.close()

    nearby = []
    for sid, name, city, lat, lon in all_stations:
        dist = geodesic(center_point, (float(lat), float(lon))).km
        if dist <= radius_km:
            nearby.append((sid, name, city, round(dist, 2)))

    return sorted(nearby, key=lambda x: x[3])


def get_sensors_for_station(station_id):
    """Zwróć sensory dla podanej stacji."""
    url = f"{BASE_URL}/station/sensors/{station_id}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []


def get_data_for_sensor(sensor_id):
    """Zwróć dane pomiarowe z sensora."""
    url = f"{BASE_URL}/data/getData/{sensor_id}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}


def analyze(values):
    """Analiza: średnia, min, max z datami."""
    values = [
        (v['value'], v['date']) for v in values if v['value'] is not None
    ]

    if not values:
        print("  Brak danych pomiarowych.")
        return

    only_values = [v[0] for v in values]
    avg = round(statistics.mean(only_values), 2)
    min_val, min_date = min(values, key=lambda x: x[0])
    max_val, max_date = max(values, key=lambda x: x[0])

    print(f"  Średnia: {avg}")
    print(f"  Min: {min_val} ({min_date})")
    print(f"  Max: {max_val} ({max_date})")


def analyze_all_sensors_for_station(station_id):
    """Przeanalizuj wszystkie sensory danej stacji."""
    print(f"\nAnaliza dla stacji ID: {station_id}")
    sensors = get_sensors_for_station(station_id)

    if not sensors:
        print("Brak sensorów dla tej stacji.")
        return

    for sensor in sensors:
        param_name = sensor['param']['paramName']
        sensor_id = sensor['id']
        print(f"\nParametr: {param_name} (sensor ID: {sensor_id})")
        data = get_data_for_sensor(sensor_id)
        analyze(data.get("values", []))


def choose_filter_method():
    """Wybierz metodę filtrowania."""
    print("Wybierz metodę filtrowania stacji:")
    print("1 - Filtrowanie po mieście")
    print("2 - Filtrowanie po promieniu geograficznym")
    choice = input("Twój wybór (1 lub 2): ")

    while choice not in ('1', '2'):
        print("Niepoprawny wybór, spróbuj jeszcze raz.")
        choice = input("Twój wybór (1 lub 2): ")

    return choice


def select_stations(stations):
    """Pozwól użytkownikowi wybrać stacje do analizy."""
    if not stations:
        print("Brak stacji do wyboru.")
        return []

    print("\nZnalezione stacje:")
    for idx, st in enumerate(stations, start=1):
        if len(st) == 3:
            sid, name, city = st
            print(f"{idx}. {name} - {city} (ID: {sid})")
        else:
            sid, name, city, dist = st
            print(
                f"{idx}. {name} - {city} (ID: {sid}, odległość: {dist} km)"
            )

    print(
        "\nWybierz numer(y) stacji do analizy "
        "(oddziel przecinkiem, max 3):"
    )
    choices = input()
    try:
        indices = [int(i.strip()) for i in choices.split(",") if i.strip()]
    except ValueError:
        print("Błędny format wyboru.")
        indices = []

    indices = [i for i in indices if 1 <= i <= len(stations)]

    if not indices:
        print("Nie wybrano żadnej prawidłowej stacji.")
        return []

    if len(indices) > 3:
        print("Możesz wybrać maksymalnie 3 stacje. Biorę pierwsze 3.")
        indices = indices[:3]

    selected = [stations[i - 1][0] for i in indices]
    return selected


def main():
    """Główna funkcja CLI do filtrowania i analizy."""
    method = choose_filter_method()

    if method == '1':
        city = input("Podaj nazwę miasta: ")
        stations = filter_by_city(city)
    else:
        addr = input("Podaj adres centrum: ")
        radius = input("Podaj promień w km: ")
        try:
            radius = float(radius)
        except ValueError:
            print("Niepoprawna wartość promienia, ustawiam na 10 km.")
            radius = 10.0
        stations = filter_by_location(addr, radius)

    if not stations:
        print("Nie znaleziono żadnych stacji.")
        return

    selected_station_ids = select_stations(stations)

    if not selected_station_ids:
        print("Nie wybrano stacji do analizy.")
        return

    for sid in selected_station_ids:
        analyze_all_sensors_for_station(sid)


if __name__ == "__main__":
    main()