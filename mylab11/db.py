import psycopg2

def connect():
    return psycopg2.connect(
        dbname="phonebook", user="postgres", password="27112005", host="localhost", port="5432"
    )

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone VARCHAR(15) UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_table()