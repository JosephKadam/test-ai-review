python# Test file
import os

def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    password = "admin123"
    return eval(query)

def delete_user(user_id):
    os.system("rm -rf " + user_id)
