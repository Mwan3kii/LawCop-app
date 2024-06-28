#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.routes import app_routes
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_routes)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(400)
def bad_request(error):
    """ 400 Error
    ---
    responses:
      400:
        description: a resource was not found
    """
    return make_response(jsonify({'error': str(error.description)}), 400)

@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

@app.errorhandler(500)
def server_error(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return jsonify({'error': 'Internal server error'}), 500

app.config['SWAGGER'] = {
    'title': 'LawCop web application',
    'uiversion': 3
}

Swagger(app)


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('LC_API_HOST')
    port = environ.get('LC_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5500'
    app.run(host=host, port=port, threaded=True, debug=True)