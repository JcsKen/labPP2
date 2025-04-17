# update_ops.py
from db import connect

def update_entry(old_name, new_name=None, new_phone=None):
    conn = connect()
    cur = conn.cursor()
    if new_name:
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s", (new_phone, old_name))
    conn.commit()
    cur.close()
    conn.close()
    print("Update successful!")
