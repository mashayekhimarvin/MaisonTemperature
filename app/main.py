

from flask import Flask, render_template, request
from database import (get_temperatures_by_date,has_data_for_date)
from datetime import datetime, timedelta


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
    series = {}
    humidity_series = {}

    for t in temperatures:

        piece = t[1]
        temperature = t[2]
        humidite = t[3]
        heure = t[5][11:16]

        if piece not in series:
            series[piece] = []

        # On utilise le Salon comme référence horaire
        
        if heure not in labels:
            labels.append(heure)

        
        if piece not in humidity_series:
            humidity_series[piece] = []


        series[piece].append(temperature)
        humidity_series[piece].append(humidite)

    print("Labels :", len(labels))

    for piece, valeurs in series.items():
        print(piece, len(valeurs))

    
    print(temperatures[0])
    print(labels[:5])

    return render_template(
        "index.html",
        temperatures=temperatures,
        series=series,
        humidity_series=humidity_series,
        labels=labels,
        selected_date=selected_date,
        previous_day=previous_day,
        next_day=next_day,
        has_previous_day=has_previous_day,
        has_next_day=has_next_day
    )



    # for t in temperatures:
    #     labels.append(t[4])
    #     valeurs_temperature.append(t[2])

    # return render_template(
    #     "index.html",
    #     temperatures=temperatures,
    #     labels=labels,
    #     valeurs_temperature=valeurs_temperature
    # )


if __name__ == "__main__":
    app.run(debug=True)


from database import (
    get_temperatures_by_date,
    has_data_for_date
)
