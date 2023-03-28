"""Server for movie ratings app."""
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def go_home():
    """View the home page"""
    return render_template('homepage.html')


@app.route('/movies')
def all_movies():
    """View all movies"""
    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)


@app.route('/movies/<movie_id>')
def one_movie(movie_id):
    """View one movie by it's ID"""
    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)


@app.route('/users')
def all_users():
    """View all users"""
    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route('/users', methods=["POST"])
def retrieve_user_info():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
        return redirect("/")
    # Now, we’ll take a brief journey back to our decision in part 2 to not add objects to the SQLAlchemy session inside of our crud.py functions. Imagine if we wrote a flask route that created multiple objects and committed them each separately to the database. If an error were to occur somewhere in between these commits, the first set of objects would get saved to the db but the second group would not. This is a problem, because our db is now in an inconsistent state!

    # To avoid situations like this, think of each flask route as existing within a single transaction - either the request completes successfully and all objects are saved to the db, or the request fails and none of them are. DB transactions that behave this way are called “atomic”. To ensure your flask routes stay atomic, always add new objects to the db session inside of your route instead of a module like crud.py, and make sure to only commit once per route.


@app.route('/users/<user_id>')
def one_user(user_id):
    """View one movie by it's ID"""
    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")


@app.route("/update_rating", methods=["POST"])
def update_rating():
    rating_id = request.json["rating_id"]
    updated_score = request.json["updated_score"]
    crud.update_rating(rating_id, updated_score)
    db.session.commit()

    return "Success"


@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def create_rating(movie_id):
    """Create a new rating for the movie."""

    logged_in_email = session.get("user_email")
    rating_score = request.form.get("rating")

    if logged_in_email is None:
        flash("You must log in to rate a movie.")
    elif not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        movie = crud.get_movie_by_id(movie_id)

        rating = crud.create_rating(user, movie, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this movie {rating_score} out of 5.")

    return redirect(f"/movies/{movie_id}")


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
