import time
import streamlit as st
from agent.agent import create_agent, connect_with_langchain_db, clean_chat_memory
from helpers import (
    get_manager,
    get_include_tables,
    connect_to_snowflake_server,
    get_choices_from_agent_content,
    get_output_name_from_agent_content,
    download_output_table
)

from working_with_db.db_functions import (
    get_table_inputs_values,
    get_snowflake_credentials_values,
)
from datetime import datetime

st.title("☃️ SQL Agent")
st.button("Clear history", on_click=clean_chat_memory)
if "agent_message_history" not in st.session_state.keys():
    st.session_state.agent_message_history = []

cookie_manager = get_manager()
user_id = cookie_manager.get("user_id")
if user_id == None:
    st.warning("You must login to start a chat")
else:
    table_inputs = get_table_inputs_values(user_id=user_id)
    include_tables = get_include_tables(table_inputs)
    snowflake_credentials = get_snowflake_credentials_values(user_id=user_id)
    connection, engine = connect_to_snowflake_server(snowflake_credentials)

    table_inputs = get_table_inputs_values(user_id=user_id)
    with st.spinner("Getting tables..."):
        connection_db = connect_with_langchain_db(engine, include_tables)

    agent_executor, memory = create_agent(connection_db)
    for message in memory.chat_memory.messages:
        with st.chat_message(message.type):
            st.write(message.content)
            choices = get_choices_from_agent_content(message.content)
            if choices:
                for choice in choices:
                    st.write(choices)
            output_name = get_output_name_from_agent_content(message.content)
            if output_name:
                download_button = st.button("Download", on_click=download_output_table)

    chat_input = st.chat_input("Chat here")
    if chat_input:
        with st.chat_message('human'):
            st.write(chat_input) 
        
        with st.spinner("Thinking..."):
            response = agent_executor.invoke({"input": chat_input})
            output = response["output"]
            with st.chat_message('ai'):
                st.write(output) 
            choices = get_choices_from_agent_content(output)
            if choices:
                for choice in choices:
                    st.write(choices)
