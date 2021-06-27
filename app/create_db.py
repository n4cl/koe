import sqlite3
con = sqlite3.connect('/usr/local/storage/koe.db', isolation_level=None)

con.execute("BEGIN")

con.execute("""
CREATE TABLE content(
    id INTEGER PRIMARY KEY,
    user TEXT,
    title TEXT,
    body TEXT,
    file TEXT,
    play_time INTEGER,
    view INTEGER,
    fav INTEGER,
    created_date TEXT,
    updated_date TEXT
)""")

con.execute("COMMIT")
