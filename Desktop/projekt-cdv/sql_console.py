import sqlite3

conn = sqlite3.connect("stations.db")
cursor = conn.cursor()

print("💡 Interaktywny tryb zapytań SQL do stations.db")
print("Wpisz zapytanie SQL (lub 'exit' aby zakończyć)\n")

while True:
    query = input("sqlite> ")
    if query.lower() in ["exit", "quit"]:
        break
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except Exception as e:
        print("❌ Błąd:", e)

conn.close()
print("Zakończono.")