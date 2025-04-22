import psycopg2

from config import load_config

def create_tables():
    commands = (
        """
        CREATE TABLE 
        """
        ,
        """

        """
        ,
        """

        """
        ,
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    create_tables()
