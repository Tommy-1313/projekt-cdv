import sqlite3

conn = sqlite3.connect("stations.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM stations")
count = cursor.fetchone()[0]

print(f"W bazie danych znajduje się {count} stacji.")

conn.close()