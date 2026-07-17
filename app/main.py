
from flask import Flask, render_template
from database import get_temperatures

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

@app.route("/")
def home():
    temperatures = get_temperatures()
    print("=== CONTENU SQLITE ===")
    for t in temperatures:
        print(t)

    
    labels = []
    valeurs_temperature = []
    salon = []
    chambre = []
    cuisine = []


    for t in temperatures:

        piece = t[1]
        temperature = t[2]
        labels.append(t[4])
        valeurs_temperature.append(t[2])

        if piece == "Salon":
            salon.append(temperature)

        elif piece == "Chambre":
            chambre.append(temperature)

        elif piece == "Cuisine":
            cuisine.append(temperature)


    
    return render_template(
        "index.html",
        temperatures=temperatures,
        salon=salon,
        chambre=chambre,
        cuisine=cuisine
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
