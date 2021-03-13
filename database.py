import pyodbc
import pandas as pd


class Connection:
    def __init__(self, driver, server, database, userid, password):
        self.driver = driver
        self.server = server
        self.database = database
        self.UserId = userid
        self.password = password

        # TODO: Trusted=yes DID NOT WORK
        self.connection_string = f'DRIVER={driver};' \
                                 f'SERVER={server};' \
                                 f'DATABASE={database};' \
                                 f'UID={userid};' \
                                 f'PWD={password}'

        self.conn = self.connect()

    def connect(self):
        try:
            conn = pyodbc.connect(self.connection_string)
            print('Connected to the database successfully!')
        except Exception as error:
            conn = None
            print(f'\nFailed to connect to the database! \nError: {str(error)}')
            print(self.connection_string)
            quit()

        return conn

    def run(self, sql_query):
        result = None

        if self.conn:
            # TODO: manage exceptions for queries
            result = pd.read_sql(sql_query, self.conn)
        else:
            print("Something wrong happened, not connected!")

        return result

    def run_via_cursor(self, sql_query):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute(sql_query)

            for row in cursor:
                print(row)

            return cursor
        else:
            print("Something wrong happened, not connected!")
