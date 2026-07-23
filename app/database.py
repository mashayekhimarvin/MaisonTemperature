
import sqlite3

DB_PATH = "database/maison.db"


def get_connection():
    return sqlite3.connect(DB_PATH)

def get_last_battery(piece):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT batterie
        FROM temperatures
        WHERE piece = ?
        AND batterie != -1
        ORDER BY date_mesure DESC
        LIMIT 1
    """, (piece,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


def has_data_for_date(date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM temperatures
        WHERE DATE(date_mesure) = ?
    """, (date,))

    count = cursor.fetchone()[0]

    conn.close()

    return count > 0

def init_db():
    conn = get_connection()
    cursor = conn.cursor()



    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            piece TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidite REAL NOT NULL,
            batterie INTEGER,
            date_mesure TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)



    conn.commit()
    conn.close()


def add_temperature(piece, temperature,humidite,batterie):
    if batterie == -1:

        derniere_batterie = get_last_battery(
            piece
        )

        if derniere_batterie is not None:
            batterie = derniere_batterie


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO temperatures (
            piece,
            temperature,
            humidite,
            batterie
        )
        VALUES (?, ?, ?, ?)
    """, (piece, temperature, humidite,batterie))


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
            batterie,       
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
            batterie,
            date_mesure
        FROM temperatures
        WHERE DATE(date_mesure) = ?
        ORDER BY date_mesure
    """, (selected_date,))

    rows = cursor.fetchall()

    conn.close()

    return rows




