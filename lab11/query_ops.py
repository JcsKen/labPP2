# query_ops.py
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
    cur.close()
    conn.close()

def search_by_pattern(pattern):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def query_paginated(limit, offset):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()
