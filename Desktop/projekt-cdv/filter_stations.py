"""
Filtrowanie stacji GIOŚ po mieście i promieniu geograficznym.
Autor: Tomek Łukasiewicz
"""

import sqlite3
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def filter_by_city(city_name):
    """
    Zwróć listę stacji, których miasto zawiera fragment city_name.
    """
    conn = sqlite3.connect("stations.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM stations WHERE city LIKE ?",
        ('%' + city_name + '%',),
    )
    results = cursor.fetchall()
    conn.close()
    return results


def filter_by_location(center_address, radius_km):
    """
    Zwróć stacje znajdujące się w zadanym promieniu od adresu.
    """
    geolocator = Nominatim(user_agent="cdv_app")
    location = geolocator.geocode(center_address)

    if not location:
        print("Nie znaleziono adresu.")
        return []

    center_point = (location.latitude, location.longitude)

    conn = sqlite3.connect("stations.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT stationName, city, latitude, longitude FROM stations"
    )
    all_stations = cursor.fetchall()
    conn.close()

    nearby = []
    for name, city, lat, lon in all_stations:
        dist = geodesic(center_point, (float(lat), float(lon))).km
        if dist <= radius_km:
            nearby.append((name, city, round(dist, 2)))

    return sorted(nearby, key=lambda x: x[2])


if __name__ == "__main__":
    print("=== Filtrowanie po mieście: Poznań ===")
    results = filter_by_city("Poznań")
    for r in results:
        print(f"{r[1]} – {r[2]}")

    print("\n=== Filtrowanie po lokalizacji: Collegium Da Vinci, 20 km ===")
    results = filter_by_location("Collegium Da Vinci, Poznań", 20)
    for name, city, dist in results:
        print(f"{name} – {city} ({dist} km)")