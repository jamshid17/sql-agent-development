users_table_create_query = """
CREATE TABLE Users(
    user_id SERIAL PRIMARY KEY,
    username VARCHAR (50) UNIQUE NOT NULL,
    password VARCHAR (50) NOT NULL
);
"""
table_input_create_query = """
CREATE TABLE TableInputs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id),
    table_name TEXT NOT NULL,
    table_description TEXT,
    meta_data TEXT
);
"""
snowflake_credentials_create_query = """
CREATE TABLE SnowflakeCredentials(
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    username VARCHAR (100) NOT NULL,
    password VARCHAR (100) NOT NULL,
    azure_account VARCHAR (512) NOT NULL,
    warehouse VARCHAR (100) NOT NULL,
    database VARCHAR (100) NOT NULL,
    schema VARCHAR (100) NOT NULL,
    role VARCHAR (100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
"""

user_login_query = """
SELECT user_id, username, password 
FROM users 
WHERE username = '{}' AND password = '{}';
"""

table_values_query = """
SELECT id, table_name, table_description, metadata 
FROM tableinputs 
WHERE user_id = {};
"""

snowflake_credentials_values_query = """
SELECT id, username, password, azure_account, warehouse, database, schema, role 
FROM snowflakecredentials
WHERE user_id = {};
"""