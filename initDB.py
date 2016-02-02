import sqlite3

conn = sqlite3.connect("twatter.db")
c = conn.cursor()
c.execute('''CREATE TABLE twats
			(content text, time bigint)''')

conn.commit()
conn.close()
