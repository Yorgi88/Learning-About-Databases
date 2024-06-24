from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

"""We gonna learn how to use ORM here so pay attention"""
app = Flask(__name__)

# first create the database
class Database(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite///new-books-collection.db"

# create the extensions
db = SQLAlchemy(model_class=Database)

# initialize the app with the extensions
db.init_app(app)

# Now create the table
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f"<book {self.title}"

# create table schema in the database
with app.app_context():
    db.create_all()


# create the record
with app.app_context():
    new_book = Book(id=1, title="Harry Potter", author="J.K. Rowling", rating=9.7)
    db.session.add(new_book)
    db.session.commit()