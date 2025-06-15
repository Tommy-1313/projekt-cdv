import sqlite3

conn = sqlite3.connect("stations.db")
cursor = conn.cursor()

cursor.execute(
    "SELECT id, stationName, city FROM stations WHERE city LIKE '%Poznań%'"
)
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()