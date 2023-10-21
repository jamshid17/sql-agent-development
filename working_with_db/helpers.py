import psycopg2
import streamlit as st
from .config import (
    create_users_table_table_query,
    create_table_inputs_table_query,
    create_snowflake_credentials_table_query,
)


def connect_with_db():
    conn = psycopg2.connect(
        database="streamlit-app",
        user="user",
        host="localhost",
        password="user",
        port=5432,
    )
    cursor = conn.cursor()
    create_table(cursor)
    return conn, cursor


def commit_and_close_connection(conn, cursor):
    cursor.close()
    conn.commit()
    conn.close()


def check_table_existence(cursor, table_name):
    cursor.execute(
        "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);",
        (table_name,),
    )
    exists = cursor.fetchone()[0]
    if exists:
        return True
    return False


def create_table(cursor):
    if not check_table_existence(cursor, table_name="users"):
        cursor.execute(create_users_table_table_query)
    if not check_table_existence(cursor, table_name="tableinputs"):
        cursor.execute(create_table_inputs_table_query)
    if not check_table_existence(cursor, table_name="snowflakecredentials"):
        cursor.execute(create_snowflake_credentials_table_query)
