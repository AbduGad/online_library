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
def hbnb():
    """ Home page is live! """
    states = storage.all(Books).values()

    tags = storage.all(Tags).values()

    return render_template('home_page.html',
                           states=states,
                           tags=tags)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
