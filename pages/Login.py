import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader
from working_with_db.db_functions import user_login



if st.session_state.user_id:
    st.info("You logged in!") 
else:
    with st.form("Login"):
        st.text_input("Username", key="login_username")
        st.text_input("Password", key="login_password")
        # st.text_input("Query for prompt", key="query_for_prompt", value="Which financial institutions in California had the highest total assets value between 2010 to 2015?")
        login_button = st.form_submit_button("Login")


    if login_button:
        if not st.session_state.user_id:
            login_result = user_login(st.session_state["login_username"], st.session_state["login_password"])
            if login_result:
                user_id = login_result[0]
                st.session_state.user_id = user_id
                st.info("Logged In!")
            else:
                st.warning("User not found!")



# with open('.streamlit/config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )
# authenticator.login('Login', 'main')
# if st.session_state["authentication_status"]:
#     authenticator.logout('Logout', 'main', key='unique_key')
#     st.write(f'Welcome *{st.session_state["name"]}*')
#     st.title('Some content')
# elif st.session_state["authentication_status"] is False:
#     st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] is None:
#     st.warning('Please enter your username and password')