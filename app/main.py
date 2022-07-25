import sys
import os
import traceback
import time
# Import local functions and variables 
from get_movies import structured_daily_movies, to_dataframe, save_as_json
from store_data import store_dataframe
from base_logger import logger, current_date




def main():
    logger.info(f"Started the program on - {current_date}")
    daily_movie_results=structured_daily_movies()
    #save_as_json(daily_movie_results) -> saves output as JSON. Used for tests
    df = to_dataframe(daily_movie_results)
    store_dataframe(df, current_date)
    logger.info(f"Finished the program on - {current_date}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # TODO - make case specific error handling
        # Currently this logs all the errors to the log file
        # Gives output in terminal: Error type, file name and line
        logger.error(traceback.format_exc())
        exc_type, exc_obj, exc_tb = sys.exc_info()
        filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        sys.exit(f"Exit with error - {exc_type} - {filename} - {exc_tb.tb_lineno}.\
             Check logs for more information")