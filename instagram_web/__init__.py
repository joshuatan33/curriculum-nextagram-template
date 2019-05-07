from app import app
from flask import render_template, Flask, request, redirect, url_for, flash
from instagram_web.blueprints.users.views import users_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/sign_up")
def sign_up():
    return render_template('signup form.html')


@app.route("/sign_up_form", methods=['POST'])
def user_create():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    new_user = User(name=username, password=password, email=email)

    if new_user.save():
        flash("Successfully Created")
        return redirect(url_for("sign_up"))
    else:
        return render_template('home.html')
