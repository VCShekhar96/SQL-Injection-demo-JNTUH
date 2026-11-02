# Implement secure authentication

import hmac

from database import get_connection


def login(username, password):

    connection = get_connection()

    try:
        query = """
            SELECT username, password_hash, salt
            FROM users
            WHERE username = ?
        """

        cursor = connection.execute(query, (username,))

        user = cursor.fetchone()

        if user is None:
            return False

        import hashlib

        entered_password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            user["salt"],
            600000
        )

        if hmac.compare_digest(
            entered_password_hash,
            user["password_hash"]
        ):
            return True

        return False

    finally:
        connection.close()


if __name__ == "__main__":

    username = input("Enter username: ")
    password = input("Enter password: ")

    if login(username, password):
        print("Login successful!")
    else:
        print("Invalid username or password.")