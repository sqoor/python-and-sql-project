import pyodbc
import pandas as pd
from tools import Verbose

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
            Verbose.print_ln('Connected to the database successfully!')
        except Exception as err:
            conn = None
            Verbose.print_ln(f'\nFailed to connect to the database! \nError: {str(err)}')
            Verbose.print_ln(self.connection_string)
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
                Verbose.print_ln("Was not able to run the query", sql_query)
                Verbose.print_ln("Error:", str(err))
                quit()
        else:
            Verbose.print_ln("Something wrong happened, not connected!")

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
                    Verbose.print_ln(row)

                return cursor
            except Exception as err:
                Verbose.print_ln("Was not able to execute the query via the cursor")
                Verbose.print_ln("Error:", str(err))
                quit()
        else:
            Verbose.print_ln("Something wrong happened, not connected!")

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
                Verbose.print_ln('Was not able to create view', sql_query)
                Verbose.print_ln("Error:", str(err))
                quit()
        else:
            Verbose.print_ln("Something wrong happened, not connected!")