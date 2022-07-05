import sqlite3
from sqlite3 import Error

import pandas as pd
import sqlite3
conn = sqlite3.connect("../mlflow.db")
table = pd.read_sql_query("SELECT * FROM sqlite_master", conn)
print(table)

#
# def create_connection(db_file):
#     """ create a database connection to the SQLite database
#         specified by the db_file
#     :param db_file: database file
#     :return: Connection object or None
#     """
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#     except Error as e:
#         print(e)
#
#     return conn
#
#
# def select_task(conn):
#
#     """
#     Query all rows in the tasks table
#     :param conn: the Connection object
#     :return:
#     """
#     cur = conn.cursor()
#     cur.execute("select * from mlflow.experiments;")
#
#     rows = cur.fetchall()
#
#     for row in rows:
#         print(row)
#
#
# def delete_task(conn, id):
#     """
#     Delete a task by task id
#     :param conn:  Connection to the SQLite database
#     :param id: id of the task
#     :return:
#     """
#     sql = 'DELETE FROM tasks WHERE id=?'
#     cur = conn.cursor()
#     cur.execute(sql, (id,))
#     conn.commit()
#
#
# def delete_all_tasks(conn):
#     """
#     Delete all rows in the tasks table
#     :param conn: Connection to the SQLite database
#     :return:
#     """
#     sql = 'DELETE FROM tasks'
#     cur = conn.cursor()
#     cur.execute(sql)
#     conn.commit()
#
#
# def main():
#     database = '../mlflow.db'
#
#     # create a database connection
#     conn = create_connection(database)
#     with conn:
#         select_task(conn)
#         # delete_task(conn, 2);
#         # delete_all_tasks(conn);
#
#
# if __name__ == '__main__':
#     main()