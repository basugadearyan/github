import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def create_database():
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
    conn.commit()
    cur.close()
    conn.close()

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER,
        password=DB_PASSWORD, database=DB_NAME
    )

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150)
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INT AUTO_INCREMENT PRIMARY KEY,
        category_name VARCHAR(100) NOT NULL UNIQUE
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        expense_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(150) NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        expense_date DATE NOT NULL,
        category_id INT NOT NULL,
        payment_mode VARCHAR(50) NOT NULL,
        description VARCHAR(255),
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS income (
        income_id INT AUTO_INCREMENT PRIMARY KEY,
        source VARCHAR(150) NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        income_date DATE NOT NULL,
        remarks VARCHAR(255)
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        budget_id INT AUTO_INCREMENT PRIMARY KEY,
        category_id INT NULL,
        amount DECIMAL(10,2) NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    )""")

    categories = ["Food","Travel","Rent","Bills","Shopping","Education","Medical","Other"]
    for category in categories:
        cur.execute(
            "INSERT IGNORE INTO categories (category_name) VALUES (%s)",
            (category,)
        )

    conn.commit()
    cur.close()
    conn.close()

def setup_database():
    create_database()
    create_tables()

if __name__ == "__main__":
    setup_database()
    print("MySQL database and tables are ready.")
