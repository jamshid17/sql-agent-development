create_users_table_table_query = """
CREATE TABLE Users(
    user_id SERIAL PRIMARY KEY,
    username VARCHAR (50) UNIQUE NOT NULL,
    password VARCHAR (60) NOT NULL
);
"""
create_table_inputs_table_query = """
CREATE TABLE TableInputs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id),
    table_name TEXT UNIQUE NOT NULL,
    table_description TEXT,
    meta_data TEXT
);
"""
create_snowflake_credentials_table_query = """
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

select_user_login_query = """
SELECT user_id, username, password 
FROM users 
WHERE username = '{}';
"""

select_snowflake_credentials_values_query = """
SELECT id, username, password, azure_account, warehouse, database, schema, role 
FROM snowflakecredentials
WHERE user_id = {};
"""

select_table_inputs_values_query = """
SELECT id, user_id, table_name, meta_data, table_description
FROM tableinputs
WHERE user_id = {};
"""

delete_query = """
DELETE FROM {} WHERE {} = {}
"""


# Table inputs queries
update_table_inputs_query = """
UPDATE tableinputs
SET table_name = '{table_name}', table_description = '{table_description}', meta_data = '{meta_data}'
WHERE id = {table_id};
"""

create_table_inputs_query = """
INSERT INTO tableinputs (user_id, table_name, table_description, meta_data) 
VALUES ({user_id}, '{table_name}', '{table_description}', '{meta_data}')
"""


# Snowflake credentials queries
update_snowflake_credentials_query = """
UPDATE SnowflakeCredentials
SET username = '{username}', password = '{password}', azure_account = '{azure_account}', 
warehouse = '{warehouse}', database = '{database}', schema = '{schema}', role = '{role}'
WHERE id = {credentials_id};
"""

create_snowflake_credentials_query = """
INSERT INTO SnowflakeCredentials (user_id, username, password, azure_account, warehouse, database, schema, role) 
VALUES ({user_id}, {username}, {password}, {azure_account}, {warehouse}, {database}, {schema}, {role})
"""


update_user_password_query = """
UPDATE users
SET password = '{hashed_password}'
WHERE user_id = {user_id};
"""


