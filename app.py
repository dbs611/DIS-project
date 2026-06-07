from flask import Flask, render_template, request, session, url_for, redirect
import sqlalchemy as db
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import re

datetime_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
app = Flask(__name__)
target_database = "postgresql://postgres:postgres@localhost/madklub"
database = db.create_engine(target_database)
conn = database.connect()
food = {
    "name": "result[0][2]",
    "description": "A platform to organize and manage your food club activities.",
    "features": [
        "Event scheduling",
        "Member management"
    ],
}
UPLOAD_FOLDER = os.path.join('static', "foodimages")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.secret_key = 'secret_key'
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
        password2 = request.form.get("password2")
        if not password:
            return "Password must be set", 400
        if password != password2:
            return "Password must be the same", 400
        hashed_pw = generate_password_hash(password)
        ##ADD SALT TO HASHED PASSWORD
        role = request.form.get("role")
        ##Beboer
        with database.begin() as conn:
            beboer_id = None
            if role == "beboer":
                name = request.form.get("name")
                room = request.form.get("room_number")
                result = conn.execute(text("""
                            INSERT INTO beboer (name, room_number, madklub_taken, amount_cleanings, cleanings_done)
                                VALUES (:name, :room_number, :madklub_taken, :amount_cleanings, :cleanings_done)
                                RETURNING id;
                                           """),
                                {
                                    "name": name,
                                    "room_number": room,
                                    "madklub_taken": False,
                                    "amount_cleanings": 2,
                                    "cleanings_done": 0
                                })
                row = result.first()
                if row is not None:
                    beboer_id = row[0]
                print("Creating a new beboer with ID: {beboer_id}")

            conn.execute(text("""
                        INSERT INTO user_table (beboer_id, role, username, password)
                        VALUES (:beboer_id, :role, :username, :password)
                        """),
                        {
                            "beboer_id": beboer_id,
                            "role": role,
                            "username": username,
                            "password": hashed_pw
                        })
            session["user_id"] = beboer_id
            session["username"] = username
            return render_template("index.html")
    return render_template("signup.html")

@app.route("/login/", methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        result = conn.execute(text("SELECT id, username, password FROM user_table WHERE username = :username;"), {"username": username})
        user_row = result.mappings().first()
        print(user_row)
        if not password:
            return "Password must be set", 400
        if user_row is not None:
            database_password = user_row["password"]
            
            is_correct = check_password_hash(database_password, password)
            if is_correct:
                session["user_id"] = user_row["id"]
                session["username"] = user_row["username"]
                result = conn.execute(text("SELECT * FROM madklub;"))
                madklub_rows = result.mappings().all()
                
                return render_template("foodclub.html", meals=madklub_rows)
            
            else:
                print("Incorrect password")
        else:
            print("Username not found.")
    return render_template("login.html")

@app.route("/foodclub/", methods = ['GET', 'POST'])
def foodclub():
    with database.begin() as conn:
        result = conn.execute(text("SELECT * FROM madklub;"))
        madklub_rows = result.mappings().all()
    
    return render_template("foodclub.html", meals=madklub_rows)

@app.route("/foodclub/add", methods = ['GET', 'POST'])
def add_foodclub():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        menu = request.form.get("menu") 
        close_at = request.form.get("close_at") 
        start_at = request.form.get("start_at") 

        if not re.match(datetime_pattern, start_at):
            return "Start date has invalid format", 400

        if not re.match(datetime_pattern, close_at):
            return "Close date has invalid format", 400

        vege = request.form.get("vege") == "on"
        vegan = request.form.get("vegan") == "on"
        image_name = request.files.get("image")
        image_name_save = None
        print(UPLOAD_FOLDER)
        if image_name and image_name.filename:
            image_name_save = secure_filename(image_name.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_name_save)
            image_name.save(filepath)


        with database.begin() as conn:
            conn.execute(text("""
                          INSERT INTO madklub (beboer_id, menu, close_at, start_at, vege, vegan, price, picture)
                          VALUES (:beboer_id, :menu, :close_at, :start_at, :vege, :vegan, :price, :picture)
                          """),
                          {
                             "beboer_id": 1, 
                             "menu": menu,
                             "close_at": close_at,
                             "start_at": start_at,
                             "vege": vege,
                             "vegan": vegan,
                             "price": 100000,
                             "picture": image_name_save 
                          }
                          )
    return render_template("foodclubadd.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
    