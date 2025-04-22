from db import connect

def update_entry(old_name, new_name=None, new_phone=None):
    conn = connect()
    cur = conn.cursor()
    
    if new_name:
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s", (new_phone, old_name))
    
    conn.commit()
    conn.close()
    print("Update successful!")

from db import connect

def upsert_user(name, phone):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT upsert_user_func(%s, %s)", (name, phone))
        result = cur.fetchone()[0]
        print(result)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()