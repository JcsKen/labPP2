# insert_ops.py
import csv
from db import connect

def insert_from_console():
    first_name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL insert_or_update_user(%s, %s)", (first_name, phone))
        conn.commit()
        print("Data inserted or updated successfully!")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    cur.close()
    conn.close()

def insert_from_csv(file_path):
    conn = connect()
    cur = conn.cursor()
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        user_list = []
        for row in reader:
            user_list.append(row)
        cur.execute("CALL insert_many_users(%s)", (user_list,))
    conn.commit()
    cur.close()
    conn.close()
    print("CSV Data inserted successfully!")
