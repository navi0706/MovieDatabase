from decouple import config
from sqlalchemy import create_engine
from datetime import date
import pandas as pd
import psycopg2

current_date = date.today()

db_user = config("POSTGRES_USER", default = None)
db_pass = config("POSTGRES_PASSWORD", default = None)
db = config("POSTGRES_DB", default = None)
host= config("HOST", default = None)


engine = create_engine(f"postgresql://{db_user}:{db_pass}@{host}:5432/{db}")


def store_dataframe(dataframe):
    con = engine.connect()
    dataframe.to_sql(str(current_date), con=con, if_exists="replace")
    con.close()


