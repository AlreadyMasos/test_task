from flask import Flask
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from schemas import BookSchema
from flask_apispec import use_kwargs, marshal_with

app = Flask(__name__)

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()
docs = FlaskApiSpec()

docs.init_app(app)
app.config.update({
    'APISPEC_SPEC':APISpec(
        title='booksdatabase',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    )
})

from models import *


@app.route('/all_books', methods=['GET'])
@marshal_with(BookSchema(many=True))
def get_book():
    books = Book.query.all()
    return books


@app.route('/book', methods=['POST'])
@use_kwargs(BookSchema)
@marshal_with(BookSchema)
def add_book(**kwargs):
    new_book = Book(**kwargs)
    session.add(new_book)
    session.commit()
    return new_book


@app.route('/book/<int:book_id>', methods=['GET'])
@marshal_with(BookSchema)
def show_book(book_id):
    item = Book.query.filter(Book.id == book_id).first()
    if not item:
        return {'message' : 'no book with such element'}
    return item


@app.route('/book/<int:book_id>', methods=['PUT'])
@marshal_with(BookSchema)
@use_kwargs(BookSchema)
def update_book(book_id, **kwargs):
    item = Book.query.filter(Book.id == book_id).first()
    if not item:
        return {'message':'no such element'}, 400
    for key, value in kwargs.items():
        setattr(item, key, value)
    session.commit()
    return Book.query.all()


@app.route('/book/<int:book_id>', methods=['DELETE'])
@marshal_with(BookSchema)
def delete_book(book_id):
    item = Book.query.filter(Book.id == book_id).first()
    session.delete(item)
    session.commit()
    return Book.query.all()


@app.route('/book/<string:author>', methods=['GET'])
@marshal_with(BookSchema(many=True))
def get_authors_books(author):
    item = Book.query.filter(Book.author == author).all()
    if not item:
        return {'message' : 'no book with such author'}
    return item


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(debug=True)


