import sqlite3

conn = sqlite3.connect(r'logs.db')

cursor = conn.cursor()

sql = 'select * from logs'

cursor.execute(sql)

results = cursor.fetchall()

for row in results:
    print(f"[{row[1]}] {row[2]}")