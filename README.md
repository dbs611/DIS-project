<<<<<<< HEAD
# DIS_PROJECT_Group75

# About the project

This project is oriented for dormmates who are looking for an easy way to keep themselves oriented on foodclubs, kitchen cleanings etc. By this we've created a database and a small frontend to represent the data from the database. We use the databases to keep track of the amount of foodclubs and cleanings that each person has made, and also for others to keep track of. Other people should also be able to see whats for dinner and sign up for the foodclubs. 

## E/R Diagram
![alt text](ERdiagram.png "E/R Diagram")

# Getting started




# Install Dependencies 

## Check your versions for Node and npm
### Node recommend to be higher than v20.x.x
```sh
node -v
```
&
```sh
npm -v
```

If none of these are installed:
```sh
sudo apt install npm nodejs
```

### Clone the repository
```sh
git clone [https://git.ku.dk/smj563/dis_project_group75.git](https://git.ku.dk/smj563/dis_project_group75.git)
```

### Enter the directory
```sh
cd dis_project_group75
```
### Install dependencies
```sh
npm install
```

### Install the ORM and the Postgres driver
```sh
npm install drizzle-orm postgres
```
### Install Drizzle Kit (CLI for database migrations) and dotenv (for env variables) as dev dependencies
```sh
npm install -D drizzle-kit dotenv
```

### Configure Your Database URL
```sh
touch .env
```

### Replace with your actual database credentials
```
DATABASE_URL="postgres://postgres:yourpassword@localhost:5432/your_database_name"
```

### Running the project 

```sh
npm run dev
```

