import pyodbc 

# Configure connection string for SQL Server
server = 'SERVERNAME'
database = 'DATABASENAME'
table_name = 'dbo.TABLENAME'
username = 'Username'
password = 'Password'
driver = '{ODBC Driver 17 for SQL Server}'

conn_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# Connect to SQL Server
conn = pyodbc.connect(conn_string)
cursor = conn.cursor()

#Queries
email_search_query = (f"SELECT * FROM {table_name} WHERE email LIKE ?")
name_search_query = (f"SELECT * FROM {table_name} WHERE name LIKE ?")
userid_search_query = (f"SELECT * FROM {table_name} WHERE user_id = ?")
update_query = (f"UPDATE {table_name} SET email = ?, name = ? WHERE user_id = ?")
