

from flask import Flask, render_template, request, jsonify
from database import (get_temperatures_by_date,has_data_for_date,add_temperature,init_db)
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def utc_to_paris(date_str):

    dt = datetime.strptime(
        date_str,
        "%Y-%m-%d %H:%M:%S"
    )

    dt = dt.replace(
        tzinfo=ZoneInfo("UTC")
    )

    return dt.astimezone(
        ZoneInfo("Europe/Paris")
    )

init_db()
app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

@app.route("/")
def home():
    selected_date = request.args.get(
        "date",
        datetime.now().strftime("%Y-%m-%d")
    )

    temperatures = get_temperatures_by_date(
        selected_date
    )
    

    current_day = datetime.strptime(
        selected_date,
        "%Y-%m-%d"
    )

    previous_day = (
        current_day - timedelta(days=1)
    ).strftime("%Y-%m-%d")

    next_day = (
        current_day + timedelta(days=1)
    ).strftime("%Y-%m-%d")
   

    has_previous_day = has_data_for_date(
        previous_day
    )

    has_next_day = has_data_for_date(
        next_day
    )



    labels = []
    timeline = {}
    pieces = set()

    for t in temperatures:
      
        piece = t[1]
        temperature = t[2]
        humidite = t[3]


        date_mesure = utc_to_paris(t[5])

        heure = date_mesure.strftime("%H:%M")



        pieces.add(piece)

        if heure not in timeline:

            timeline[heure] = {}

            labels.append(heure)

        timeline[heure][piece] = {
            "temperature": temperature,
            "humidite": humidite
        }

    series = {}
    humidity_series = {}

    for piece in pieces:

        series[piece] = []
        humidity_series[piece] = []

        for heure in labels:

            if (
                heure in timeline
                and piece in timeline[heure]
            ):

                series[piece].append(
                    timeline[heure][piece]["temperature"]
                )

                humidity_series[piece].append(
                    timeline[heure][piece]["humidite"]
                )

            else:

                series[piece].append(None)
                humidity_series[piece].append(None)


    
    temperatures_data = []
    humidites_data = []

    last_measures = {}

    for t in temperatures:

        temperatures_data.append(t[2])

        if t[3] is not None:
            humidites_data.append(t[3])



        date_mesure = utc_to_paris(t[5])
        

        delta = (datetime.now(ZoneInfo("Europe/Paris"))
            - date_mesure)


        minutes = int(delta.total_seconds() / 60)

        if minutes <= 0:

            last_seen = "à l'instant"

        elif minutes == 1:

            last_seen = "il y a 1 minute"

        elif minutes < 60:

            last_seen = f"il y a {minutes} minutes"

        else:

            heures = minutes // 60

            if heures == 1:
                last_seen = "il y a 1 heure"
            else:
                last_seen = f"il y a {heures} heures"


        last_measures[t[1]] = {
            "temperature": t[2],
            "humidite": t[3],
            "batterie": t[4],
            "date": t[5],
            "last_seen": last_seen
        }


    


    if not temperatures_data:

        return render_template(
            "index.html",
            series={},
            humidity_series={},
            labels=[],
            selected_date=selected_date,
            previous_day=previous_day,
            next_day=next_day,
            has_previous_day=has_previous_day,
            has_next_day=has_next_day,
            temp_min=0,
            temp_max=0,
            humidite_min=0,
            humidite_max=0,
            last_measures={},
            daily_summary={}
        )



    temp_min = min(temperatures_data)
    temp_max = max(temperatures_data)



    humidite_min = min(humidites_data)
    humidite_max = max(humidites_data)

    daily_summary = {}

    
    for piece, valeurs in series.items():

        humidites = humidity_series[piece]


        valeurs_valides = [
            v for v in valeurs
            if v is not None
        ]

        humidites_valides = [
            h for h in humidites
            if h is not None
        ]

        daily_summary[piece] = {
            "temp_min": min(valeurs_valides),
            "temp_max": max(valeurs_valides),
            "hum_min": min(humidites_valides),
            "hum_max": max(humidites_valides)
        }


    for piece, valeurs in series.items():

        print(
            piece,
            len(valeurs)
        )


    return render_template(
        "index.html",
        series=series,
        humidity_series=humidity_series,
        labels=labels,
        selected_date=selected_date,
        previous_day=previous_day,
        next_day=next_day,
        has_previous_day=has_previous_day,
        has_next_day=has_next_day,

        
        temp_min=temp_min,
        temp_max=temp_max,

        humidite_min=humidite_min,
        humidite_max=humidite_max,

        last_measures=last_measures,

        daily_summary=daily_summary

    )

@app.route(
    "/api/measurement",
    methods=["POST"]
)
def receive_measurement():

    data = request.get_json()

    piece = data["piece"]
    temperature = data["temperature"]
    humidite = data["humidite"]
    batterie = data["batterie"]
    

    add_temperature(
        piece,
        temperature,
        humidite,
        batterie
    )




    print("")
    print("=== MESURE ENREGISTREE ===")
    print(
        f"{piece} | "
        f"{temperature}°C | "
        f"{humidite}%  | "
        f"{batterie}%"
    )

    return jsonify({
        "status": "ok"
    })


if __name__ == "__main__": 
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

