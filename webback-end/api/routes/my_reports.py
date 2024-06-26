#!/usr/bin/python3
""" objects that handles all default RestFul API actions for cities """
from models.user import User
from models.reports import Report
from models import storage
from api.routes import app_routes
from flask import abort, jsonify, make_response, request, render_template
from flasgger.utils import swag_from

@app_routes.route('/my_reports', methods=['GET'], strict_slashes=False)
@login_required
def get_reports():
    user = storage.get(User, user.id)
    if not user:
        abort(404)
    reports = [report.to_dict() for report in user.reports]
    return jsonify(reports)

@app_routes.route('/my_reports/<report_id>', methods=['GET'])
@login_required
def get_report(report_id):
    report = storage.get(Report, report_id)
    if not report or report.user_id != user.id:
        abort(404)
    
    return jsonify(report.to_dict())

@app_routes.route('/my_reports', methods=['GET'])
@login_required
def my_reports():
    user = current_user
    reports = user.reports
    return render_template('my_reports.html', reports=reports)