import sqlite3
import os

def find_path(path: str):
    return os.path.abspath(__file__ + f"/../../{path}")

def edit_database(command: str):
    print(command)
    with sqlite3.connect(find_path(path = "database.db")) as database:
        cursor = database.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        database.commit()
    return data