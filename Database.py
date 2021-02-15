import pyodbc 
import pandas as pd

# TODO make program OOP, manage the exeptions, DRY & KISS

driver = '{ODBC Driver 17 for SQL Server}'
server = 'ABDULLAH\\SQL2019'
database = 'Survey_Sample_A19'
# TODO: text obfuscation for password and username encryption
UserId = 'sa'
password = '123456'

# TODO: Trusted=yes DID NOT WORK
connection_string = f'DRIVER={driver};' \
                    f'SERVER={server};' \
                    f'DATABASE={database};' \
                    f'UID={UserId};' \
                    f'PWD={password}'


try:
    conn = pyodbc.connect(connection_string)
    print('Connected to the database successfully!')
except Exception as error:
    conn = None
    print(f'Failed to connect to the database! \nError: {str(error)}')


# if conn:
#     cursor = conn.cursor()
#     sql_query_all_users = 'SELECT * FROM [User]'
#     cursor.execute(sql_query_all_users)
#
#     for row in cursor:
#         print(row)

if conn:
    cursor = conn.cursor()
    sql_all_users = 'SELECT * FROM [User]'
    # TODO: manage exceptions for queries
    df_all_users = pd.read_sql(sql_all_users, conn)
    print(df_all_users.head(3))


