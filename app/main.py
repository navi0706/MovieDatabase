from get_movies import structured_daily_movies, to_dataframe, save_as_json
from store_data import store_dataframe


#INIT project
if __name__ == "__main__":
    daily_movie_results=structured_daily_movies()
    #save_as_json(daily_movie_results) -> saves output as JSON. Used for tests
    df = to_dataframe(daily_movie_results)
    store_dataframe(df)
