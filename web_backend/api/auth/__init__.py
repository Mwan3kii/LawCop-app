#!/usr/bin/python3
"""importing auth blueprint"""
from flask import Blueprint
auth = Blueprint('auth', __name__, url_prefix='/api')
from api.auth.auth import *
