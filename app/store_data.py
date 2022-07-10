import psycopg2
from decouple import config
from sqlalchemy import create_engine

import pandas as pd

db_user = config("POSTGRES_USER", default = None)
db_pass = config("POSTGRES_PASS", default = None)
db = config("POSTGRES_DB", default = None)
host= config("HOST", default = None)


engine = create_engine(f"postgresql://{db_user}:{db_pass}@{host}:5432/{db}")




def store_dataframe(dataframe):
    con = engine.connect()
    dataframe.to_sql("table2", con=con, if_exists="replace")
    con.close()


