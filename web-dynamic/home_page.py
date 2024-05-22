#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.book import Books
from models.book_tags import Books_tags
from models.tags import Tags
from os import environ
from flask import Flask, render_template
import uuid
app = Flask(__name__)
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/home/', strict_slashes=False)
def home():
    """ Home page is live! """

    books = storage.all(Books).values()

    tags = storage.all(Tags).values()

    return render_template('home_page.html',
                           books=books,
                           tags=tags)


@app.route('/books/<book_name>', strict_slashes=False)
def open_book(book_name):
    """ Opens pdf """
    book = storage.getBy_name(cls=Books, name=book_name)

    return render_template('book_page.html',
                           book=book)

@app.route('/landing/', strict_slashes=False)
def landing_page():
    """ Landing page """
    return render_template('landing_page.html')

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=9000)
