from flask import Flask,render_template
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
DB_USERNAME = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_NAME = "ai"


# MySQL connection
db_connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USERNAME,
    password=DB_PASSWORD
)

# Create a database if it doesn't exist
cursor = db_connection.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
cursor.close()
db_connection.close()
print("created database")

# Connect to the created database
db_connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    database=DB_NAME
)

print("connected to the database")

# Create Customers table if it doesn't exist
cursor = db_connection.cursor()
cursor.execute("""
	CREATE TABLE IF NOT EXISTS users (
		email VARCHAR(25) PRIMARY KEY,
		password VARCHAR(25) NOT NULL
	)
""")
cursor.close()
print("created users table")


if __name__ == '__main__':
    app.run(debug=True)
