from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import os
'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)


class Database(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite///books.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

"""had to ask chatGPT for help, gave me the code below and seems there are no issues"""
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'books.db')


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

    # def __repr__(self):
    #     return f"<book {self.title}>"

# create table schema in the database
with app.app_context():
    db.create_all()


# create the record
# with app.app_context():
#     new_book = Book(id=1, title="Harry Potter", author="J.K. Rowling", rating=9.7)
#     db.session.add(new_book)
#     db.session.commit()




all_books = []


@app.route('/')
def home():
    res = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = res.scalars().all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data = request.form

        new_book = Book(
            title=data["title"],
            author=data["author"],
            rating=data["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        # new_books = {
        #     "title" : name,
        #     "author" : author,
        #     "rating" : rating
        # }
        # all_books.append(new_books)
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        """we wanna perform an update action here"""
        data = request.form
        book_id = data["id"]
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.rating = data["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get("id")
    book_selected = db.get_or_404(Book, book_id)
    return render_template("edit.html", book=book_selected)

@app.route("/delete")
def delete():
    """we are going to perform a delete action here from CRUD"""
    book_id = request.args.get("id")
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



"""we finished the project CRUD"""





if __name__ == "__main__":
    app.run(debug=True)

