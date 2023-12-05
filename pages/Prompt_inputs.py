import streamlit as st
import pandas as pd
from helpers import (
    check_prompt_inputs,
    get_manager,
    make_add_new_table_button_state_true,
    cancel_add_new_table_button_state
)
from conf import system_prompt, base_prompt
import openai
import re, time
from working_with_db.db_functions import (
    get_table_inputs_values,
    insert_table_values,
    delete_input,
    update_table_inputs_input,
    create_table_inputs_input,
)
from working_with_db.helpers import connect_with_db, commit_and_close_connection


cookie_manager = get_manager()
user_id = cookie_manager.get("user_id")
time.sleep(0.1)

if user_id:
    results = get_table_inputs_values(user_id)
    st.header("Your Snowflake Tables!")
    for result in results:
        table_input_id = result[0]
        with st.form(f"table_form_{table_input_id}"):
            table_name_key = f"table_name_input_{table_input_id}"
            metadata_query_key = (f"metadata_query_input_{table_input_id}",)
            table_description_key = f"table_description_input_{table_input_id}"

            st.text_input("TABLE NAME", key=table_name_key, value=result[2])
            st.text_input("METADATA_QUERY", key=metadata_query_key, value=result[3])
            st.text_area(
                "TABLE_DESCRIPTION", key=table_description_key, value=result[4]
            )
            update_table_inputs_button = st.form_submit_button("Save")
            delete_table_inputs_button = st.form_submit_button(
                "Delete",
                on_click=delete_input,
                args=["tableinputs", "id", table_input_id],
            )
        if update_table_inputs_button:
            update_table_inputs_input(
                table_id=table_input_id,
                table_name=st.session_state[table_name_key],
                meta_data=st.session_state[metadata_query_key],
                table_description=st.session_state[table_description_key],
            )
    # adding new table inputs
    if "add_table_button_state" not in st.session_state:
        st.session_state["add_table_button_state"] = False
    if "disable_add_table_button" not in st.session_state:
        st.session_state["disable_add_table_button"] = False

    add_table_button = st.button(
        label="Add new table input",
        key="add_table_input",
        on_click=make_add_new_table_button_state_true,
        disabled=st.session_state.disable_add_table_button,
    )

    if add_table_button or st.session_state.add_table_button_state:
        with st.form("create_new_table_form", clear_on_submit=True):
            st.header("Add new table")
            st.text_input("TABLE NAME", key="new_table_input")
            st.text_input("METADATA_QUERY", key="new_metadata_query")
            st.text_area("TABLE_DESCRIPTION", key="new_table_description")
            create_table_inputs_button = st.form_submit_button("Add")
            cancel_create_table_inputs_button = st.form_submit_button("Cancel", on_click=cancel_add_new_table_button_state)

        if create_table_inputs_button:
            st.write(st.session_state.new_table_input)
            create_table_inputs_input(
                user_id,
                st.session_state["new_table_input"],
                st.session_state["new_table_description"],
                st.session_state["new_metadata_query"],
            )
            st.session_state.add_table_button_state = False
            cancel_add_new_table_button_state()
            st.rerun()

else:
    st.warning("You need to login first!")

#     submit_columns_button = st.form_submit_button("get columns")


# table_desc = """This table has various metrics for financial entities (also referred to as banks) since 1983.
# The user may describe the entities interchangeably as banks, financial institutions, or financial entities.
# """
# meta_data_query = "SELECT VARIABLE_NAME, DEFINITION FROM FREEZY_SAMPLE.CYBERSYN_FINANCIAL.FINANCIAL_ENTITY_ATTRIBUTES_LIMITED;"


# insert_table_values(user_id, qualified_table_name="test", metadata="meta_data_query", table_description="table_desc")


# with st.form("table_form"):
# st.text_input("QUALIFIED TABLE NAME", key="qualified_table_name_input", value="FREEZY_SAMPLE.CYBERSYN_FINANCIAL.FINANCIAL_ENTITY_ANNUAL_TIME_SERIES")
#     st.text_area("TABLE_DESCRIPTION", key="table_description_input", value=table_desc)
#     st.text_input("METADATA_QUERY", key="metadata_query_input", value=meta_data_query)
#     # st.text_input("Query for prompt", key="query_for_prompt", value="Which financial institutions in California had the highest total assets value between 2010 to 2015?")
#     submit_columns_button = st.form_submit_button("get columns")

# if submit_columns_button:

#     is_error, error_message = check_prompt_inputs(st)
#     if is_error:
#         st.warning(error_message, icon="🚨")
#     else:
#         st.session_state.table_is_filled = True
#         st.session_state["qualified_table_name"] = st.session_state.qualified_table_name_input
#         st.session_state["table_description"] = st.session_state.table_description_input
# st.session_state["metadata_query"] = st.session_state.metadata_query_input
