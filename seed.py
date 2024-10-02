import sqlite3
from faker import Faker

database = './test.db'

def clear_table(conn, table_name):
    """ Clear the table before inserting new values """
    sql = f"DELETE FROM {table_name}"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def insert_statuses(conn):
    statuses = [('new',), ('in progress',), ('completed',)]
    sql = "INSERT INTO status (name) VALUES (?)"
    cur = conn.cursor()
    cur.executemany(sql, statuses)
    conn.commit()

def insert_users(conn, num_users=10):
    fake = Faker()
    users = [(fake.name(), fake.email()) for _ in range(num_users)]
    sql = "INSERT INTO users (fullname, email) VALUES (?, ?)"
    cur = conn.cursor()
    cur.executemany(sql, users)
    conn.commit()

def insert_tasks(conn, num_tasks=20):
    fake = Faker()
    cur = conn.cursor()
    cur.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cur.fetchall()]

    tasks = [
        (
            fake.sentence(nb_words=6),
            fake.text(),
            fake.random_element(status_ids),
            fake.random_element(user_ids)
        )
        for _ in range(num_tasks)
    ]
    sql = "INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)"
    cur.executemany(sql, tasks)
    conn.commit()

if __name__ == '__main__':
    with sqlite3.connect(database) as conn:
        clear_table(conn, 'status')
        insert_statuses(conn)
        insert_users(conn)
        insert_tasks(conn)
