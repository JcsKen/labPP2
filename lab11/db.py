# db.py
import psycopg2

def connect():
    return psycopg2.connect(
        dbname="phonebook_db", user="your_user", password="your_password", host="localhost", port="5432"
    )

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone VARCHAR(15) UNIQUE NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def create_functions_and_procedures():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE OR REPLACE FUNCTION search_by_pattern(pattern TEXT)
        RETURNS TABLE(id INT, first_name TEXT, phone TEXT) AS $$
        BEGIN
            RETURN QUERY
            SELECT * FROM phonebook
            WHERE first_name ILIKE '%' || pattern || '%'
               OR phone ILIKE '%' || pattern || '%';
        END;
        $$ LANGUAGE plpgsql;
    """)

    cur.execute("""
        CREATE OR REPLACE PROCEDURE insert_or_update_user(user_name TEXT, user_phone TEXT)
        LANGUAGE plpgsql AS $$
        BEGIN
            IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = user_name) THEN
                UPDATE phonebook SET phone = user_phone WHERE first_name = user_name;
            ELSE
                INSERT INTO phonebook(first_name, phone) VALUES (user_name, user_phone);
            END IF;
        END;
        $$;
    """)

    cur.execute("""
        CREATE OR REPLACE PROCEDURE insert_many_users(user_list TEXT[][], OUT incorrect TEXT[][])
        LANGUAGE plpgsql AS $$
        DECLARE
            i INT := 1;
            name TEXT;
            phone TEXT;
        BEGIN
            incorrect := ARRAY[]::TEXT[][];
            WHILE i <= array_length(user_list, 1) LOOP
                name := user_list[i][1];
                phone := user_list[i][2];

                IF phone ~ '^\\d{10,15}$' THEN
                    BEGIN
                        INSERT INTO phonebook(first_name, phone) VALUES (name, phone);
                    EXCEPTION WHEN unique_violation THEN
                        UPDATE phonebook SET phone = phone WHERE first_name = name;
                    END;
                ELSE
                    incorrect := array_append(incorrect, ARRAY[name, phone]);
                END IF;
                i := i + 1;
            END LOOP;
        END;
        $$;
    """)

    cur.execute("""
        CREATE OR REPLACE FUNCTION get_paginated(limit_num INT, offset_num INT)
        RETURNS TABLE(id INT, first_name TEXT, phone TEXT) AS $$
        BEGIN
            RETURN QUERY
            SELECT * FROM phonebook ORDER BY id LIMIT limit_num OFFSET offset_num;
        END;
        $$ LANGUAGE plpgsql;
    """)

    cur.execute("""
        CREATE OR REPLACE PROCEDURE delete_by_identifier(identifier TEXT)
        LANGUAGE plpgsql AS $$
        BEGIN
            DELETE FROM phonebook WHERE first_name = identifier OR phone = identifier;
        END;
        $$;
    """)

    conn.commit()
    cur.close()
    conn.close()
