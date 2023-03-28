"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
# More code will go here

# os
# This is a module from Python’s standard library. It contains code related to working with your computer’s operating system.

# json
# Remember this module from the APIs lab? You’ll need this to load the data in data/movies.json.

# choice and randint from random
# choice is a function that takes in a list and returns a random element in the list. randint will return a random number within a certain range. You’ll use both to generate fake users and ratings.

# datetime from datetime
# We’ll use datetime.strptime to turn a string into a Python datetime object.

# crud, model, and server
# These are all files that you wrote (or will write) — crud.py, model.py, and server.py.

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

# Remember — we imported model and server instead of importing individual functions.

# If we had written from model import db, we’d be able to access db. However, since it’s just import model, you have to go through model before you can access db.

# Load the data from data/movies.json and save it to a var:
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Movie data will now be a list of dicts that look like this:
# [{'overview': 'The near future, [...] search of the unknown.',
#   'poster_path': 'https://image.tmdb.org/t/p/original//xBHvZcjRiWyobQ9kxBhO6B2dtRI.jpg',
#   'release_date': '2019-09-20',
#   'title': 'Ad Astra'}
#  ]


# Now we want to loop over the data from the file. When we read in data from a file, we always get strings. So the release date of each movie is a string.
# BUT THE DATA TYPE FOR  release_date is db.DateTime and not db.String. So we need to convert the strings to datetime obj. Do this with the Python datetime module.

# The datetime module provides classes to work with dates and times. One of them is the datetime class. Play with it in the Python console to see what it does.

# >>> from datetime import datetime
# The datetime class has a method called datetime.strptime. It turns a string into a datetime obj. This is how we will convert dates from our data file to datetime objs. Type the following into the REPL to mess with it.

# >>> date_str = "31-Oct-2015"
# >>> format = "%d-%b-%Y"
# >>> date = datetime.strptime(date_str, format)

# >>> date
# datetime.datetime(2015, 10, 31, 0, 0)
# >>> date.year
# 2015
# >>> date.month
# 10
# >>> date.day
# 31

# datetime.strptime(date_string, format)
# datetime takes in two args. date_string-a string with a date in it. the data you want to turn into a datetime obj and format- a string that tells Python how the date is formatted.

# The time format codes start with a % followed by another char. Check out this cheat sheet https://strftime.org/
# %d is the day of month as a zero padded num
# %m the month as a zero-padded num
# %Y the four digit year

# another example: Put this in the REPL
# >>> date_str2 = "Python 3.8 release: October 14th, 2019"
# >>> format2 = "Python 3.8 release: %B %dth, %Y"
# >>> date2 = datetime.strptime(date_str2, format2)

# >>> date2
# datetime.datetime(2019, 10, 14, 0, 0)
# >>> date2.year
# 2019
# >>> date2.month
# 10
# >>> date2.day
# 14


# Create movies, store them in list so we can use them
# to create fake ratings later
# getting each item, each obj is a dict
movies_in_db = []
for movie in movie_data:
    # TODO: get the title, overview, and poster_path from the movie
    title, overview, poster_path = (
        movie["title"],
        movie["overview"],
        movie["poster_path"],
    )
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime
    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit()
# we need to add movies to the SQLAlchemy seesion and commit them to the db. db.session.add() will add a single obj to the db. If you want to add a list of obj, use db.session.add_all()
# TODO: create a movie here and append it to movies_in_db

# for n in range(10):
#     email = f'user{n}@test.com'  # Voila! A unique email!
#     password = 'test'

#     user = crud.create_user(email, password)
#     model.db.session.add(user)
#     # call a random movie and score from the array
#     for _ in range(10):
#         rand_movie = choice(movies_in_db)
#         rand_rscore = randint(1, 5)

#         rating = crud.create_rating(user, rand_movie, rand_rscore)

#         model.db.session.add(rating)
# model.db.session.commit()

# (...snippet)
# Create 10 users; each user will make 10 ratings
for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)
    # check_user = model.User.query.first()
    # print(check_user)
    for _ in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1, 5)

        rating = crud.create_rating(user, random_movie, score)
        model.db.session.add(rating)

model.db.session.commit()
