import psycopg2
from .helpers import connect_with_db, commit_and_close_connection
from .config import (
    select_user_login_query,
    select_snowflake_credentials_values_query,
    select_table_inputs_values_query,
    delete_query,
    update_table_inputs_query,
    create_table_inputs_query,
    update_snowflake_credentials_query,
    create_snowflake_credentials_query,
)
import streamlit as st


def insert_table_values(
    user_id, qualified_table_name, metadata, table_description=None
):
    print("erer")
    connection, cursor = connect_with_db()
    cursor.execute(
        "INSERT INTO tableinputs (user_id, table_name, table_description, meta_data) VALUES (%s, %s, %s, %s)",
        (user_id, qualified_table_name, metadata, table_description),
    )
    commit_and_close_connection(connection, cursor)


def insert_credential_values(
    user_id, username, password, azure_account, warehouse, database, schema, role
):
    connection, cursor = connect_with_db()
    cursor.execute(
        "INSERT INTO snowflakecredentials (user_id, username, password, azure_account, warehouse, database, schema, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (user_id, username, password, azure_account, warehouse, database, schema, role),
    )
    commit_and_close_connection(connection, cursor)


@st.cache_data
def user_login(username, password):
    connection, cursor = connect_with_db()
    cursor.execute(select_user_login_query.format(username, password))
    login_result = cursor.fetchone()
    commit_and_close_connection(connection, cursor)
    return login_result


def get_snowflake_credentials_values(user_id):
    connection, cursor = connect_with_db()
    cursor.execute(select_snowflake_credentials_values_query.format(user_id))
    snowflake_credentials_values_result = cursor.fetchone()
    commit_and_close_connection(connection, cursor)
    return snowflake_credentials_values_result


def get_table_inputs_values(user_id):
    connection, cursor = connect_with_db()
    cursor.execute(select_table_inputs_values_query.format(user_id))
    table_inputs_values_result = cursor.fetchall()
    commit_and_close_connection(connection, cursor)
    return table_inputs_values_result


def delete_input(table_name, id_field_name, input_id):
    connection, cursor = connect_with_db()
    cursor.execute(delete_query.format(table_name, id_field_name, input_id))
    commit_and_close_connection(connection, cursor)


def update_table_inputs_input(table_id, table_name, meta_data, table_description):
    connection, cursor = connect_with_db()
    query = update_table_inputs_query.format(
            table_id=table_id,
            table_name=table_name,
            table_description=table_description,
            meta_data=meta_data,
        )
    print(query, " query ")
    cursor.execute(
        update_table_inputs_query.format(
            table_id=table_id,
            table_name=table_name,
            table_description=table_description,
            meta_data=meta_data,
        )
    )
    commit_and_close_connection(connection, cursor)


def create_table_inputs_input(user_id, table_name, table_description, meta_data):
    connection, cursor = connect_with_db()
    cursor.execute(
        create_table_inputs_query.format(
            user_id=user_id,
            table_name=table_name,
            table_description=table_description,
            meta_data=meta_data,
        )
    )
    commit_and_close_connection(connection, cursor)


def update_snowflake_credentials_input(
    credentials_id, credential_values
):
    connection, cursor = connect_with_db()
    cursor.execute(
        update_snowflake_credentials_query.format(
            credentials_id=credentials_id,
            username=credential_values["username"],
            password=credential_values["password"],
            azure_account=credential_values["azure_account"],
            warehouse=credential_values["warehouse"],
            database=credential_values["database"],
            schema=credential_values["schema"],
            role=credential_values["role"],
        )
    )
    commit_and_close_connection(connection, cursor)


def create_snowflake_credentials_input(
    user_id, table_name, table_description, meta_data
):
    connection, cursor = connect_with_db()
    cursor.execute(
        create_table_inputs_query.format(
            user_id=user_id,
            table_name=table_name,
            table_description=table_description,
            meta_data=meta_data,
        )
    )
    commit_and_close_connection(connection, cursor)


# connection, cursor = connect_with_db()
# result = cursor.execute("""SELECT id FROM snowflakecredentials""")
# commit_and_close_connection(connection, cursor)


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
