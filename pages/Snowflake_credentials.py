import streamlit as st 
from helpers import (
    create_snowflake_credentials, 
    get_manager, 
    get_and_validate_snowflake_credential_values_from_session
)
from working_with_db.db_functions import (
    get_snowflake_credentials_values,
    delete_input,
    update_snowflake_credentials_input,
)
import time 


cookie_manager = get_manager()
user_id = cookie_manager.get("user_id")
time.sleep(0.1)

if user_id:
    credentials_values = get_snowflake_credentials_values(user_id)

    username_value = None
    password_value = None
    azure_account_value = None
    warehouse_value = None
    database_value = None
    schema_value = None
    role_value = None

    if credentials_values:
        (
            credentials_id,
            username_value,
            password_value,
            azure_account_value,
            warehouse_value,
            database_value,
            schema_value,
            role_value,
        ) = credentials_values

    # with st.form("snowflake_credentials_form"):
    if credentials_values:
        st.title("Your snowflake account")
    else:
        st.title("Connect to your snowflake account")
    st.text_input(label="username", key="sn_cred_username", value=username_value)
    st.text_input(
        label="password", key="sn_cred_password", type="password", value=password_value
    )
    st.text_input(
        label="azure-account", key="sn_cred_azure_account", value=azure_account_value
    )
    st.text_input(label="warehouse", key="sn_cred_warehouse", value=warehouse_value)
    st.text_input(label="database", key="sn_cred_database", value=database_value)
    st.text_input(label="schema", key="sn_cred_schema", value=schema_value)
    st.text_input(label="role", key="sn_cred_role", value=role_value)

    if credentials_values:
        update_credentials_button = st.button(
            "update credential values",
            key="update credentials button"
        )
        delete_credentials_button = st.button(
            "delete credential values",
            key="delete credentials button",
        )
    else:
        create_credentials_button = st.button(
            "connect to server",
            key="create credentials button"
        )


    if "update credentials button" in st.session_state:
        if update_credentials_button:
            credential_values = get_and_validate_snowflake_credential_values_from_session(session_state=st.session_state)
            update_snowflake_credentials_input(
                credentials_id=credentials_id,
                credential_values=credential_values,
            )
            st.rerun()            

        if delete_credentials_button:
            delete_input("snowflakecredentials", "id", credentials_id)
            del st.session_state["delete credentials button"]
            del st.session_state["update credentials button"]
            st.rerun()            


    if "create credentials button" in st.session_state:
        if create_credentials_button:
            credential_values = get_and_validate_snowflake_credential_values_from_session(session_state=st.session_state)
            create_snowflake_credentials(
                st=st, 
                user_id=user_id,        
                credential_values=credential_values        
            )
            del st.session_state["create credentials button"]
            # st.rerun()            

else:
    st.warning('You need to login first!')