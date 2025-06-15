"""
Interfejs graficzny aplikacji do analizy danych GIOŚ.
Autor: Tomek Łukasiewicz
"""

import tkinter as tk
from tkinter import ttk, messagebox
from dodatek import (
    filter_by_city,
    filter_by_location,
    analyze_all_sensors_for_station,
)
from plot_all import plot_all_for_station
from generate_map import generate_map


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("GIOŚ – Analiza powietrza")
        self.root.geometry("600x400")

        # Tryb filtrowania
        self.filter_type = tk.StringVar(value="city")

        # Ramka wyboru trybu
        mode_frame = tk.LabelFrame(root, text="Metoda filtrowania")
        mode_frame.pack(pady=10, fill="x", padx=10)

        tk.Radiobutton(
            mode_frame, text="Po mieście",
            variable=self.filter_type, value="city"
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            mode_frame, text="Po promieniu (adres + km)",
            variable=self.filter_type, value="location"
        ).pack(side="left", padx=10)

        # Wejścia
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Miasto / Adres:").grid(
            row=0, column=0, sticky="e"
        )
        self.address_entry = tk.Entry(input_frame, width=40)
        self.address_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Promień (km):").grid(
            row=1, column=0, sticky="e"
        )
        self.radius_entry = tk.Entry(input_frame, width=10)
        self.radius_entry.grid(row=1, column=1, sticky="w")
        self.radius_entry.insert(0, "10")

        # Lista stacji
        list_frame = tk.Frame(root)
        list_frame.pack(pady=10)

        tk.Label(list_frame, text="Wybierz stację:").pack()
        self.stations_box = ttk.Combobox(
            list_frame, width=60, state="readonly"
        )
        self.stations_box.pack()

        # Przycisk szukania
        search_btn = tk.Button(
            root, text="Szukaj stacji", command=self.search_stations
        )
        search_btn.pack(pady=5)

        # Przycisk mapki
        map_btn = tk.Button(
            root, text="Pokaż mapę stacji", command=self.show_map
        )
        map_btn.pack(pady=5)

        # Przycisk analizy
        analyze_btn = tk.Button(
            root, text="Generuj wykresy", command=self.run_analysis
        )
        analyze_btn.pack(pady=5)

    def search_stations(self):
        filt = self.filter_type.get()
        addr = self.address_entry.get().strip()
        radius = self.radius_entry.get().strip()

        if not addr:
            messagebox.showerror(
                "Błąd", "Wpisz nazwę miasta lub adres."
            )
            return

        if filt == "city":
            stations = filter_by_city(addr)
        else:
            try:
                radius_val = float(radius)
            except ValueError:
                radius_val = 10.0
            stations = filter_by_location(addr, radius_val)

        if not stations:
            messagebox.showinfo(
                "Brak wyników", "Nie znaleziono stacji."
            )
            return

        self.station_map = {
            f"{s[1]} – {s[2]}" if len(s) == 3
            else f"{s[1]} – {s[2]} ({s[3]} km)": s[0]
            for s in stations
        }

        self.stations_box["values"] = list(self.station_map.keys())
        self.stations_box.current(0)

    def run_analysis(self):
        selected = self.stations_box.get()
        if not selected:
            messagebox.showwarning(
                "Uwaga", "Wybierz stację."
            )
            return

        station_id = self.station_map[selected]
        plot_all_for_station(station_id)
        analyze_all_sensors_for_station(station_id)

        messagebox.showinfo(
            "Gotowe", "Wykresy zostały wygenerowane i zapisane!"
        )

    def show_map(self):
        generate_map()


# --- Start aplikacji ---
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()