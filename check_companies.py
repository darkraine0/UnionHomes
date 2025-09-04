import sqlite3

conn = sqlite3.connect('homes.db')
cursor = conn.cursor()
cursor.execute('SELECT DISTINCT company FROM plans')
print('All companies:')
for row in cursor.fetchall():
    print(f'  - {row[0]}')

print('\nEdgewater companies:')
cursor.execute('SELECT DISTINCT company FROM plans WHERE community = "Edgewater"')
for row in cursor.fetchall():
    print(f'  - {row[0]}')
conn.close()
