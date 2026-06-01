from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    project = {
        "name": "Welcome to Food Club planner",
        "description": "This project is designed to help you plan your meals and manage your food club activities.",
        "status": "In Development",
    }

    return render_template("index.html", project=project)
@app.route("/foodclub")
def foodclub():
    food = {
        "name": "Food Club",
        "description": "A platform to organize and manage your food club activities.",
        "features": [
            "Event scheduling",
            "Member management"
        ],
    }
    return render_template("foodclub.html", food = food)

if __name__ == "__main__":
    app.run(debug=True)