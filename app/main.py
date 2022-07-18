# Import local functions and variables 
from get_movies import structured_daily_movies, to_dataframe, save_as_json
from store_data import store_dataframe
from base_logger import logger, current_date

import time



def main():
    logger.info(f"Started the program on - {current_date}")
    daily_movie_results=structured_daily_movies()
    #save_as_json(daily_movie_results) -> saves output as JSON. Used for tests
    df = to_dataframe(daily_movie_results)
    store_dataframe(df, current_date)
    logger.info(f"Finished the program on - {current_date}")
    time.sleep(120)

#INIT project
if __name__ == "__main__":
    main()
