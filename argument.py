import argparse

""" Documentation
    Description:
        Argument is a class with one static method get(), used to read all the arguments from the command line/terminal 
        and read the values and use it in this script, all the arguments related to connecting to the database.
        Verbose flag used to print to the console the status of the script (i.e connected to db, view updated,... etc)
        
        List of argument:
            --driver='db driver'
            --server='db server name'
            --userid='db user'
            --password='user password'
            --database='db name'
            --verbose: if was specified value = True otherwise None
        or you can use the shortcut
            -r='db driver'
            -s='db server name'
            -u='db user'
            -p='user password'
            -d='db name'
            -v: if was specified value = True otherwise None
            
        All the argument are required to run this script, except verbose flag.
    
    Returns:
      object: has the list of parsed argument from CMD/terminal so it will be used later in this script.
"""


class Argument:
    @staticmethod
    def get():
        parser = argparse.ArgumentParser(description="This a program that connects to SQL db and check if a table "
                                                     "changed then update the view on db.", exit_on_error=True)
        parser.add_argument(
            '-r',
            '--driver',
            help='database driver',
            required=True
        )
        parser.add_argument(
            '-s',
            '--server',
            help='database server name',
            required=True
        )
        parser.add_argument(
            '-d',
            '--database',
            help='database name',
            required=True
        )
        parser.add_argument(
            '-u',
            '--userid',
            help='database user ID',
            required=True
        )
        parser.add_argument(
            '-p',
            '--password',
            help='database user password',
            required=True
        )
        parser.add_argument(
            '-v',
            '--verbose',
            help='it will print descriptive messages of the script status, if it was provided.',
            nargs='?',
            const=True,
            type=bool
        )

        return parser.parse_args()
