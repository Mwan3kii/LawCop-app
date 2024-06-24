#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint


app_routes = Blueprint('app_routes', __name__, url_prefix='/api')

from api.routes.index import *
from api.routes.reports import *
from api.routes.alerts import *
from api.routes.user import *
