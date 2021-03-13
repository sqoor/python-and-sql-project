import _utils

try:
    import pandas as pd
    from argument import Argument
    from database import Connection
except ModuleNotFoundError:
    _utils.InstallPackages({'pandas', 'argparse', 'pyodbc'})

    import pandas as pd
    from argument import Argument
    from database import Connection


def main():
    args = Argument.get()

    # test connecting to the database
    conn = Connection(args.driver, args.server, args.database, args.userid, args.password)
    result_df = conn.run('SELECT * FROM [SurveyStructure]')

    print(result_df)
    x = pd.read_pickle('result.pkl')  # if "result.pkl" existed
    print(result_df.compare(x))  # error if x not existed or result_df

    result_df.to_pickle('result.pkl')

    # TODO: implement the stored procedure here (separate class and call here)
    # first call the get the table data (serialize and save to file)
    # next calls compare the serialized


if __name__ == '__main__':
    main()
