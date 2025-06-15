"""
Generowanie interaktywnej mapy stacji GIOŚ w folium.
Autor: Tomek Łukasiewicz
"""

import sqlite3
import folium
import webbrowser
import os


def generate_map():
    """
    Generuj mapę z wszystkimi stacjami z bazy danych i otwórz w przeglądarce.
    """
    conn = sqlite3.connect("stations.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT stationName, latitude, longitude, city FROM stations"
    )
    stations = cursor.fetchall()
    conn.close()

    if not stations:
        print("Nie znaleziono stacji.")
        return

    mapa = folium.Map(location=[52.0, 19.0], zoom_start=6)

    for name, lat, lon, city in stations:
        folium.Marker(
            location=[float(lat), float(lon)],
            popup=f"{name} ({city})",
            icon=folium.Icon(color="blue", icon="cloud"),
        ).add_to(mapa)

    filename = "mapa.html"
    mapa.save(filename)
    print(f"Mapa zapisana jako: {filename}")

    webbrowser.open(f"file://{os.path.abspath(filename)}")


if __name__ == "__main__":
    generate_map()