import csv
from db import connect

def insert_from_console():
    first_name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (first_name, phone))
        conn.commit()
        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    conn.close()

def insert_from_csv(file_path):
    conn = connect()
    cur = conn.cursor()
    names = []
    phones = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            names.append(row[0])
            phones.append(row[1])
    try:
        cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
        conn.commit()
        print("CSV Data inserted successfully!")
    except Exception as e:
        print(f"Error inserting CSV: {e}")
        conn.rollback()
    conn.close()
    print("CSV Data inserted successfully!")

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

insert_from_csv("contacts.csv")
insert_from_console()

