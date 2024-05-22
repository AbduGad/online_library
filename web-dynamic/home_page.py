#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.book import Books
from models.book_tags import Books_tags
from models.tags import Tags
from models.user_support_messages import User_support
from os import environ
from flask import Flask, jsonify, render_template, request
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
    books = storage.all(Books).values()
    
    return render_template('landing_page.html',
                           books=books)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Retrieve form data from the request
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Create a new FormData object
    form_data = User_support(name=name, email=email, message=message)

    # Add the form data to the database session
    storage.new(form_data)
    storage.save()

    
    return jsonify({'message': 'Form submitted successfully', 'status': 'success'})


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=9000)
