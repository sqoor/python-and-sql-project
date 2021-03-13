import argparse


class Argument:
    def __init__(self):
        pass

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

        return parser.parse_args()
