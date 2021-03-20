# Python SQL Project

### Description:
Python and SQL project - connect to MSSQLServer and convert the getAllSurveyData stored procedure in the database to python code, 
including (trigger, cursors) that fire the getAllSurveyData function



### Author: 
Abdullah Daqdoqa



### Run script with arguments, expected values example:

    driver = '{ODBC Driver 17 for SQL Server}'
    server = 'ABDULLAH\SQL2019'
    userid = 'sa'
    password = '123456'
    database = 'Survey_Sample_A19'

#### Example to run the script: 
> python main.py --driver "{ODBC Driver 17 for SQL Server}" --server ABDULLAH\SQL2019 --userid sa --password 123456 --database Survey_Sample_A19

> python main.py -r "{ODBC Driver 17 for SQL Server}" -s ABDULLAH\SQL2019 -u sa -p 123456 -d Survey_Sample_A19



### Required Packages:
- it will be downloaded automatically within the script itself via pip.



### Environment:
- Windows 10 python 3.9.x



### Permissions:
- to create new file result.pkl (a serialized file store dataframe of the SurveyStructure table) 
      used to compare the old database (SurveyStructure) data with new data read in the following script runs.
- allowing the script to install pip packages to the OS.



### Resources:
- in the resources folder we have .pdf elaborating more about this project, 
    getAllSurveyData.sql file which is extracted from Survey_Sample_A19.bak,
    Survey_Sample_A19.bak a database backup which can be imported in MS SQL Server.



### Files:
- _utils.py: has one class InstallPackages class by making an instance of this call it will install all the packages passed 
        to the constructor using pip on the OS.
- argument: Argument is a class with one static method get(), used to read all the arguments from the command line/terminal 
        and read the values and use it in this script, all the arguments related to connecting to the database.
- database: has a class used to connect to database using pyodbc package.
- main: the engine of the script will get together all various parts of these codes.
- procedures: has a class used to replicate the functionalities of get_all_survey_data stored procedure.
- result.pkl: an expected files which is a serialized file to save the current database table status, 
        might not be there on before the script first run.
- README.md file: for documenting.
- .gitignore: to git configuration file to exclude some files from being uploaded to github.




### Behavior:
- running the script for the first time (without result.pkl file) will create this file if not existed and get all survey data and create new view
- running the script if the file was created, and the database table (SurveyStructure) status has been changed will, so data 
        from the database different from result.pkl will result updating the view.
- running the script while the file existed, and the status of database table (SurveyStructure) is identical to result.pkl will produce nothing,
        except connecting to the database and exiting the script.
