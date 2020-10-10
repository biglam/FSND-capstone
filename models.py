import os
from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

postgres_username = os.environ.get('POSTGRES_USERNAME')
postgres_password = os.environ.get('POSTGRES_PASSWORD')

database_name = "capstone"
database_path = "postgres://{}:{}@{}/{}".format(postgres_username, postgres_password, 'localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()
    migrate = Migrate(app, db)


actor_movies = db.Table('actor_movies',
                        Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True),
                        Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True)
                        )


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)  # TODO: regex
    movies = db.relationship('Movie', secondary=actor_movies, backref=db.backref('movies'))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def short_format(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def full_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_count': len(self.movies),
            'movies': [movie.short_format() for movie in self.movies]
        }


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(Integer, primary_key=True)
    title = db.Column(String, nullable=False, unique=True)
    release_date = db.Column(Date(), nullable=False)
    actors = db.relationship('Actor', secondary=actor_movies, backref=db.backref('actors'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def short_format(self):
        return {
            'id': self.id,
            'title': self.title
        }

    def full_details(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actor_count': len(self.actors),
            'actors': [actor.short_format() for actor in self.actors]
        }
