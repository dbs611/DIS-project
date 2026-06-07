# DIS_PROJECT_Group75
Anton Vesterbæk - KU ID: mjh161
Mathias Hilger - KU ID: smj563
Simon Thrane - KU ID: dbs611

# About the project
This project is oriented for dormmates who are looking for an easy way to keep themselves oriented on foodclubs, kitchen cleanings etc. By this we've created a database and a small frontend to represent the data from the database. We use the databases to keep track of the amount of foodclubs and cleanings that each person has made, and also for others to keep track of. Other people should also be able to see whats for dinner and sign up for the foodclubs.

## E/R Diagram
![alt text](ERdiagram.png "E/R Diagram")

# Install Dependencies 
Install PostgreSQL from:

https://www.postgresql.org/download/windows/

During installation:

Username: postgres
Password: postgres
Port: 5432

Install all required packages:

```bash
pip install Flask
pip install SQLAlchemy
pip install sqlalchemy-utils
pip install psycopg2-binary
pip install Werkzeug
```

Or install them all at once:

```bash 
pip install Flask SQLAlchemy sqlalchemy-utils psycopg2-binary Werkzeug
```

# Getting started (compilation/execution instructions)
First run:

```bash 
py database.py
```

to create all the databases. Then run:

```bash 
py -m flask run 
```

to run the app.  



# Website interaction instructions
To access the site, you have to login. The logins are saved in the 'user_table' relation, and gives you access to register new foodclubs and join existing ones. You make your own user at http://127.0.0.1:5000/signup, and login at http://127.0.0.1:5000/login. 

# Shortcommings
We decided not to include events and cleaning schedule and focused purely on the foodclubs due to time constraints.  

# AI-Declaration
We have not used generative AI to generate code during the development of this project. We have used AI regarding some issues concerning managing virtual enviroments and installing packages. 
