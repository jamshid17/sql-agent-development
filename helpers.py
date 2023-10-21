from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from working_with_db.db_functions import (
    insert_credential_values,
    get_snowflake_credentials_values,
    get_table_inputs_values
)
import extra_streamlit_components as stx
import streamlit as st
import pandas as pd
from conf import system_prompt
import re


# @st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    cookie_manager = stx.CookieManager()
    cookie_manager.get_all()
    return cookie_manager


def create_snowflake_credentials(st, user_id, credential_values):
    # if '' in [username, password, azure_account, warehouse, database, schema, role]:
    if False:
        st.warning("Input all credentials", icon="🚨")
    else:
        # url = URL(
        #     user=credential_values["username"],
        #     password=credential_values["password"],
        #     account=credential_values["azure_account"],
        #     warehouse=credential_values["warehouse"],
        #     database=credential_values["database"],
        #     schema=credential_values["schema"],
        #     role=credential_values["role"]
        # )
        url = URL(
            user="fmukhutdinov",
            password="t23@ys_1Wh2uw!uI",
            account="ee30191.uk-south.azure",
            warehouse="COMPUTE_WH",
            database="FREEZY_SAMPLE",
            schema="CYBERSYN_FINANCIAL",
            role="ACCOUNTADMIN",
        )

        engine = create_engine(url)
        try:
            engine.connect()
        except DatabaseError as e:
            st.warning("Wrong credentials", icon="🚨")
        else:
            insert_credential_values(
                user_id=user_id,
                username="fmukhutdinov",
                password="t23@ys_1Wh2uw!uI",
                azure_account="ee30191.uk-south.azure",
                warehouse="COMPUTE_WH",
                database="FREEZY_SAMPLE",
                schema="CYBERSYN_FINANCIAL",
                role="ACCOUNTADMIN",
            )

@st.cache_resource
def connect_to_server(snowflake_credentials):
    username, password, azure_account, warehouse, database, schema, role = snowflake_credentials[1:]
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
    return connection 


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
        "username":session_state["sn_cred_username"],
        "password":session_state["sn_cred_password"],
        "azure_account":session_state["sn_cred_azure_account"],
        "warehouse":session_state["sn_cred_warehouse"],
        "database":session_state["sn_cred_database"],
        "schema":session_state["sn_cred_schema"],
        "role":session_state["sn_cred_role"],
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


def get_system_prompt(table_inputs):
    user_id, table_name, metadata_query, table_description = table_inputs[1:]
    table_str_list = table_name.split(".")
    query = f"""
        SELECT COLUMN_NAME, DATA_TYPE FROM {table_str_list[0].upper()}.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{table_str_list[1].upper()}' AND TABLE_NAME = '{table_str_list[2].upper()}'
        """
    # connection = st.session_state.connection
    snowflake_credentials = get_snowflake_credentials_values(user_id=user_id)
    connection = connect_to_server(snowflake_credentials)
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

    full_system_prompt = system_prompt.format(context)

    return full_system_prompt, connection


def run_sql_code_from_response(response_content, connection):
    sql_match = re.search(r"```sql\n(.*)\n```", response_content, re.DOTALL)
    if sql_match:
        sql = sql_match.group(1)
        # conn = st.experimental_connection("snowpark")
        results = pd.read_sql(sql, connection)
        st.dataframe(results)