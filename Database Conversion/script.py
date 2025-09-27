from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas, os, urllib.parse

load_dotenv(".env")

mysql_engine = create_engine (
    f"mysql+pyodbc:///?odbc_connect=DRIVER={{MySQL ODBC 8.0 ANSI Driver}};"
    "SERVER=localhost;PORT=3306;DATABASE=yourdatabase;"
    f"UID={os.getenv('MYSQLUSER')};PWD={os.getenv('MYSQLPASSWORD')};"
    "CHARSET=utf8mb4;"
)

odbc_conn = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=WIN-MFHV45P219S\\SQLEXPRESS;"
    "DATABASE=yourdatabase;"
    f"UID={os.getenv('MS_SQLUSER')};"
    f"PWD={os.getenv('MS_SQLPASSWORD')};"
)

sqlserver_engine = create_engine (
    f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(odbc_conn)}"
)

table_name = "yourtablename"

try:
    df = pandas.read_sql_table(table_name, con = mysql_engine)
    print("Successfully read data from MySQL table.")

except Exception as e:
    print(f"Error reading from MySQL: {e}")
    exit()

try:
    df.to_sql(table_name, con = sqlserver_engine, if_exists  = "replace", index = False)
    print("Successfully wrote data to SQL Server.")

except Exception as e:
    print(f"Error writing to SQL Server: {e}")

finally:
    mysql_engine.dispose()
    sqlserver_engine.dispose()