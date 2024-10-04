import sqlite3
from sqlite3 import Error
from contextlib import contextmanager

database = './task_management.db'

@contextmanager
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = sqlite3.connect(db_file)
    yield conn
    conn.rollback()
    conn.close()

def execute_query(conn, query, params=None):
    """ Execute a SQL query """
    try:
        c = conn.cursor()
        if params:
            c.execute(query, params)
        else:
            c.execute(query)
        conn.commit()
        return c.fetchall()
    except Error as e:
        print(e)

if __name__ == '__main__':
    with create_connection(database) as conn:
        if conn is not None:

            user_id = 1
            tasks_for_user = execute_query(conn, "SELECT * FROM tasks WHERE user_id=?", (user_id,))
            print("Tasks for user 1:", tasks_for_user)

            status_name = 'new'
            status_id = execute_query(conn, "SELECT id FROM status WHERE name=?", (status_name,))[0][0]
            tasks_by_status = execute_query(conn, "SELECT * FROM tasks WHERE status_id=?", (status_id,))
            print("Tasks with status 'new':", tasks_by_status)

            task_id = 1
            new_status_name = 'in progress'
            new_status_id = execute_query(conn, "SELECT id FROM status WHERE name=?", (new_status_name,))[0][0]
            execute_query(conn, "UPDATE tasks SET status_id=? WHERE id=?", (new_status_id, task_id))

            users_without_tasks = execute_query(conn, """
                SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks)
            """)
            print("Users without tasks:", users_without_tasks)

            new_task = ('New Task Title', 'Task Description', new_status_id, user_id)
            execute_query(conn, "INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)", new_task)

            not_completed_status_id = execute_query(conn, "SELECT id FROM status WHERE name != 'completed'")
            not_completed_tasks = execute_query(conn, "SELECT * FROM tasks WHERE status_id IN (?)", (not_completed_status_id,))
            print("Tasks not completed:", not_completed_tasks)

            task_to_delete_id = 1
            execute_query(conn, "DELETE FROM tasks WHERE id=?", (task_to_delete_id,))

            email_filter = '%@example.com'
            users_with_specific_email = execute_query(conn, "SELECT * FROM users WHERE email LIKE ?", (email_filter,))
            print("Users with specific email:", users_with_specific_email)

            new_fullname = 'Updated Name'
            execute_query(conn, "UPDATE users SET fullname=? WHERE id=?", (new_fullname, user_id))

            task_count_by_status = execute_query(conn, """
                SELECT s.name, COUNT(t.id) FROM tasks t
                JOIN status s ON t.status_id = s.id
                GROUP BY t.status_id
            """)
            print("Task count by status:", task_count_by_status)


            domain_filter = '%@example.com'
            tasks_for_specific_domain = execute_query(conn, """
                SELECT t.* FROM tasks t
                JOIN users u ON t.user_id = u.id
                WHERE u.email LIKE ?
            """, (domain_filter,))
            print("Tasks for specific email domain:", tasks_for_specific_domain)
