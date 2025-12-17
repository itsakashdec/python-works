from flask import Flask, render_template

app = Flask(__name__)

cafes = [
    {
        "name": "Cafe Mocha",
        "location": "Chennai",
        "wifi": "Yes",
        "power": "Yes",
        "rating": "4.5"
    },
    {
        "name": "Brew Hub",
        "location": "Bangalore",
        "wifi": "Yes",
        "power": "No",
        "rating": "4.0"
    },
    {
        "name": "Work & Coffee",
        "location": "Hyderabad",
        "wifi": "Yes",
        "power": "Yes",
        "rating": "4.8"
    }
]

@app.route("/")
def home():
    return render_template("index.html", cafes=cafes)

if __name__ == "__main__":
    app.run(debug=True)
