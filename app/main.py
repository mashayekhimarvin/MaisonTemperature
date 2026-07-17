
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
    
    labels = []
    valeurs_temperature = []

    for t in temperatures:
        labels.append(t[4])
        valeurs_temperature.append(t[2])

    return render_template(
        "index.html",
        temperatures=temperatures,
        labels=labels,
        valeurs_temperature=valeurs_temperature
    )


if __name__ == "__main__":
    app.run(debug=True)
