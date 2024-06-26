#!/usr/bin/python3
"""handle all default RestFul API actions for authentication"""
from models.user import User
from models import storage
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from flask import render_template, url_for, redirect, flash
from flasgger.utils import swag_from
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('alerts'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(password, method='sha256')
            new_user = User(username=username, password=hashed_password, email=email)
            storage.add(new_user)
            storage.save
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')


@app_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('/login'))


if __name__ == '__main__':
    app.run(debug=True)
