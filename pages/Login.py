import streamlit_authenticator as stauth
import streamlit as st
import yaml, time
from yaml.loader import SafeLoader
from working_with_db.db_functions import user_login
from helpers import get_manager, verify_password


cookie_manager = get_manager()
time.sleep(0.1)

user_id = cookie_manager.get('user_id')
if user_id:
    st.info("You are logged in!") 
    logout_button = st.button("Log Out")

    if logout_button:
        cookie_manager.delete("user_id")
    
else:
    with st.form("Login"):
        st.text_input("Username", key="login_username")
        st.text_input("Password", key="login_password", type="password")
        # st.text_input("Query for prompt", key="query_for_prompt", value="Which financial institutions in California had the highest total assets value between 2010 to 2015?")
        login_button = st.form_submit_button("Login")


    if login_button:
        if not user_id:
            entered_username = st.session_state["login_username"]
            entered_password = st.session_state["login_password"]
            # print(entered_password, " et pas")
            
            login_result = user_login(st.session_state["login_username"])

            if login_result:
                user_id = login_result[0]
                password = login_result[2]
                print(password, " pas")
                print(entered_password, " et pas")

                if verify_password(password, entered_password):             
                    cookie_manager.set(cookie="user_id", val=user_id)
                    st.info("Logged In!")
                else:
                    st.warning("Password is incorrect!")
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