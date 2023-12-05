from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from working_with_db.db_functions import (
    insert_credential_values,
    get_snowflake_credentials_values,
    get_table_inputs_values,
)
import extra_streamlit_components as stx
import streamlit as st
import pandas as pd
from conf import system_prompt
import re
import bcrypt
import time


# @st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    cookie_manager = stx.CookieManager()
    cookie_manager.get_all()
    return cookie_manager


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(stored_password, provided_password):
    # for now it checks without encryption
    if stored_password == provided_password:
        return True
    return False
    # return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))


def create_snowflake_credentials(st, user_id, credential_values):
    # if '' in [username, password, azure_account, warehouse, database, schema, role]:
    if False:
        st.warning("Input all credentials", icon="🚨")
    else:
        url = URL(
            user=credential_values["username"],
            password=credential_values["password"],
            account=credential_values["azure_account"],
            warehouse=credential_values["warehouse"],
            database=credential_values["database"],
            schema=credential_values["schema"],
            role=credential_values["role"]
        )

        engine = create_engine(url)
        try:
            engine.connect()
        except DatabaseError as e:
            st.warning("Wrong credentials", icon="🚨")
            time.sleep(5)
        else:
            insert_credential_values(
                user_id=user_id,
                username=credential_values["username"],
                password=credential_values["password"],
                azure_account=credential_values["azure_account"],
                warehouse=credential_values["warehouse"],
                database=credential_values["database"],
                schema=credential_values["schema"],
                role=credential_values["role"],
            )


@st.cache_resource
def connect_to_snowflake_server(snowflake_credentials):
    (
        username,
        password,
        azure_account,
        warehouse,
        database,
        schema,
        role,
    ) = snowflake_credentials[1:]
    url = URL(
        user=username,
        password=password,
        account=azure_account,
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role,
    )
    engine = create_engine(url)
    connection = engine.connect()
    return connection, engine


def check_prompt_inputs(st):
    is_error = False
    error_message = ""
    table_name = st.session_state.qualified_table_name_input
    table_description = st.session_state.table_description_input

    if table_name == "":
        is_error = True
        error_message = "Input Table Name"
        return is_error, error_message
    if len(table_name.split(".")) < 3:
        is_error = True
        error_message = "Input table name correctly: it must include 3 '.'"

    if table_description == "":
        is_error = True
        error_message = "Input Table description"
        return is_error, error_message

    return is_error, error_message


def get_and_validate_snowflake_credential_values_from_session(session_state):
    return {
        "username": session_state["sn_cred_username"],
        "password": session_state["sn_cred_password"],
        "azure_account": session_state["sn_cred_azure_account"],
        "warehouse": session_state["sn_cred_warehouse"],
        "database": session_state["sn_cred_database"],
        "schema": session_state["sn_cred_schema"],
        "role": session_state["sn_cred_role"],
    }


def check_chat_availability(user_id):
    is_available = False
    warning_message = None
    if not user_id:
        warning_message = "You must log in to start a chat!"
        return is_available, warning_message
    else:
        credentials_values = get_snowflake_credentials_values(user_id)
        if not credentials_values:
            warning_message = "You must insert snowflake credentials!"
            return is_available, warning_message
        else:
            table_input_values = get_table_inputs_values(user_id)
            if not table_input_values:
                warning_message = "You do not have any snowflake table!"
                return is_available, warning_message
            else:
                is_available = True
                return is_available, warning_message


@st.cache_resource
def get_system_prompt(table_inputs):
    full_context = ""
    user_id = table_inputs[0][1]
    snowflake_credentials = get_snowflake_credentials_values(user_id=user_id)

    for table_input in table_inputs:
        user_id, table_name, metadata_query, table_description = table_input[1:]
        table_str_list = table_name.split(".")
        query = f"""
            SELECT COLUMN_NAME, DATA_TYPE FROM {table_str_list[0].upper()}.INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = '{table_str_list[1].upper()}' AND TABLE_NAME = '{table_str_list[2].upper()}'
            """
        # connection = st.session_state.connection

        connection, engine = connect_to_snowflake_server(snowflake_credentials)
        columns = pd.read_sql(query, connection)
        columns = "\n".join(
            [
                f"- **{columns['column_name'][i]}**: {columns['data_type'][i]}"
                for i in range(len(columns["column_name"]))
            ]
        )
        context = f"""
        Here is the table name <tableName> {'.'.join(table_str_list)} </tableName>

        <tableDescription>{table_description}</tableDescription>

        Here are the columns of the {'.'.join(table_str_list)}

        <columns>\n\n{columns}\n\n</columns>
        """
        full_context += context + "\n\n\n"

    # if metadata_query != '':
    #     print(metadata_query)
    #     metadata = pd.read_sql(metadata_query, connection)

    #     # metadata = connection.query(metadata_query)
    #     metadata = "\n".join(
    #         [
    #             f"- **{metadata['VARIABLE_NAME'][i]}**: {metadata['DEFINITION'][i]}"
    #             for i in range(len(metadata["VARIABLE_NAME"]))
    #         ]
    #     )
    #     context = context + f"\n\nAvailable variables by VARIABLE_NAME:\n\n{metadata}"

    full_system_prompt = system_prompt.format(full_context)

    return full_system_prompt, connection


# def removing_sql_code_from_response(response_content):
#     sql_match = re.search(r"```sql\n(.*)\n```", response_content, re.DOTALL)
#     if sql_match:
#         sql = sql_match.group(1)


def run_sql_code_from_response(response_content, connection):
    sql_match = re.search(r"```sql\n(.*)\n```", response_content, re.DOTALL)
    if sql_match:
        sql = sql_match.group(1)
        # conn = st.experimental_connection("snowpark")
        results = pd.read_sql(sql, connection)
        st.dataframe(results)


def make_add_new_table_button_state_true():
    st.session_state.add_table_button_state = True
    st.session_state.disable_add_table_button = True


def cancel_add_new_table_button_state():
    st.session_state["add_table_button"] = False
    st.session_state["add_table_button_state"] = False
    st.session_state["disable_add_table_button"] = False


def get_include_tables(table_inputs):
    include_tables = []
    for table_input in table_inputs:
        full_table_name = table_input[2]
        table_name = full_table_name.split(".")[-1].lower()
        include_tables.append(table_name)
    return include_tables


def get_choices_from_agent_content(content):
    return None

def get_output_name_from_agent_content(content):
    return None

def download_output_table(connection, snowflake_credentials, output_table_name):
    database_name = snowflake_credentials[4]
    schema = snowflake_credentials[5]

    sql_query = f"SELECT * FROM {database_name}.{schema}.{output_table_name.upper()}"
    df = pd.read_sql(sql_query, connection)
    df.to_csv(f'files/{output_table_name}.csv', index=False)

