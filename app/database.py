
import sqlite3

DB_PATH = "database/maison.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            piece TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidite REAL NOT NULL,
            date_mesure TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    conn.commit()
    conn.close()


def add_temperature(piece, temperature,humidite):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO temperatures (
            piece,
            temperature,
            humidite
        )
        VALUES (?, ?, ?)
    """, (piece, temperature, humidite))


    conn.commit()
    conn.close()


def get_temperatures():
    conn = get_connection()
    cursor = conn.cursor()



    cursor.execute("""
        SELECT
            id,
            piece,
            temperature,
            humidite,
            date_mesure
        FROM temperatures
        ORDER BY date_mesure DESC
    """)



    rows = cursor.fetchall()

    conn.close()

    return rows


def get_temperatures_by_date(selected_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            piece,
            temperature,
            humidite,
            date_mesure
        FROM temperatures
        WHERE DATE(date_mesure) = ?
        ORDER BY date_mesure
    """, (selected_date,))

    rows = cursor.fetchall()

    conn.close()

    return rows

