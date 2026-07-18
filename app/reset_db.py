from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("DELETE FROM temperatures")

conn.commit()
conn.close()

print("Base vidée")

