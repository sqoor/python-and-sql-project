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

from procedures import Procedure

args = Argument.get()
db = Connection(args.driver, args.server, args.database, args.userid, args.password)


def main():
    pkl_df = None
    db_updated = False
    first_run = False

    db_df = db.run('SELECT * FROM [SurveyStructure]')

    try:
        pkl_df = pd.read_pickle('result.pkl')
        db_updated = pkl_df.shape != db_df.shape or not pkl_df.equals(db_df)
    except FileNotFoundError:
        first_run = pkl_df is None
    except Exception as err:
        print("Something went bad \nError: ", err)

    if first_run or db_updated:
        db_df.to_pickle('result.pkl')
        create_or_update_view()
        print("update the view and the pkl")


def create_or_update_view():
    procedure = Procedure(db)
    final_query = ' CREATE OR ALTER VIEW vw_AllSurveyDataPython AS ' + procedure.get_all_survey_data()
    db.create(final_query)
    print("View updated.")


def println(arg, name=''):
    print("\n\n")
    if name:
        print(f'{name}:')
    print(arg)
    print("\n\n\n")


if __name__ == '__main__':
    main()
