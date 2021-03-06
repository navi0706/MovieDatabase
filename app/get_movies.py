import requests
from decouple import config
from json import dump
import pandas as pd


from senitiment_analysis import SentimentAnalysisNLTK
from base_logger import logger


# Get auth key from .env file, Init SentimentyAnalysis
auth_key = config("AUTH_KEY", default = None)
sentiment_analysis = SentimentAnalysisNLTK()



# Wanted properties of each movie
wanted_properties = "original_title", "genres", "release_date"





class MoviesDatabase:

    # NOTE possible improvement, run program in while loop and trigger program every 24h
    # Currently program has to be started manually

    def get_top_daily_movies(self):
        # Fetches top movies on the first page for the current day

        URL = f"https://api.themoviedb.org/3/movie/popular?api_key={auth_key}&language=en-US&page=1" 
        r= requests.get(url = URL)
        return r.json()

        



            
    def get_movie_details(self, movie_id):
        # Get details of a movie by id

        URL = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={auth_key}&language=en-US"
        r = requests.get(url = URL)
        # Return only wanted properties, i.e.  "original_title", "genre", "release_date"
        movie_details_specific = {key:value for key, value in r.json().items() if key in wanted_properties}

        movie_details_specific["reviews"] = self.get_movie_review(movie_id)
        
        # Returm final dictionary containing both specific requests as well as the director of the movie and actors
        return self.get_movie_credits(movie_id, movie_details_specific)
        

    def get_movie_credits(self, movie_id, movie_dictionary):
        # Get credits of a movie by id

        # Init empty list values for actors and directors
        movie_dictionary["actors"] = []
        movie_dictionary["directors"] = []

        URL = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={auth_key}&language=en-US"
        r = requests.get(url = URL)
        credits_data = r.json()

        # Get directors and actors, NOTE - can be more efficient with list comprehension
        
        for key, values in credits_data.items():
            if key != "id":
                for credit_value in values:
                    if credit_value["known_for_department"] == "Acting":
                        movie_dictionary["actors"].append(credit_value["name"])
                    elif "job" in credit_value:
                        if credit_value["job"] == "Director":
                            movie_dictionary["directors"].append(credit_value["name"])
        
        # first value cointains actors the other list contains directors
        return movie_dictionary

    def get_movie_review(self, movie_id):
        # Get user reviews of a movie, gets movie by movie_id

        URL = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={auth_key}&language=en-US&page=1"
        r = requests.get(url = URL)
        review_data = r.json()
        #print(len(data["results"]))

        # Add reviews for each movie

        structured_reviews = ", ".join( sentiment_analysis.sentiment_analysis_pipeline(movie_review["content"])
                             for movie_review in review_data["results"])
        return structured_reviews


    def making_data_nice(self, dict):
    # Making a change so that values inside the list are joined.
    # NOTE this can be done more efficiently when originally getting the data

        for movie_id, movie_details in dict.items():
            movie_details["genres"] = ", ".join(genre_name["name"] for genre_name in movie_details["genres"])
            movie_details["actors"] = ", ".join(actor for actor in movie_details["actors"])
            movie_details["directors"] = ", ".join(director for director in movie_details["directors"])
        return dict    


# Init MoviesDatabase class            
movie_api=MoviesDatabase()    
def structured_daily_movies():
    # Gets structured daily movies with all necessary details
    
    daily_movies_data = movie_api.get_top_daily_movies()
    logger.info("Fetched daily movies")
    movie_results = daily_movies_data["results"]
    # Get extended details of each movie - contains release date, genre, original title. Also fetches actors and directors
    logger.info("Started sentiment analysis and structuring")
    extended_movies_results = {movie["id"]: movie_api.get_movie_details(movie["id"]) for movie in movie_results}
    logger.info("Finished sentiment analysis")
    structured_movies_result = movie_api.making_data_nice(extended_movies_results)
    logger.info("Finished structuring daily movies")
    return structured_movies_result


def save_as_json(data):
    # Saves dictionary as JSON
    with open("output.json", "w+", encoding="utf-8") as f:
        dump(data,f)

def to_dataframe(custom_dictionary):
    return pd.DataFrame.from_dict(custom_dictionary, orient="index")
    


