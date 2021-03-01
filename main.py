import argparse
from Database import Connection


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--driver', help='driver')
    parser.add_argument('--server', help='server name')
    parser.add_argument('--database', help='database name')
    parser.add_argument('--userid', help='userID')
    parser.add_argument('--password', help='User password')
    args = parser.parse_args()

    # test connecting to the database
    conn = Connection(args.driver, args.server, args.database, args.userid, args.password)
    conn.run('SELECT * FROM [User]')

    #TODO: implement the stored prodcedure here (separate class and call here)
    # first call the get the table data (seralize and save to file)
    # next calls compare the seralized


if __name__ == '__main__':
    main()
