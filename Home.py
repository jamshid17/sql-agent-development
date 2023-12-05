import streamlit as st 
import pandas as pd
import numpy as np
from helpers import get_manager, check_chat_availability, get_system_prompt, run_sql_code_from_response
import openai, re, time
import extra_streamlit_components as stx
from working_with_db.db_functions import (
    get_table_inputs_values
)
from conf import RECOMMENDED_BTN_MESSAGES
from decouple import config

st.title("☃️ Freezy")

#stating some variables
if "messages" not in st.session_state.keys():    
    st.session_state.messages = []

if 'openai' not in st.session_state:
    st.session_state["openai"] = openai

cookie_manager = get_manager()
user_id = cookie_manager.get("user_id")

openai = st.session_state.openai

openai.api_key = config("OPENAI_API_KEY")
openai.api_base = config("OPENAI_API_BASE") # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = config("OPENAI_API_TYPE")
openai.api_version = config("OPENAI_API_VERSION")



is_available, warning_message = check_chat_availability(user_id)
if is_available:

    table_inputs = get_table_inputs_values(user_id=user_id)
    system_prompt, connection = get_system_prompt(table_inputs=table_inputs)

    #adding deafault messages
    if st.session_state.messages == []:
        st.session_state.messages.append({"role": 'system', "content": system_prompt})
        st.session_state.messages.append({"role": "assistant", "content": "How can I help?"})

    # checking if user has user message
    have_user_message = False
    for message in st.session_state.messages:
        if message["role"] == "user":
            have_user_message = True

    # chat input 
    chat_input = st.chat_input("Chat here")    
    if chat_input:
        st.session_state.messages.append({"role": "user", "content": chat_input})
        
    with st.container():
        first_recommended_prompt_btn = st.button(RECOMMENDED_BTN_MESSAGES[0], disabled=have_user_message)
        second_recommende_prompt_btn = st.button(RECOMMENDED_BTN_MESSAGES[1], disabled=have_user_message)
        third_recommende_prompt_btn = st.button(RECOMMENDED_BTN_MESSAGES[2], disabled=have_user_message)
        recommended_prompt_buttons = [first_recommended_prompt_btn, second_recommende_prompt_btn, third_recommende_prompt_btn]
        for que, recommended_prompt_button in enumerate(recommended_prompt_buttons):
            if recommended_prompt_button:
                st.session_state.messages.append({"role": "user", "content": RECOMMENDED_BTN_MESSAGES[que]})
                have_user_message = True
                st.rerun()
                break
            
    #printing out messages 
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

    # if user sent new message
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                r = openai.ChatCompletion.create(
                    engine="gpt-4",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    temperature=0,
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



# st.write(st.session_state.messages)
