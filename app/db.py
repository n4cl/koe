import sqlite3
con = sqlite3.connect('koe.db', isolation_level=None)

con.execute("BEGIN")

con.execute("""
CREATE TABLE content(
    id INTEGER PRIMARY KEY,
    title TEXT,
    body TEXT,
    file TEXT,
    play_time INTEGER,
    fav INTEGER,
    views INTEGER,
    created_date TEXT,
    updated_date TEXT
)""")

con.execute("COMMIT")
