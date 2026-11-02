# Study unsafe SQL construction

import sqlite3

connection = sqlite3.connect("training.db")

cursor = connection.cursor()

query = """
    SELECT *
    FROM users
    WHERE username = ?
"""

username = input("Enter username: ")

cursor.execute(query, (username,))

result = cursor.fetchone()

print(result)

connection.close()