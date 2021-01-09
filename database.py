import sqlite3

def connect():
    connection = sqlite3.connect("database.db", check_same_thread = False)
    try:
        connection.execute("""CREATE TABLE errors (
    errorID integer PRIMARY KEY AUTOINCREMENT,
    message text
);""")
    except sqlite3.OperationalError:
        pass
    return connection

def create(connection, errorID, message):
    while True:
        try:
            connection.execute(f"INSERT INTO errors (errorID, message) VALUES ('{errorID}', '{message}');")
            connection.commit()
            break
        except sqlite3.IntegrityError:
            errorID += 1
            continue

def retrieve(connection):
    cursor = connection.execute(f"SELECT * FROM errors;")
    output = []
    for row in cursor:
        message = {}
        message["id"] = row[0]
        message["message"] = row[1]
        output.append(message)
    return output