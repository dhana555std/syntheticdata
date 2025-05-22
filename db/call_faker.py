# Auto-generated script to call generate functions in dependency order

import os
import json
from decimal import Decimal

from utils.file_utils import write_to_json_file

from do.actors import generate_actors
from do.customers import generate_customers
from do.directors import generate_directors
from do.genres import generate_genres
from do.movies import generate_movies
from do.movie_actors import generate_movie_actors
from do.reviews import generate_reviews
from do.theaters import generate_theaters
from do.screenings import generate_screenings
from do.tickets import generate_tickets


def main_faker():
    print('Calling generate_actors()...')
    actors = generate_actors()
    write_to_json_file('actors', actors)

    print('Calling generate_customers()...')
    customers = generate_customers()
    write_to_json_file('customers', customers)

    print('Calling generate_directors()...')
    directors = generate_directors()
    write_to_json_file('directors', directors)

    print('Calling generate_genres()...')
    genres = generate_genres()
    write_to_json_file('genres', genres)

    print('Calling generate_movies(genres, directors)...')
    movies = generate_movies(genres, directors)
    write_to_json_file('movies', movies)

    print('Calling generate_movie_actors(movies, actors)...')
    movie_actors = generate_movie_actors(movies, actors)
    write_to_json_file('movie_actors', movie_actors)

    print('Calling generate_reviews(customers, movies)...')
    reviews = generate_reviews(customers, movies)
    write_to_json_file('reviews', reviews)

    print('Calling generate_theaters()...')
    theaters = generate_theaters()
    write_to_json_file('theaters', theaters)

    print('Calling generate_screenings(movies, theaters)...')
    screenings = generate_screenings(movies, theaters)
    write_to_json_file('screenings', screenings)

    print('Calling generate_tickets(customers, screenings)...')
    tickets = generate_tickets(customers, screenings)
    write_to_json_file('tickets', tickets)



if __name__ == '__main__':
    main_faker()
