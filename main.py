from operator import contains
import requests
from decouple import config

#get auth key from .env file
auth_key = config("AUTH_KEY", default = None)

def get_top_daily_movies():
    """Fetches top movies on the first page for the current day"""

    URL = f"https://api.themoviedb.org/3/movie/popular?api_key={auth_key}&language=en-US&page=1" 
    r= requests.get(url = URL)
    return  r.json()


def get_movie_details(movie_id):
    """ Get details of a movie bv id"""

    URL= f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={auth_key}&language=en-US"
    r= requests.get(url = URL)
    return  r.json()

def get_credits(movie_id):
    """Get credits of a movie by id"""

    URL = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={auth_key}&language=en-US"
    r= requests.get(url = URL)
    return  r.json()


wanted_properties= "original_title", "genre", "release_date"

daily_movies_data = get_top_daily_movies()
movie_results = daily_movies_data["results"]


extended_movies_results = {movie["id"]: get_movie_details(movie["id"]) for movie in movie_results}

#print(extended_movies_results[453395])
#extended_movies_results = [get_movie_details(movie["id"]) for movie in movie_results]
movies_credits = [get_credits(movie["id"]) for movie in movie_results]

print(movies_credits[0])

