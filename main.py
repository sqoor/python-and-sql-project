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
    pkl_df = None
    db_updated = False
    first_run = False

    args = Argument.get()

    # test connecting to the database
    conn = Connection(args.driver, args.server, args.database, args.userid, args.password)

    db_df = conn.run('SELECT * FROM [SurveyStructure]')
    println(db_df, 'db dataframe')

    try:
        pkl_df = pd.read_pickle('result.pkl')  # if "result.pkl" existed!! exception
        println(pkl_df, 'pkl dataframe')
        db_updated = pkl_df.shape != db_df.shape or not pkl_df.equals(db_df)
        if db_updated:
            print("db changed...")
    except FileNotFoundError:
        print('first run...')
        # save a pkl file run getAllSurevyData then update the view
        first_run = pkl_df is None
    except Exception as err:
        print("something went bad: ", err)

    # println(pd.contains, 'compare pkl with db DFs')  # error if x not existed or result_df

    if first_run or db_updated:
        # update the pkl file (to compare with db)
        # run the getAllSurveyData function
        # update the view
        db_df.to_pickle('result.pkl')
        print("update the view and the pkl")
    else:
        # do nothing
        print("nothing changed in the db table")

    # TODO: implement the stored procedure here (separate class and call here)
    # first call the get the table data (serialize and save to file)
    # next calls compare the serialized


def println(arg, name=''):
    print("\n\n")
    if name:
        print(f'{name}:')
    print(arg)
    print("\n\n\n")


def test():
    data1 = {
        'col': [1, 2, 3, 4],
        'col2': [5, 6, 7, 8],
        'col3': [9, 10, 11, 12]
    }

    data2 = {
        'col': [1, 2, 3, 4],
        'col2': [5, 6, 7, 8],
        'col3': [9, 10, 11, 12]
    }

    df1 = pd.DataFrame(data1, columns=['col', 'col2', 'col3'])
    df2 = pd.DataFrame(data2, columns=['col', 'col2'])

    result = df1.shape == df2.shape and df1.equals(df2)
    print('result', result)


if __name__ == '__main__':
    main()
