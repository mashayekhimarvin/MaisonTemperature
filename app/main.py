

from flask import Flask, render_template, request
from database import get_temperatures_by_date
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
   
    labels = []
    series = {}

    for t in temperatures:

        piece = t[1]
        temperature = t[2]
        heure = t[4][11:16]

        if piece not in series:
            series[piece] = []

        # On utilise le Salon comme référence horaire
        if piece == "Salon":
            labels.append(heure)

        series[piece].append(temperature)

    print("Labels :", len(labels))

    for piece, valeurs in series.items():
        print(piece, len(valeurs))

    
    return render_template(
        "index.html",
        temperatures=temperatures,
        series=series,
        labels=labels,
        selected_date=selected_date,
        previous_day=previous_day,
        next_day=next_day
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
