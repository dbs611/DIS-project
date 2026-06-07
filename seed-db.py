import csv
import os

import sqlalchemy as db
from sqlalchemy import text
from sqlalchemy_utils import database_exists, create_database
from werkzeug.security import generate_password_hash

target_database = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost/madklub",
)

if not database_exists(target_database):
    create_database(target_database)

print(database_exists(target_database))

database = db.create_engine(target_database)

with database.begin() as conn:

    conn.execute(text("TRUNCATE TABLE beboer RESTART IDENTITY;"))

    with open('beboer.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            print(row)
            conn.execute(
                text("""
                    INSERT INTO beboer (id, name, room_number, madklub_taken, amount_cleanings, cleanings_done)
                    VALUES (:id, :name, :room_number, :madklub_taken, :amount_cleanings, :cleanings_done)
                """),
                {
                    "id": int(row[0]),
                    "name": row[1],
                    "room_number": int(row[2]),
                    "madklub_taken": row[3].upper() == 'TRUE',
                    "amount_cleanings": int(row[4]),
                    "cleanings_done": int(row[5])
                }
            )
        print("Successfully seeded BEBOER databasse")
    
    with open('user_table.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        seeded_users = []
        for row in reader:
            username = row[3]
            plain_password = row[4]
            hashed_password = generate_password_hash(plain_password)
            seeded_users.append((username, plain_password))
            conn.execute(
                text("""
                    INSERT INTO user_table (id, beboer_id, role, username, password)
                    VALUES (:id, :beboer_id, :role, :username, :password)
                """),
                {
                    "id": int(row[0]),
                    "beboer_id": int(row[1]),
                    "role": row[2],
                    "username": username,
                    "password": hashed_password,
                }
            )
        print("Successfully seeded USER_TABLE database")
        print("\n--- Seeded login credentials (passwords stored hashed in DB) ---")
        for username, plain_password in seeded_users:
            print(f"  username: {username:<25} password: {plain_password}")
        print("---\n")

    conn.execute(text("TRUNCATE TABLE madklub RESTART IDENTITY;"))

    with open('madklub.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            conn.execute(
                text("""
                    INSERT INTO madklub (id, beboer_id, menu, close_at, start_at, vege, vegan, price, picture)
                    VALUES (:id, :beboer_id, :menu, :close_at, :start_at, :vege, :vegan, :price, :picture)
                """),
                {
                    "id": int(row[0]),
                    "beboer_id": int(row[1]),
                    "menu": row[2],
                    "close_at": row[3],
                    "start_at": row[4],
                    "vege": row[5].upper() == 'TRUE',
                    "vegan": row[6].upper() == 'TRUE',
                    "price": float(row[7]),
                    "picture": row[8] or None,
                }
            )
        print("Successfully seeded MADKLUB database")

    conn.execute(text("SELECT setval('beboer_id_seq', (SELECT MAX(id) FROM beboer))"))
    conn.execute(text("SELECT setval('user_table_id_seq', (SELECT MAX(id) FROM user_table))"))
    conn.execute(text("SELECT setval('madklub_id_seq', (SELECT MAX(id) FROM madklub))"))
