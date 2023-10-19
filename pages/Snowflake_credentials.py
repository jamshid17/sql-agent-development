import streamlit as st 
from helpers import connect_to_server, make_snowflake_cred_form
from working_with_db.db_functions import get_snowflake_credentials_values

if st.session_state.connected:
    st.info("You are connected to snowflake", icon="ℹ️")

if st.session_state.user_id:
    credentials_values = get_snowflake_credentials_values(st.session_state.user_id)
    print(credentials_values, "s")
    if credentials_values:
        st.info("You already have snowflake credentials")
        st.write(credentials_values)
    else:
        make_snowflake_cred_form(st)

else:
    make_snowflake_cred_form(st)