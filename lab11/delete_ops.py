# delete_ops.py
from db import connect

def delete_entry(identifier):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_by_identifier(%s)", (identifier,))
    conn.commit()
    cur.close()
    conn.close()
    print("Deletion successful!")
