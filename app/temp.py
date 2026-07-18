
from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE temperatures
ADD COLUMN batterie INTEGER
""")

conn.commit()
conn.close()

print("Colonne batterie ajoutée")
