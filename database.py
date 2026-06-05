import sqlalchemy as db
from sqlalchemy import text
from sqlalchemy_utils import database_exists, create_database



target_database = "postgresql://postgres:postgres@localhost/madklub"

if not database_exists(target_database):
    create_database(target_database)

print(database_exists(target_database))

database = db.create_engine(target_database)
  
conn = database.connect()

def create_user_table(conn):
    conn.execute(text("DROP TABLE IF EXISTS user_table;"))
    conn.execute(text("""
        CREATE TABLE user_table (
            id SERIAL PRIMARY KEY,
            beboer_id INT,
            role VARCHAR(20),
            username VARCHAR(50),
            password VARCHAR(200)
            );"""
        ))
    conn.commit()

def create_beboer_table(conn):
    conn.execute(text("DROP TABLE IF EXISTS beboer;"))
    conn.execute(text("""
        CREATE TABLE beboer (
            id SERIAL PRIMARY KEY,
            name VARCHAR(30),
            room_number INT,
            madklub_taken BOOL,
            amount_cleanings INT,
            cleanings_done INT
            );"""
        ))
    conn.commit()


def create_madklub_table(conn):
    conn.execute(text("DROP TABLE IF EXISTS madklub;"))
    conn.execute(text("""
        CREATE TABLE madklub (
            id SERIAL PRIMARY KEY,
            beboer_id INT,
            menu VARCHAR(200),
            close_at VARCHAR(40),
            start_at VARCHAR(40),
            vege BOOL,
            vegan BOOL,
            price FLOAT,
            picture VARCHAR(100)
            );"""
        ))
    conn.commit()
    
def create_event_table(conn):
    conn.execute(text("DROP TABLE IF EXISTS event;"))
    conn.execute(text("""
        CREATE TABLE event (
            id SERIAL PRIMARY KEY,
            headline VARCHAR(100),
            body VARCHAR(100),
            start_date VARCHAR(100),
            end_date VARCHAR(100),
            category VARCHAR(100)
            );"""
        ))
    conn.commit()
    
def create_tables(conn):
      create_user_table(conn)
      print("User table has been created\n")
      create_beboer_table(conn)
      print("Beboer table has been created\n")
      create_madklub_table(conn)
      print("Madklub table has been created\n")
      create_event_table(conn)
      print("Event table has been created\n")

create_tables(conn)