"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(title=title, overview=overview,
                  release_date=release_date, poster_path=poster_path)
    return movie


def get_movies():
    """Return all movies"""
    return Movie.query.all()


def get_users():
    """Return all users"""

    return User.query.all()


def get_user_by_id(user_id):
    """Get a moive by it's ID"""
    return User.query.get(user_id)


def get_movie_by_id(movie_id):
    """Get a moive by it's ID"""
    return Movie.query.get(movie_id)


def create_rating(user, movie, score):
    """Create and return a new rating."""

    rating = Rating(user=user, movie=movie, score=score)
    return rating


if __name__ == '__main__':
    from server import app
    connect_to_db(app)


# How to get create_rating to work:
# create the object of the user and the movie first. Then we only need to pass in the score!
# >>> jesse = User(email="email@jesse", password="hiagain")
# >>> sports = Movie(title="Something about sports", overview="They are losing until a coach inspires them", release_date="2002, 5, 5", poster_p
# ath="staticonyourcomputer")
# jesseRating = Rating(score=5)
