from db import connect

def query_phonebook(filter_name=None, filter_phone=None):
    conn = connect()
    cur = conn.cursor()
    query = "SELECT * FROM phonebook WHERE 1=1"
    params = []
    if filter_name:
        query += " AND first_name = %s"
        params.append(filter_name)
    if filter_phone:
        query += " AND phone = %s"
        params.append(filter_phone)
    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()

query_phonebook(filter_name="pork")