# python-and-sql-project
Python and SQL project - connect to MSSQLServer and convert the SQL code to python, including (triggers and cursors, ...etc)

Author: Abdullah Daqdoqa

data access layer
Polling - query the database regularly from your code and detect changes in your Python code
Notifications 
The infinite loop with a fixed sleep time is the simplest thing to try indeed

real-time database (mysql)

socketIO


checksum 
SELECT CHECKSUM_AGG(BINARY_CHECKSUM(*)) FROM sample_table WITH (NOLOCK);


`

serlize pucklet dataframe pandas serelization

cmd read arguments 
import sys
print sys.argv

import time

while True:

    print("This prints once a minute.")
    
    time.sleep(60) # Delay for 1 minute (60 seconds).
`

`
from time import sleep
sleep(5)
`


3:51     on video a clue: 
script starts and stops first time
difference between the first time run script and all the times after running the script
rerun the script and make decision of


* TODO make program OOP, manage the exceptions, DRY & KISS
* TODO: text obfuscation for password and username encryption

run script with arguments, expected values example:

    driver = '{ODBC Driver 17 for SQL Server}'
    server = 'ABDULLAH\SQL2019'
    userid = 'sa'
    password = '123456'
    database = 'Survey_Sample_A19'

> python main.py --driver "{ODBC Driver 17 for SQL Server}" --server ABDULLAH\SQL2019 --userid sa --password 123456 --database Survey_Sample_A19

> python main.py driver="{ODBC Driver 17 for SQL Server}" server=ABDULLAH\SQL2019 userid=sa password=123456

# TODO: dowload the libraries within the script, exceptions also 