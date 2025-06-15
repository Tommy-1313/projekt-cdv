# Projekt: Analiza jakości powietrza – CDV

Projekt inżynierski realizowany w ramach studiów podyplomowych na kierunku - Akademia Programowania w Pythonie, Collegium Da Vinci.  
Aplikacja desktopowa pozwala na pobieranie, filtrowanie, analizowanie i wizualizację danych o jakości powietrza pochodzących z publicznego API GIOŚ.

---

## Funkcjonalności

- Filtrowanie stacji po nazwie miasta lub promieniu geograficznym (geolokalizacja)
- Pobieranie danych z API GIOŚ (PM10, PM2.5, SO2, NO2, CO itd.)
- Zapis danych do lokalnej bazy danych SQLite (stations, sensors, measurements)
- Wykresy pomiarów z trendem (regresja liniowa)
- Statystyki: min, max, średnia + data wystąpienia
- Mapa wszystkich stacji pomiarowych z użyciem folium
- Testy jednostkowe z pytest
- Interfejs graficzny (GUI) zbudowany w Tkinter

---

## Technologie

- requests
- matplotlib
- folium
- geopy
- numpy
- pytest


## Jak uruchomić projekt

1. Sklonuj repozytorium:

"""
git clone https://github.com/Tommy-1313/projekt-cdv.git
cd projekt-cdv

2. Utwórz środowisko wirtualne:

python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt

3. Uruchom aplikacje:

python app_gui.py

4. Jak uruchomić testy:

pytest

5. Mapa

W aplikacji kliknij „Pokaż mapę stacji” – otworzy się mapa Polski w przeglądarce, z zaznaczonymi wszystkimi stacjami pomiarowymi z bazy danych.

6. Autor

Tomasz Łukasiewicz
Colegium Da Vinci, Poznań
Studia podyplomowe - Akademia Programowania w Pythonie ~ 2025