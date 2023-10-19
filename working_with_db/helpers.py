import psycopg2 
import streamlit as st
from .config import (
    users_table_create_query, 
    table_input_create_query, 
    snowflake_credentials_create_query
)

def connect_with_db():
    conn = psycopg2.connect(database = "streamlit-app", 
                            user = "user", 
                            host= 'localhost',
                            password = "user",
                            port = 5432)
    cursor = conn.cursor()
    create_table(cursor)
    return conn, cursor


def commit_and_close_connection(conn, cursor):
    cursor.close()
    conn.commit()
    conn.close()
    

def check_table_existence(cursor, table_name):
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);", (table_name,))
    exists = cursor.fetchone()[0]
    if exists:
        return True
    return False


def create_table(cursor):
    if not check_table_existence(cursor, table_name="users"):
        print("herer")
        cursor.execute(users_table_create_query)
    if not check_table_existence(cursor, table_name="tableinputs"):
        cursor.execute(table_input_create_query)
    if not check_table_existence(cursor, table_name="snowflakecredentials"):
        cursor.execute(snowflake_credentials_create_query)
