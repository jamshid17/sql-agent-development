import streamlit as st
import pandas as pd 
from helpers import check_prompt_inputs
from conf import system_prompt, base_prompt
import openai
import re

table_desc = """This table has various metrics for financial entities (also referred to as banks) since 1983.
The user may describe the entities interchangeably as banks, financial institutions, or financial entities.
"""
meta_data_query = "SELECT VARIABLE_NAME, DEFINITION FROM FREEZY_SAMPLE.CYBERSYN_FINANCIAL.FINANCIAL_ENTITY_ATTRIBUTES_LIMITED;"


with st.form("table_form"):
    st.text_input("QUALIFIED TABLE NAME", key="qualified_table_name_input", value="FREEZY_SAMPLE.CYBERSYN_FINANCIAL.FINANCIAL_ENTITY_ANNUAL_TIME_SERIES")
    st.text_area("TABLE_DESCRIPTION", key="table_description_input", value=table_desc)
    st.text_input("METADATA_QUERY", key="metadata_query_input", value=meta_data_query)
    # st.text_input("Query for prompt", key="query_for_prompt", value="Which financial institutions in California had the highest total assets value between 2010 to 2015?")
    submit_columns_button = st.form_submit_button("get columns")

if submit_columns_button:
    if st.session_state.connected:
        is_error, error_message = check_prompt_inputs(st)
        if is_error:
            st.warning(error_message, icon="🚨")
        else:
           st.session_state.table_is_filled = True
           st.session_state["qualified_table_name"] = st.session_state.qualified_table_name_input
           st.session_state["table_description"] = st.session_state.table_description_input
           st.session_state["metadata_query"] = st.session_state.metadata_query_input
    else:
        st.warning("Not connected to snowflake", icon="🚨")

