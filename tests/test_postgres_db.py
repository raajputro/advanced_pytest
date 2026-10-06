import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

# --- Connection ---
def get_postgres_connection():
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        database=os.getenv("PG_DATABASE"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD")
    )
    return conn

def get_postgres_connection_generic(host, port, database, user, password):
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    return conn

# --- Execute SELECT ---
def postgres_select(query: str = "select sa.account_name, sa.account_no, sa.installment_amount from savings_account sa limit 5"):

    conn = get_postgres_connection()
    conn1 = get_postgres_connection_generic(os.getenv("PG_HOST"), os.getenv("PG_PORT"), os.getenv("PG_DATABASE"), os.getenv("PG_USER"), os.getenv("PG_PASSWORD"))
    conn2 = get_postgres_connection_generic(os.getenv("PG_HOST2"), os.getenv("PG_PORT2"), os.getenv("PG_DATABASE2"), os.getenv("PG_USER2"), os.getenv("PG_PASSWORD2"))
    output_in_table_format = 0

    try:
        with conn1.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(query)
            rows = cur.fetchall()

            if output_in_table_format == 0:
                for row in rows:
                    print(row)
            else:
                print(tabulate(rows, headers="keys", tablefmt="grid"))
            return rows
    finally:
        conn1.close()


# # --- Execute INSERT / UPDATE / DELETE ---
# def postgres_insert(name, email):
#     conn = get_postgres_connection()
#     try:
#         with conn.cursor() as cur:
#             cur.execute(
#                 "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
#                 (name, email)
#             )
#             new_id = cur.fetchone()[0]
#             conn.commit()
#             print(f"Inserted user with id: {new_id}")
#             return new_id
#     except Exception as e:
#         conn.rollback()
#         raise e
#     finally:
#         conn.close()

# # --- Bulk insert ---
# def postgres_bulk_insert(users):
#     conn = get_postgres_connection()
#     try:
#         with conn.cursor() as cur:
#             cur.executemany(
#                 "INSERT INTO users (name, email) VALUES (%s, %s)",
#                 users  # list of tuples
#             )
#             conn.commit()
#     finally:
#         conn.close()

if __name__ == "__main__":
    postgres_select()
    # postgres_insert("Alice", "alice@example.com")