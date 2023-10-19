import psycopg2
from .helpers import connect_with_db, commit_and_close_connection
from .config import user_login_query, table_values_query, snowflake_credentials_values_query
import streamlit as st



def insert_table_values(user_id, qualified_table_name, metadata, table_description=None):
    connection, cursor = connect_with_db()
    cursor.execute("INSERT INTO tableinputs (user_id, table_name, table_description, meta_data) VALUES (%s, %s)", 
                   (user_id, qualified_table_name, metadata, table_description))
    commit_and_close_connection(connection, cursor)

def insert_credential_values(user_id, username, password, azure_account, warehouse, database, schema, role):
    connection, cursor = connect_with_db()
    cursor.execute("INSERT INTO snowflakecredentials (user_id, username, password, azure_account, warehouse, database, schema, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                   (user_id, username, password, azure_account, warehouse, database, schema, role))
    commit_and_close_connection(connection, cursor)


@st.cache_data
def user_login(username, password):
    connection, cursor = connect_with_db()
    cursor.execute(user_login_query.format(username, password))
    login_result = cursor.fetchone()
    commit_and_close_connection(connection, cursor)
    return login_result


def get_table_values(user_id):
    connection, cursor = connect_with_db()
    getting_table_values_result = cursor.execute(table_values_query.format(user_id))
    commit_and_close_connection(connection, cursor)
    return getting_table_values_result


def get_snowflake_credentials_values(user_id):
    connection, cursor = connect_with_db()
    cursor.execute(snowflake_credentials_values_query.format(user_id))
    getting_snowflake_credentials_values_result = cursor.fetchone()
    commit_and_close_connection(connection, cursor)
    return getting_snowflake_credentials_values_result



connection, cursor = connect_with_db()
result = cursor.execute("""SELECT id FROM snowflakecredentials""")
print(result)
commit_and_close_connection(connection, cursor)





# commit_and_close_connection(connection, cursor)

# try:
#     cursor.execute("INSERT INTO tableinputs (table_name, table_description, meta_data) VALUES (%s, %s)", (qualified_table_name, metadata, table_description))
# except:
#     pass ``
# cur.execute("INSERT INTO datacamp_courses(course_name, course_instructor, topic) VALUES('Introduction to SQL','Izzy Weber','Julia')");

# # Execute a command: create datacamp_courses table
# cur.execute("""CREATE TABLE datacamp_courses(
#             course_id SERIAL PRIMARY KEY,
#             course_name VARCHAR (50) UNIQUE NOT NULL,
#             course_instructor VARCHAR (100) NOT NULL,
#             topic VARCHAR (20) NOT NULL);
#             """)
# # Make the changes to the database persistent
# conn.commit()
# Close cursor and communication with the database
# cur.execute("""SELECT * FROM datacamp_courses""")
# for table in cur.fetchall():
#     print(table)

# print(conn)