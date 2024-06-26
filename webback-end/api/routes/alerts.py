#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from models.alerts import Alert
from models import storage
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_routes.route('/alerts', methods=['GET'], strict_slashes=False)
@swag_from('documentation/alert/get_alert.yml', methods=['GET'])
def get_alerts():
    """
    Retrieves the list of all State objects
    """
    all_alerts = storage.all(Alert).values()
    list_alerts = []
    for alert in all_alerts:
        list_alerts.append(alert.to_dict())
    return jsonify(list_alerts)


@app_routes.route('/alerts/<alert_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_id_state.yml', methods=['get'])
def get_alert(alert_id):
    """ Retrieves a specific State """
    alert = storage.get(Alert, alert_id)
    if not alert:
        abort(404)

    return jsonify(alert.to_dict())


@app_routes.route('/alerts/<alert_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete_state.yml', methods=['DELETE'])
def delete_alert(alert_id):
    """
    Deletes a State Object
    """

    alert = storage.get(Alert, alert_id)

    if not alert:
        abort(404)

    storage.delete(alert)
    storage.save()

    return make_response(jsonify({}), 200)


@app_routes.route('/alerts', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post_state.yml', methods=['POST'])
def post_alert():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Alert(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_routes.route('/alerts/<alert_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/put_state.yml', methods=['PUT'])
def put_alert(alert_id):
    """
    Updates a State
    """
    alert = storage.get(Alert, alert_id)

    if not alert:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(alert, key, value)
    storage.save()
    return make_response(jsonify(alert.to_dict()), 200)