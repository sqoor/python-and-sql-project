try:
    import pandas as pd
    from argument import Argument
    from database import Connection
except ModuleNotFoundError:
    from tools import InstallPackages
    InstallPackages({'pandas', 'argparse', 'pyodbc'})
    import pandas as pd
    from argument import Argument
    from database import Connection

from procedures import Procedure
from tools import Verbose


class Starter:
    def __init__(self):
        args = Argument.get()
        self.db = Connection(args.driver, args.server, args.database, args.userid, args.password)

    def __del__(self):
        Verbose.print_ln('Script executed.')

    """ Documentation: main
          Description:
              a method used to create put all the script objects together and run all the script.
    """
    def main(self):
        pkl_df = None
        db_updated = False
        first_run = False

        db_df = self.db.run('SELECT * FROM [SurveyStructure]')

        try:
            pkl_df = pd.read_pickle('result.pkl')
            db_updated = pkl_df.shape != db_df.shape or not pkl_df.equals(db_df)
        except FileNotFoundError:
            first_run = pkl_df is None
        except Exception as err:
            Verbose.print_ln("Something went bad \nError: ", err)

        if first_run or db_updated:
            try:
                db_df.to_pickle('result.pkl')
            except Exception as err:
                Verbose.print_ln("Was not able to create new pkl file, Error:", err)
            self.create_or_update_view()
            Verbose.print_ln("update the view and the pkl")
        else:
            Verbose.print_ln('No changes, database table status remained same.')

    """ Documentation: create_or_update_view
       Description:
           a method used to create new view "vw_AllSurveyDataPython" and store all survey data we got from procedure object.
    """
    def create_or_update_view(self):
        procedure = Procedure(self.db)
        final_query = ' CREATE OR ALTER VIEW vw_AllSurveyData AS ' + procedure.get_all_survey_data()
        self.db.create(final_query)
        Verbose.print_ln("View updated.")


if __name__ == '__main__':
    args = Argument.get()
    Verbose.show_messages(args.verbose)

    starter = Starter()
    starter.main()
