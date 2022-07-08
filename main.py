from operator import contains
import requests
from decouple import config

# Get auth key from .env file
auth_key = config("AUTH_KEY", default = None)

# Wanted properties of each movie
wanted_properties = "original_title", "genres", "release_date"

def get_top_daily_movies():
    # Fetches top movies on the first page for the current day

    URL = f"https://api.themoviedb.org/3/movie/popular?api_key={auth_key}&language=en-US&page=1" 
    r= requests.get(url = URL)
    return  r.json()


def get_movie_details(movie_id):
    # Get details of a movie bv id

    URL= f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={auth_key}&language=en-US"
    r= requests.get(url = URL)
    # Return only wanted properties, i.e.  "original_title", "genre", "release_date"
    movie_details_specific = {key:value for key, value in r.json().items() if key in wanted_properties}
    # Returm final dictionary containing both specific requests as the dictor and actors
    return get_credits(movie_id, movie_details_specific)
    


def get_credits(movie_id, movie_dictionary):
    # Get credits of a movie by id

    # Init empty list values for actors and directors
    movie_dictionary["actors"] = []
    movie_dictionary["directors"] = []

    URL = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={auth_key}&language=en-US"
    r= requests.get(url = URL)
    data = r.json()

    # Get directors and actors, NOTE - can be more efficient with list comprehension
    
    for key, value in data.items():
        if key != "id":
            for x in value:
                if x["known_for_department"] == "Acting":
                    movie_dictionary["actors"].append(x["name"])
                elif "job" in x:
                    if x["job"] == "Director":
                        movie_dictionary["directors"].append(x["name"])
     
    # first value cointains actors the other list contains directors
    return movie_dictionary




daily_movies_data = get_top_daily_movies()
movie_results = daily_movies_data["results"]


extended_movies_results = {movie["id"]: get_movie_details(movie["id"]) for movie in movie_results}

print(extended_movies_results[453395])



