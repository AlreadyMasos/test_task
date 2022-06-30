from flask_sqlalchemy import SQLAlchemy
from main import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(70), nullable=False)

    def __repr__(self):
        return self.title, self.author

