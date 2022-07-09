from operator import contains
import requests
from decouple import config
from json import dump

# Get auth key from .env file
auth_key = config("AUTH_KEY", default = None)

# Wanted properties of each movie
wanted_properties = "original_title", "genres", "release_date"

#movie_id=453395
def get_review(movie_id):
    # Get user reviews of a movie, gets movie by movie_id

    URL = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={auth_key}&language=en-US&page=1"
    r= requests.get(url = URL)
    data = r.json()

    # Add reviews for each movie

    # NOTE postprocessing can be done here, regex for reviews to remove URLs etc.
    structued_reviews = [x["content"] for x in data["results"]]

    return structued_reviews
        

def get_top_daily_movies():
    # Fetches top movies on the first page for the current day

    URL = f"https://api.themoviedb.org/3/movie/popular?api_key={auth_key}&language=en-US&page=1" 
    r= requests.get(url = URL)
    return r.json()


        
def get_movie_details(movie_id):
    # Get details of a movie bv id

    URL= f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={auth_key}&language=en-US"
    r= requests.get(url = URL)
    # Return only wanted properties, i.e.  "original_title", "genre", "release_date"
    movie_details_specific = {key:value for key, value in r.json().items() if key in wanted_properties}

    movie_details_specific["reviews"] = get_review(movie_id)
    # Returm final dictionary containing both specific requests as well as the director of the movie and actors
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


def structured_top_daily_movies():
    # Returns structured output for todays top movies in wanted format.
    # Wanted format includes release date, genre, original title, actors and directors
    
    daily_movies_data = get_top_daily_movies()
    movie_results = daily_movies_data["results"]

    # Get extended details of each movie - contains release date, genre, original title. Also fetches actors and directors
    extended_movies_results = {movie["id"]: get_movie_details(movie["id"]) for movie in movie_results}

    return extended_movies_results


def save_as_json(data):
    with open("output.json", "w+", encoding="utf-8") as f:
        dump(data,f)

#data=get_review(movie_id)
#print(data)

if __name__ == "__main__":
        data = structured_top_daily_movies()
        #save_as_json(data)
        #print(data[615469])


