import streamlit as st 
import pandas as pd
import numpy as np
from helpers import get_manager, check_chat_availability, get_system_prompt, run_sql_code_from_response
import openai, re, time
from conf import system_prompt, base_prompt
import extra_streamlit_components as stx
from working_with_db.db_functions import (
    get_snowflake_credentials_values,
    get_table_inputs_values
)


st.title("☃️ Freezy")

#stating some variables
if "messages" not in st.session_state.keys():    
    st.session_state.messages = []

if 'openai' not in st.session_state:
    st.session_state["openai"] = openai

cookie_manager = get_manager()
user_id = cookie_manager.get("user_id")

openai = st.session_state.openai

openai.api_key = "d3e70cf965e3499c868d5fd0448ecf99"
openai.api_base =  "https://ai-stage1.openai.azure.com/" # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-03-15-preview'

is_available, warning_message = check_chat_availability(user_id)
if is_available:
    #for now, I'm getting the first table inputs 
    table_inputs = get_table_inputs_values(user_id=user_id)[0]
    system_prompt, connection = get_system_prompt(table_inputs=table_inputs)

    if st.session_state.messages == []:
        st.session_state.messages.append({"role": 'system', "content": system_prompt})
        st.session_state.messages.append({"role": "assistant", "content": "How can I help?"})

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])
                results = run_sql_code_from_response(
                    response_content=message['content'],
                    connection=connection
                )
                if results:
                    st.dataframe(results)

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                r = openai.ChatCompletion.create(
                    engine="chatgpt",
                    model="gpt-3.5-turbo",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    temperature=0.1,
                )
                response = r.choices[0].message.content
                st.write(response)
                results = run_sql_code_from_response(
                    response_content=response,
                    connection=connection
                )
                if results:
                    st.dataframe(results)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)

else:
    st.warning(warning_message)



st.write(st.session_state.messages)
