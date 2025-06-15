"""
Testy jednostkowe API GIOŚ – pobieranie danych i prosta analiza.
Autor: Tomek Łukasiewicz
"""

import requests
import pytest
from statistics import mean

BASE_URL = "https://api.gios.gov.pl/pjp-api/rest"


def test_api_station_list():
    """Test: pobranie listy stacji"""
    response = requests.get(f"{BASE_URL}/station/findAll")
    assert response.status_code == 200
    stations = response.json()
    assert isinstance(stations, list)
    assert len(stations) > 0


def test_api_sensor_for_station():
    """Test: pobranie sensorów dla konkretnej stacji"""
    station_id = 400  # Możesz zmienić na inny znany ID
    response = requests.get(f"{BASE_URL}/station/sensors/{station_id}")
    assert response.status_code == 200
    sensors = response.json()
    assert isinstance(sensors, list)
    assert len(sensors) > 0


def test_data_analysis_sample():
    """Test: analiza danych PM10 – min, max, średnia"""
    sensor_id = 5503  # np. PM10 z Krakowa
    response = requests.get(f"{BASE_URL}/data/getData/{sensor_id}")
    assert response.status_code == 200
    data = response.json()
    values = [
        v["value"] 
        for v in data.get("values", []) 
        if v["value"] is not None
    ]
    assert isinstance(values, list)
    if not values:
        pytest.skip(
            "Brak danych pomiarowych – sensor działa ale chwilowo bez wyników."
        )
    assert min(values) <= mean(values) <= max(values)