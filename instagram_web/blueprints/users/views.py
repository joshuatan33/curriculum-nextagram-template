from flask import Blueprint, render_template, request, flash, redirect, url_for, session, escape, abort
from werkzeug.security import generate_password_hash
from models.user import User
from flask_login import current_user, login_required, logout_user, login_user

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')


@users_blueprint.route('/sign_up', methods=['GET'])
def sign_up():
    if current_user.is_active:
        return redirect(url_for('home'))
    return render_template('signup form.html')


@users_blueprint.route('/sign_up_form', methods=['POST'])
def user_create():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    new_user = User(name=username, password=password, email=email)

    if new_user.save():
        flash("Successfully Created")
        login_user(new_user)
        return redirect(url_for("users.show", username=current_user.name))
    else:
        return render_template('signup form.html', email=request.form['email'], errors=new_user.errors)


@users_blueprint.route('/sign_in', methods=['GET'])
def sign_in():
    if current_user.is_active:
        return redirect(url_for("users.show", username=current_user.name))
    return render_template('signin form.html')


@users_blueprint.route('/sign_in_form', methods=['POST'])
def user_show():
    current_username = request.form.get('username')
    current_password = request.form.get('password')
    current_person = User.get_or_none(User.name == current_username)

    if current_person != None:
        if current_person.login_validate(current_password):
            login_user(current_person)
            flash('Successfully signed in')
            return redirect(url_for('users.show', username=current_username))
        else:
            return render_template('signin form.html', errors=current_person.errors)
    else:
        flash('Username not found! Please sign up for an account.')
        return render_template('signin form.html')


@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    if current_user.is_active:
        return render_template('userpage.html', username=current_user.name)
    else:
        return render_template(url_for('user.login'))


@users_blueprint.route('/', methods=["GET"])
@login_required
def index():
    if current_user.is_active:
        return render_template('userpage.html', username=current_user.name)
    else:
        return render_template(url_for('user.login'))


@users_blueprint.route('/<uid>/edit', methods=['GET'])
@login_required
def edit(uid):
    if current_user.is_active:
        if int(uid) == current_user.id:
            return render_template('edit form.html', uid=current_user.id, username=current_user.name)
        else:
            abort(401)
    return redirect(url_for("users.sign_in"))


@users_blueprint.route('/<uid>', methods=['POST'])
def update(uid):
    new_username = request.form.get('username')
    new_password = request.form.get('password')
    current_person = User.get_or_none(User.id == uid)

    if current_person != None:
        if new_password == '':
            current_person = User.update(
                name=new_username
            ).where(User.id == uid)
        else:
            if current_user.login_validate(new_password):
                current_person = User.update(
                    name=new_username,
                    password=generate_password_hash(new_password)
                ).where(User.id == uid)
            else:
                flash('Failed to update: Password does not match requirements! Your password must have at least 1 number, 1 UPPER case character and 1 lower case character')
                return redirect(url_for('users.edit', uid=current_user.id))

        if current_person.execute():
            flash('Successfully updated details')
            return redirect(url_for('users.show', username=current_user.name))
        else:
            flash('Failed')
            return redirect(url_for('users.show', username=current_user.name))
    else:
        flash('Username not found! Please sign up for an account.')
        return render_template('signin form.html')


@users_blueprint.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('home'))
