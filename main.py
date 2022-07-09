from operator import contains
import requests
from decouple import config
from json import dump
import pandas as pd

from senitiment_analysis import SentimentAnalysisNLTK

# Get auth key from .env file, Init SentimentyAnalysis
auth_key = config("AUTH_KEY", default = None)
sentiment_analysis = SentimentAnalysisNLTK()

# Wanted properties of each movie
wanted_properties = "original_title", "genres", "release_date"



class MoviesDatabase:
    

    def get_top_daily_movies(self):
        # Fetches top movies on the first page for the current day

        URL = f"https://api.themoviedb.org/3/movie/popular?api_key={auth_key}&language=en-US&page=1" 
        r= requests.get(url = URL)
        return r.json()


            
    def get_movie_details(self, movie_id):
        # Get details of a movie bv id

        URL= f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={auth_key}&language=en-US"
        r= requests.get(url = URL)
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
        r= requests.get(url = URL)
        credits_data = r.json()

        # Get directors and actors, NOTE - can be more efficient with list comprehension
        
        for key, value in credits_data.items():
            if key != "id":
                for x in value:
                    if x["known_for_department"] == "Acting":
                        movie_dictionary["actors"].append(x["name"])
                    elif "job" in x:
                        if x["job"] == "Director":
                            movie_dictionary["directors"].append(x["name"])
        
        # first value cointains actors the other list contains directors
        return movie_dictionary

    def get_movie_review(self, movie_id):
        # Get user reviews of a movie, gets movie by movie_id

        URL = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={auth_key}&language=en-US&page=1"
        r= requests.get(url = URL)
        review_data = r.json()
        #print(len(data["results"]))

        # Add reviews for each movie
        print(movie_id)

        structured_reviews = [sentiment_analysis.sentiment_analysis_pipeline(x["content"])
                             for x in review_data["results"]]
        return structured_reviews


# Init MoviesDatabase class            
movie_api=MoviesDatabase()    
def structured_daily_movies():
    # Gets structured daily movies with all necessary details

    daily_movies_data = movie_api.get_top_daily_movies()
    movie_results = daily_movies_data["results"]
    # Get extended details of each movie - contains release date, genre, original title. Also fetches actors and directors
    extended_movies_results = {movie["id"]: movie_api.get_movie_details(movie["id"]) for movie in movie_results}

    return extended_movies_results


def save_as_json(data):
    with open("output.json", "w+", encoding="utf-8") as f:
        dump(data,f)

def dataframe(custom_dictionary):
    return pd.DataFrame.from_dict(custom_dictionary)

if __name__ == "__main__":
    daily_movie_results=structured_daily_movies()
    save_as_json(daily_movie_results)
    print(dataframe(daily_movie_results))
