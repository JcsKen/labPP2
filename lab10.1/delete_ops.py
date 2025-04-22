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
