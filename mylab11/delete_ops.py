from db import connect

def delete_entry(identifier, by_phone=False):
    conn = connect()
    cur = conn.cursor()
    if by_phone:
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (identifier,))
    else:
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (identifier,))
    conn.commit()
    conn.close()
    print("Deletion successful!")

def delete_user(identifier):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT delete_user_func(%s)", (identifier,))
        result = cur.fetchone()[0]
        print(result)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()