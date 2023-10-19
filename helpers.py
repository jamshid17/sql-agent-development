from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from working_with_db.db_functions import insert_credential_values



def connect_to_server(st):
    username = st.session_state.username
    password = st.session_state.password
    azure_account = st.session_state.azure_account
    warehouse = st.session_state.warehouse
    database = st.session_state.database
    schema = st.session_state.schema
    role = st.session_state.role
    # if '' in [username, password, azure_account, warehouse, database, schema, role]:
    if False:
        st.warning("Input all credentials", icon="🚨")
    else:
        # url = URL(
        #     user=username,
        #     password=password,
        #     account=azure_account,
        #     warehouse=warehouse,
        #     database=database,
        #     schema=schema,
        #     role=role
        # )
        url = URL(
            user='fmukhutdinov',
            password='t23@ys_1Wh2uw!uI',
            account='ee30191.uk-south.azure',
            warehouse='COMPUTE_WH',
            database='FREEZY_SAMPLE',
            schema='CYBERSYN_FINANCIAL',
            role = 'ACCOUNTADMIN'
        )
        
        engine = create_engine(url)
        try:
            connection = engine.connect()
            st.session_state.connection = connection
            st.session_state.connected = True
            insert_credential_values(
                user_id=st.session_state.user_id,
                username='fmukhutdinov',
                password='t23@ys_1Wh2uw!uI',
                azure_account='ee30191.uk-south.azure',
                warehouse='COMPUTE_WH',
                database='FREEZY_SAMPLE',
                schema='CYBERSYN_FINANCIAL',
                role = 'ACCOUNTADMIN'
            )

        except DatabaseError as e:
            st.warning("Wrong credentials", icon="🚨")
    

def check_prompt_inputs(st):
    is_error = False
    error_message = ''
    table_name = st.session_state.qualified_table_name_input
    table_description = st.session_state.table_description_input

    if table_name == '':
        is_error = True
        error_message = "Input Table Name"
        return is_error, error_message
    if len(table_name.split(".")) < 3:
        is_error = True
        error_message = "Input table name correctly: it must include 3 '.'"
            
    if table_description == '':
        is_error = True
        error_message = "Input Table description"
        return is_error, error_message
    
    return is_error, error_message

def make_snowflake_cred_form(st):
    with st.form("snowflake_credentials_form"):
        st.title("Connect to your snowflake account")
        st.text_input(label="username", key="username")
        st.text_input(label="password", key="password", type="password")
        st.text_input(label="azure-account", key="azure_account")
        st.text_input(label="warehouse", key="warehouse")
        st.text_input(label="database", key="database")
        st.text_input(label="schema", key="schema")
        st.text_input(label="role", key="role")
        st.form_submit_button("connect to server", on_click=connect_to_server, args=[st])
