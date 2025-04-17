# main.py
from db import create_table, create_functions_and_procedures
from insert_ops import insert_from_console, insert_from_csv
from update_ops import update_entry
from query_ops import query_phonebook, search_by_pattern, query_paginated
from delete_ops import delete_entry

if __name__ == "__main__":
    create_table()
    create_functions_and_procedures()

    insert_from_console()
    insert_from_csv("contacts.csv")
    update_entry("John", new_phone="1234567890")
    query_phonebook(filter_name="John")
    search_by_pattern("Jo")
    query_paginated(5, 0)
    delete_entry("John")
