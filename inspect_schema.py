import sqlite3
conn = sqlite3.connect('Code/ProjetBdd1.db')
c = conn.cursor()
c.execute('PRAGMA table_info(produits)')
rows = c.fetchall()
for row in rows:
    print(row)
conn.close()