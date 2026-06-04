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

@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        salt = "497hg4"
        ##ADD SALT TO HASHED PASSWORD
        role = request.form.get("role")
        ##Beboer
        beboer_id = None
        if role == "beboer":
            name = request.form.get("name")
            room = request.form.get("room_number")
            result = conn.execute(text("""
                        INSERT INTO beboer (name, room_number, madklub_taken, amount_cleanings, cleanings_done)
                              VALUES (:name, :room_number, :madklub_taken, :amount_cleanings, :cleanings_done)
                              """),
                              {
                                  "name": name,
                                  "room_number": room,
                                  "madklub_taken": False,
                                  "amount_cleanings": 2,
                                  "cleanings_done": 0
                              })
            print("Beboer created!!")
            beboer_id = result.scalar()
            print("Creating a new beboer with ID: {beboer_id}")
            conn.commit()


        conn.execute(text("""
                      INSERT INTO user_table (beboer_id, role, username, password)
                      VALUES (:beboer_id, :role, :username, :password)
                      """),
                      {
                          "beboer_id": beboer_id,
                          "role": role,
                          "username": username,
                          "password": password
                      })
        conn.commit()
        return "User Created"
    return render_template("signup.html")

@app.route("/foodclub/", methods = ['GET', 'POST'])
def foodclub():
    result = conn.execute(text("""
                    SELECT * FROM madklub;
                      """))
    result = result.fetchall()

    food = {
        "name": result[0][2],
        "description": "A platform to organize and manage your food club activities.",
        "features": [
            "Event scheduling",
            "Member management"
        ],
    }

    return render_template("foodclub.html", food = food)

@app.route("/foodclub/add", methods = ['GET', 'POST'])
def add_foodclub():

    if request.method == "POST":
        menu = request.form.get("menu") 
        close_at = request.form.get("close_at") 
        start_at = request.form.get("start_at") 
        vege = request.form.get("vege") == "on"
        vegan = request.form.get("vegan") == "on"

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
    return render_template("foodclubadd.html")

if __name__ == "__main__":
    app.run(debug=True)