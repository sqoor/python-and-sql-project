import argparse
import sys


class Argument:
    def __init__(self):
        print("arguments")

    @staticmethod
    def get():
        parser = argparse.ArgumentParser(description="This a program that connects to SQL db and check if a table "
                                                     "changed then update the view on db.", exit_on_error=True)
        parser.add_argument('driver', help='database driver')
        parser.add_argument('server', help='database server name')
        parser.add_argument('database', help='database name')
        parser.add_argument('userid', help='database user ID')
        parser.add_argument('password', help='database user password')

        print(parser.parse_args())
        print(type(parser.parse_args()))

        return parser.parse_args()
