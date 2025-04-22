from db import create_table
from insert_ops import insert_from_console, insert_from_csv
from update_ops import update_entry
from query_ops import query_phonebook
from delete_ops import delete_entry

if __name__ == "__main__":
    create_table()
    insert_from_console()
    insert_from_csv("contacts.csv")
    update_entry("John", new_phone="1234567890")
    query_phonebook(filter_name="John")
    delete_entry("1234567890", by_phone=True)

