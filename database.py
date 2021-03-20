import pyodbc
import pandas as pd

""" Documentation: Connection
   Description:
       a class used to connect to database using pyodbc package.

   Parameters:
     driver: database driver
     server: database server name
     database: database name
     userid: database user name/id
     password: user password

   Returns:
     object: connection object so you can execute sql queries to the provided database.
"""


class Connection:
    def __init__(self, driver, server, database, userid, password):
        self.driver = driver
        self.server = server
        self.database = database
        self.UserId = userid
        self.password = password
        self.connection_string = f'DRIVER={driver};' \
                                 f'SERVER={server};' \
                                 f'DATABASE={database};' \
                                 f'UID={userid};' \
                                 f'PWD={password}'

        self.conn = self.connect()

    """ Documentation: connect
       Description:
           used to connect to database using pyodbc package.

       Returns:
         object: connection object so you can execute sql queries to the provided database.
    """
    def connect(self):
        try:
            conn = pyodbc.connect(self.connection_string)
            print('Connected to the database successfully!')
        except Exception as err:
            conn = None
            print(f'\nFailed to connect to the database! \nError: {str(err)}')
            print(self.connection_string)
            quit()

        return conn

    """ Documentation: run
    Description:
        a public method, execute select query using pandas and return the dataframe.
    
    Parameters:
        sql_query (string): string representing select SQL query.

    Returns:
        object(dataframe): result select query from the database as a dataframe.
    """
    def run(self, sql_query):
        result = None

        if self.conn:
            try:
                result = pd.read_sql(sql_query, self.conn)
            except Exception as err:
                print("was not able to run the query", sql_query)
                print("Error:", str(err))
                quit()
        else:
            print("Something wrong happened, not connected!")

        return result

    """ Documentation: run_via_cursor
     Description:
         a public method, execute select query using cursor of pyodbc and return the object result.

     Parameters:
         sql_query (string): string representing select SQL query.

     Returns:
         object: result select query from the database as a object.
     """
    def run_via_cursor(self, sql_query):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(sql_query)

                for row in cursor:
                    print(row)

                return cursor
            except Exception as err:
                print("Was not able to execute the query via the cursor")
                print("Error:", str(err))
                quit()
        else:
            print("Something wrong happened, not connected!")

    """ Documentation: create
      Description:
          a public method, execute select query using cursor of pyodbc and create new structure in the database
          table, view, ... etc, you can execute select queries here but won't return anything.

      Parameters:
          sql_query (string): string representing DDL SQL query.
    """
    def create(self, sql_query):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(sql_query)
                self.conn.commit()
            except Exception as err:
                print('Was not able to create view', sql_query)
                print("Error:", str(err))
                quit()
        else:
            print("Something wrong happened, not connected!")