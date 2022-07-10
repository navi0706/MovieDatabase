# Movie database

This is a data engineering project coded in python.
Idea of the project is to get data using TMDB api, structure and clean the data,
preform sentiment analysis and to store the results into a database.

## Installation

The whole project is ran in containers.
In order to start the project it is necessary to build a docker image based on this project.
Steps to install:

Run inside project's directory --> docker build -t movie_api .

This will build movie_api image that is neccessary for project to be ran.

After that run docker compose command --> docker compose up

## Notes

For setting up .env file follow env_example.
AUTH_KEY is tied to authentication key on TMDB website.
Other env variables are tied to PostgreSQL server.


## Example of database
index - Refers to movie_id

genres - Contains a list of genres for each movie, some movies have multiple genres

original_title - Refers to the original title of the movie

release_date - Date when movie was release in format "yyyy-MM-dd"

reviews - Using sentiment analysis each review is labled as positive, neutral or negative. Some films have multiple reviews while
some have none

actors - list of all actors present in the movie

directors - main director for each movie


![alt text](https://github.com/navi0706/MovieDatabase/blob/master//PostgreSQL_example.png?raw=true)