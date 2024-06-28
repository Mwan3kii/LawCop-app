#!/usr/bin/python3
""" Starts a Flash Web Application """
from web_backend.models import storage
from web_backend.models import User
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ
from flask import Flask, render_template, request, redirect, flash, url_for, Blueprint
import requests
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup_page():
    return render_template('signup.html', cache_id=uuid.uuid4())

@auth.route('/account_page')
@login_required
def account_page():
    user = current_user
    return render_template('account.html', user=user)

@auth.route('delete_account', methods=['POST'], strict_slashes=False)
def delete_account():
    """deletes user account"""
    user_api_url = "http://127.0.0.1:5500/api/routes/users/{}".format(current_user.id)
    response = request.delete(user_api_url)
    if response.status_code != 201:
        flash("Server error!, please try again")
        return redirect(url_for('auth.delete_account_page'))
    logout_user()
    return redirect(url_for('alert.html'))

@auth.route('/login')
def login_page():
    return render_template('login.html', cache_id=uuid.uuid4())

@auth.route('/login', methods=['POST'], strict_slashes=False)
def login():
    email_or_name = request.form.get('email_or_name')
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user_api_url = "http://127.0.0.1:5500/api/routes/users"
    response = request.get(user_api_url)
    if response.status_code == 200:
        users = response.json()
        for user_data in users:
            user = User(**user_data)
            if email_or_name == user.email or email_or_name == user.username:
                if check_password_hash(user.password, password):
                    login_user(user, remember=remember)
                    return redirect(url_for('alerts.html'))
                else:
                    flash('Invalid password')
                    return redirect(url_for('auth.login_page'))
    flash("User doesnt exist! Try again")
    return redirect(url_for('auth.login_page'))

@auth.route('/signup', methods=['POST'], strict_slashes=False)
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    remember = True if request.form.get('remember') else False
    data = {"email":email, "password":password, "username": username}
    user_api_url = "http://127.0.0.1:5500/api/routes/users"
    response = requests.post(user_api_url, json=data)
    if response.status_code in [400, 409]:
        flash("{}".format(response.json().get('error')))
        return redirect(url_for('auth.signup_page'))
    elif response.status_code != 201:
        flash("Error on our side, please try again")
        return redirect(url_for('auth.signup_page'))
    new_user = User(**response.json())
    login_user(new_user, remember=remember)
    return redirect(url_for('login.html'))

@auth.route('/logout')
def logout():
    print("called logout")
    logout_user()
    print(current_user)
    print("exiting logout")
    return redirect(url_for('signing.html'))

if __name__ == "__alert__":
    """Main function"""
    app.run(host='0.0.0.0', port=5500)