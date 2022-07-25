import sys
from decouple import config
from sqlalchemy import create_engine, exc
from datetime import date
import pandas as pd
import psycopg2
import traceback

from base_logger import logger

# Get env variables from .env file using decouple
db_user = config("POSTGRES_USER", default = None)
db_pass = config("POSTGRES_PASSWORD", default = None)
db = config("POSTGRES_DB", default = None)
host= config("HOST", default = None)

#init engine
engine = create_engine(f"postgresql://{db_user}:{db_pass}@{host}:5432/{db}")


def store_dataframe(dataframe, date):
    #Connect and store the dateframe under format "yyyy-MM-dd"
    try:
        con = engine.connect()
        dataframe.to_sql(str(date), con=con, if_exists="replace")
        logger.info("Pushed data to database")
        con.close()
        
    except exc.SQLAlchemyError as e:
        # Log SQL alchemy errors
        logger.error(traceback.format_exc())

        # Clean up if the connection was not closed
        con.close()
        sys.exit(f"ERROR - Issue with SQL database - {type(e)}")





