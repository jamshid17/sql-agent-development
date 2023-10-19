import streamlit as st 
import pandas as pd
import numpy as np
from helpers import connect_to_server
import openai, re
from conf import system_prompt, base_prompt

st.title("☃️ Freezy")

#stating some variables
if 'connected' not in st.session_state:
    st.session_state['connected'] = True

if 'table_is_filled' not in st.session_state:
    st.session_state['table_is_filled'] = False

if "messages" not in st.session_state.keys():    
    st.session_state.messages = []

if 'openai' not in st.session_state:
    st.session_state["openai"] = openai

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None


openai = st.session_state.openai

openai.api_key = "56cca713540840d59d2e01b7b81830df"
openai.api_base =  "https://ai-stage1.openai.azure.com/" # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-03-15-preview'

if not st.session_state.connected:
    st.warning("You are not connected to snowflake", icon="ℹ️")
if not st.session_state.table_is_filled:    
    st.warning("You did not enter table input", icon="ℹ️")


if st.session_state.table_is_filled:
    table_name = st.session_state.qualified_table_name
        
    table_str_list = table_name.split(".")
    query = f"""
        SELECT COLUMN_NAME, DATA_TYPE FROM {table_str_list[0].upper()}.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{table_str_list[1].upper()}' AND TABLE_NAME = '{table_str_list[2].upper()}'
        """
    connection = st.session_state.connection
    columns = pd.read_sql(query, connection)
    columns = "\n".join(
        [
            f"- **{columns['column_name'][i]}**: {columns['data_type'][i]}"
            for i in range(len(columns["column_name"]))
        ]
    )
    table_description = st.session_state.table_description
    context = f"""
    Here is the table name <tableName> {'.'.join(table_str_list)} </tableName>

    <tableDescription>{table_description}</tableDescription>

    Here are the columns of the {'.'.join(table_str_list)}

    <columns>\n\n{columns}\n\n</columns>
    """
    # metadata_query = st.session_state.metadata_query
    # if metadata_query != '':
    #     metadata = connection.query(metadata_query)
    #     metadata = "\n".join(
    #         [
    #             f"- **{metadata['VARIABLE_NAME'][i]}**: {metadata['DEFINITION'][i]}"
    #             for i in range(len(metadata["VARIABLE_NAME"]))
    #         ]
    #     )
    #     context = context + f"\n\nAvailable variables by VARIABLE_NAME:\n\n{metadata}"
    system_prompt = system_prompt.format(context)
    if st.session_state.messages == []:
        st.session_state.messages.append({"role": 'system', "content": system_prompt})
        st.session_state.messages.append({"role": "assistant", "content": "How can I help?"})
    

if st.session_state.connected and st.session_state.table_is_filled:
    print("herer ww go")
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])
                sql_match = re.search(r"```sql\n(.*)\n```", message["content"], re.DOTALL)
                if sql_match:
                    sql = sql_match.group(1)
                    # conn = st.experimental_connection("snowpark")
                    results = pd.read_sql(sql, connection)
                    st.dataframe(results)


    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                r = openai.ChatCompletion.create(
                    engine="chatgpt",
                    model="gpt-3.5-turbo",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                )
                response = r.choices[0].message.content
                st.write(response)
            # response = openai.Completion.create(engine="chatgpt", prompt=prompt, temperature=0.1, max_tokens=1024)
            # response_text = response['choices'][0]['text'].strip()
            # st.write(response_text)
            # Parse the response for a SQL query and execute if available
                sql_match = re.search(r"```sql\n(.*)\n```", response, re.DOTALL)
                if sql_match:
                    print("there is match!")
                    sql = sql_match.group(1)
                    # conn = st.experimental_connection("snowpark")
                    results = pd.read_sql(sql, connection)
                    st.dataframe(results)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)


st.write(st.session_state.messages)
