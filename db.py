import sqlite3

def get_connection():
    return sqlite3.connect("forms.db")

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        sphere TEXT,
        problem TEXT,
        volume TEXT,
        priority TEXT,
        format TEXT,
        contact TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_form(data, user_id):
    conn = sqlite3.connect("forms.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO forms (
            user_id,
            sphere,
            problem,
            volume,
            priority,
            format,
            contact
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            data["sphere"],
            data["problem"],
            data["volume"],
            data["priority"],
            data["format"],
            data["contact"],
        )
    )

    conn.commit()
    conn.close()