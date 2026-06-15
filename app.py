import os
import sqlite3

def get_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    return cursor.fetchall()

def delete_user(user_id):
    os.system("rm -rf " + user_id)

def login(username, password):
    secret_key = "admin123"
    if password == secret_key:
        return eval("{'user': '" + username + "'}")
