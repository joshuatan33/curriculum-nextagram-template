from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from models.user import User

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/sign_up', methods=['GET'])
def sign_up():
    return render_template('signup form.html')


@users_blueprint.route('/sign_up_form', methods=['POST'])
def user_create():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    new_user = User(name=username, password=password, email=email)

    if new_user.save():
        flash("Successfully Created")
        return redirect(url_for("users.sign_up"))
    else:
        return render_template('signup form.html', email=request.form['email'], errors=new_user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass


# @app.route("/sign_up")
# def sign_up():
#     return render_template('signup form.html')


# @app.route("/sign_up_form", methods=['POST'])
# def user_create():
#     username = request.form.get('username')
#     password = request.form.get('password')
#     hashed_password = generate_password_hash(password)
#     email = request.form.get('email')
#     new_user = User(name=username, password=hashed_password, email=email)
#     if new_user.validate() != []:
#         if new_user.save():
#             flash("Successfully Created")
#             return redirect(url_for("sign_up"))
#         else:
#             return render_template('home.html')
#     else:
#         return render_template('signup form.html', email=request.form['email'], errors=self.errors)
