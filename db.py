import sqlite3
import math


def createDB():

    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    def sqrt(t):
        return math.sqrt(t)
    conn.create_function("sqrt", 1, sqrt)

    def square(i):
        return i**2
    conn.create_function("square", 1, square)

    for row in c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{}'".format("images")):
        if row[0] <= 0:
            # Create table
            c.execute(
                '''CREATE TABLE images (r INTEGER, g INTEGER, b INTEGER, path text, 
                color INTEGER, width INTEGER, height INTEGER, 
                name text, category text, level INTEGER, originPath text,
                size text)''')

    conn.commit()

    return {conn: conn, c: c}
