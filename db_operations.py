import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from parameters import *

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-movies-list.db"
db.init_app(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500))
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(500))
    img_url = db.Column(db.String(250))

    def create(self):
        with app.app_context():
            db.session.add(self)
            db.session.commit()


def select_all():
    with app.app_context():
        all_movies = db.session.execute(db.select(Movie).order_by(desc(Movie.rating))).scalars()
        rank = 1
        movies_list = []
        for movie in all_movies:
            add_rank(movie.id, rank)
            rank += 1
            movies_list.append(movie)
        movies_list.reverse()
        return movies_list


def add_rank(id, rank):
    with app.app_context():
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
        movie_to_update.ranking = rank
        db.session.commit()


def select(id):
    with app.app_context():
        movie = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
        return movie


def update_movie(id, rating, review):
    with app.app_context():
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
        movie_to_update.rating = rating
        movie_to_update.review = review
        db.session.commit()


def delete_movie(id):
    with app.app_context():
        movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
        db.session.delete(movie_to_delete)
        db.session.commit()


with app.app_context():
    db.create_all()

new_movie = Movie(
    title="Phone Booth",
    year=2002,
    description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's "
                "sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads "
                "to a jaw-dropping climax.",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)
# new_movie.create()

second_movie = Movie(
    title="Avatar The Way of Water",
    year=2022,
    description="Set more than a decade after the events of the first film, learn the story of the Sully family"
                " (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep"
                " each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    rating=7.3,
    ranking=9,
    review="I liked the water.",
    img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
)


# second_movie.create()


def get_movie(movie_title):
    parameters = {
        "query": movie_title,
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}"
    }
    response = requests.get(url="https://api.themoviedb.org/3/search/movie", params=parameters, headers=headers)
    movie_titles = []
    for movie in response.json()["results"]:
        temp_movie = {
            'id': movie['id'],
            'title': movie['title'],
            'release_date': movie['release_date'],
            'overview': movie['overview'],
            'poster_path': movie['poster_path'],
        }
        movie_titles.append(temp_movie)
    return movie_titles


def add_movie(id):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}"
    }
    response = requests.get(url=f"https://api.themoviedb.org/3/movie/{id}", headers=headers)
    movie = response.json()
    print(movie['title'], movie['release_date'])

    temp_movie = Movie(
        id=movie['id'],
        title=movie['title'],
        year=movie['release_date'],
        description=movie['overview'],
        img_url=f"https://image.tmdb.org/t/p/w500{movie['backdrop_path']}"
    )
    temp_movie.create()
