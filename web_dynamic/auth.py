#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.user import User
from os import environ
from flask import Flask, render_template
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/login/', strict_slashes=False)
def login():
