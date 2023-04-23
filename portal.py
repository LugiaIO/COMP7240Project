import sqlite3


def connection():
    database_file = r"./model/database.db"
    conn = sqlite3.connect(database_file)
    return conn


def getUserId(username):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", [username])
    return cursor.fetchone()[0]


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


def storeRating(username, booktitle, rating):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ratings (username, booktitle, rating) VALUES (?, ?, ?)",
        (username, booktitle, rating),
    )
    conn.commit()
    conn.close()


def getRating(username):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ratings WHERE username = ?", [username])
    return cursor.fetchall()
