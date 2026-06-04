from flask import Flask, render_template, request
import sqlalchemy as db
from sqlalchemy import text
import requests

app = Flask(__name__)
target_database = "postgresql://postgres:postgres@localhost/madklub"
database = db.create_engine(target_database)
conn = database.connect()

@app.route("/")
def home():
    project = {
        "name": "Welcome to Food Club planner",
        "description": "This project is designed to help you plan your meals and manage your food club activities.",
        "status": "In Development",
    }

    return render_template("index.html", project=project)
@app.route("/foodclub/", methods = ['GET', 'POST'])
def foodclub():
    if request.method == "POST":
        menu = request.form.get("menu") 
        close_at = request.form.get("close_at") 
        start_at = request.form.get("start_at") 
        vege = request.form.get("vege")
        if vege == "on":
            vege = True
        else:
            vege = False
        vegan = request.form.get("vegan")
        if vegan == "on":
            vegan = True
        else:
            vegan = False
        print("Adding to database")
        conn.execute(text("""
                          INSERT INTO madklub (id, beboer_id, menu, close_at, start_at, vege, vegan, price, picture)
                          VALUES (:id, :beboer_id, :menu, :close_at, :start_at, :vege, :vegan, :price, :picture)
                          """),
                          {
                             "id": 2, 
                             "beboer_id": 1, 
                             "menu": menu,
                             "close_at": close_at,
                             "start_at": start_at,
                             "vege": vege,
                             "vegan": vegan,
                             "price": 100000,
                             "picture": "somethingbla" 
                          }
                          )
        conn.commit()
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