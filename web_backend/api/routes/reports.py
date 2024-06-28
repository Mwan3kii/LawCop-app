#!/usr/bin/python3
""" objects that handles all default RestFul API actions for cities """
from models.user import User
from models.reports import Report
from models import storage
from api.routes import app_routes
from flask import abort, jsonify, make_response, request, render_template, flash, url_for, redirect
from flasgger.utils import swag_from


@app_routes.route('/report/<state_id>/reports', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/reports/reports.yml', methods=['GET'])
def get_reports(user_id):
    """
    Retrieves the list of all cities objects
    of a specific State, or a specific city
    """
    list_reports = []
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    for rep in user.report:
        list_reports.append(rep.to_dict())

    return jsonify(list_reports)


@app_routes.route('/reports/<report_id>/', methods=['GET'], strict_slashes=False)
@swag_from('documentation/report/get_report.yml', methods=['GET'])
def get_report(user_id):
    """
    Retrieves a specific report based on user id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_routes.route('/reports/<report_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/report/delete_report.yml', methods=['DELETE'])
def delete_report(report_id):
    """
    Deletes a report based on id provided
    """
    report = storage.get(Report, report_id)

    if not report:
        abort(404)
    storage.delete(report)
    storage.save()

    return make_response(jsonify({}), 200)

@app_routes.route('/report/<report_id>', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/report/create_report.yml', methods=['POST'])
def create_report(report_id):
    """
    Creates a report
    """
    if request.method == 'POST':
        data = request.form
        if 'title' not in data or 'description' not in data:
            flash("Missing title or description", "danger")
            return render_template('report.html')

        new_report = Report(
            user_id=user.id,
            title=data['title'],
            description=data['description'],
            location=data['location']
        )
        storage.add(new_report)
        storage.save()
        flash("Report created successfully!", "success")
        return redirect(url_for('my_reports.html', user_id=user.id))

    return render_template('report.html')


@app_routes.route('/report/<report_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/report/update_report.yml', methods=['PUT'])
def update_report(report_id):
    """
    Updates a report
    """
    report = storage.get(Report, report_id)
    if not report:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'report_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(report, key, value)
    storage.save()
    return make_response(jsonify(report.to_dict()), 200)