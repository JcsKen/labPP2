from db import create_table
from insert_ops import insert_from_console, insert_from_csv
from update_ops import update_entry
from query_ops import query_phonebook
from delete_ops import delete_entry
from update_ops import upsert_user
from delete_ops import delete_user

if __name__ == "__main__":
    create_table()
    insert_from_console()
    insert_from_csv("contacts.csv")

    update_entry("John", new_phone="1234567890")
    query_phonebook(filter_name="John")
    delete_entry("1234567890", by_phone=True)

    upsert_user("Alice", "+7771234567")
    upsert_user("Alice", "+7770000000")  

    delete_user("Alice")
    delete_user("+7770000000")  
