import sqlite3


# Function to establish a connection to the SQLite database
def connection():
    database_file = r"./model/database.db"
    conn = sqlite3.connect(database_file)
    return conn


# Function to get the user ID based on the username
def getUserId(username):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", [username])
    return cursor.fetchone()[0]


# Function to check if the provided username and password match a user in the database
def login(username, password):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
    )
    if cursor.fetchone():
        conn.commit()
        conn.close()
        return True
    else:
        return False


# Function to register a new user in the database
def register(username, password):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    results = cursor.fetchall()
    if len(results) != 0:
        return False
    else:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        conn.commit()
        conn.close()
        return True


# Function to store a user's rating for a book in the database
def storeRating(username, booktitle, rating):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ratings (username, booktitle, rating) VALUES (?, ?, ?)",
        (username, booktitle, rating),
    )
    conn.commit()
    conn.close()


# Function to get all ratings for a specific user from the database
def getRating(username):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ratings WHERE username = ?", [username])
    return cursor.fetchall()
