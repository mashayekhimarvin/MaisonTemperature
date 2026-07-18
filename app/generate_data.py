
from database import get_connection

from datetime import datetime, timedelta

import random
import math


def temp_exterieur(current):

    heure = current.hour + current.minute / 60

    base = 15 + 8 * math.sin(
        (heure - 6) * math.pi / 12
    )

    bruit = random.uniform(-0.5, 0.5)

    return round(base + bruit, 1)


def temp_salon(current):

    ext = temp_exterieur(current)

    temperature = 21 + (ext - 15) * 0.15

    bruit = random.uniform(-0.2, 0.2)

    return round(temperature + bruit, 1)


def temp_chambre(current):

    ext = temp_exterieur(current)

    temperature = 19.5 + (ext - 15) * 0.10

    bruit = random.uniform(-0.2, 0.2)

    return round(temperature + bruit, 1)


def humidity(current):

    heure = current.hour + current.minute / 60

    base = 50

    variation = 5 * math.sin(
        heure * math.pi / 12
    )

    bruit = random.uniform(-2, 2)

    return round(base + variation + bruit, 1)


conn = get_connection()
cursor = conn.cursor()


cursor.execute("DELETE FROM temperatures")


pieces = [
    "Exterieur",
    "Salon",
    "Chambre"
]


debut = datetime.now() - timedelta(days=7)

courant = debut


while courant <= datetime.now():

    for piece in pieces:

        if piece == "Exterieur":
            temperature = temp_exterieur(courant)

        elif piece == "Salon":
            temperature = temp_salon(courant)

        elif piece == "Chambre":
            temperature = temp_chambre(courant)

        humidite = humidity(courant)

        cursor.execute("""
            INSERT INTO temperatures
            (
                piece,
                temperature,
                humidite,
                date_mesure
            )
            VALUES (?, ?, ?, ?)
        """, (
            piece,
            temperature,
            humidite,
            courant.strftime("%Y-%m-%d %H:%M:%S")
        ))

    courant += timedelta(minutes=5)


conn.commit()
conn.close()

print("Données réalistes générées avec succès")
