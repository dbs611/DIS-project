import sqlalchemy as db
from sqlalchemy import text
from sqlalchemy_utils import database_exists, create_database
import csv

target_database = "postgresql://postgres:postgres@localhost/madklub"

if not database_exists(target_database):
    create_database(target_database)

print(database_exists(target_database))

database = db.create_engine(target_database)

with database.begin() as conn:

    conn.execute(text("TRUNCATE TABLE beboer RESTART IDENTITY;"))

    with open('users.csv', 'r', encoding='utf-8') as f:
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
