from flask import Blueprint, render_template, request, flash, redirect, url_for, session, escape, abort
from werkzeug.security import generate_password_hash
from models.user import User

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')


@users_blueprint.route('/sign_up', methods=['GET'])
def sign_up():
    if 'username' in session:
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
        session['username'] = username
        return redirect(url_for("users.show", username=username))
    else:
        return render_template('signup form.html', email=request.form['email'], errors=new_user.errors)


@users_blueprint.route('/sign_in', methods=['GET'])
def sign_in():
    if 'username' in session:
        return redirect(url_for("users.show", username=username))
    return render_template('signin form.html')


@users_blueprint.route('/sign_in_form', methods=['POST'])
def user_show():
    current_username = request.form.get('username')
    current_password = request.form.get('password')
    current_user = User.get_or_none(User.name == current_username)

    if current_user != None:
        if current_user.login_validate(current_password):
            session['username'] = current_username
            session['uid'] = current_user.id
            flash('Successfully signed in')
            return redirect(url_for('users.show', username=current_username))
        else:
            return render_template('signin form.html', errors=current_user.errors)
    else:
        flash('Username not found! Please sign up for an account.')
        return render_template('signin form.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    if 'username' in session:
        return render_template('userpage.html', username=username)
    else:
        return render_template(url_for('user.login'))


@users_blueprint.route('/logout', methods=["GET"])
def logout():
    session.pop('username', None)
    session.pop('uid', None)
    return redirect(url_for('home'))


@users_blueprint.route('/', methods=["GET"])
def index():
    if 'username' in session:
        return render_template('userpage.html', username=session['username'])
    else:
        return render_template(url_for('user.login'))


@users_blueprint.route('/<uid>/edit', methods=['GET'])
def edit(uid):
    if 'uid' in session:
        if int(uid) == session['uid']:
            return render_template('edit form.html', uid=session['uid'], username=session['username'])
        else:
            abort(401)
    return redirect(url_for("users.sign_in"))


@users_blueprint.route('/<uid>', methods=['POST'])
def update(uid):
    new_username = request.form.get('username')
    new_password = request.form.get('password')
    current_user = User.get_or_none(User.id == uid)

    if current_user != None:
        if new_password == '':
            current_user = User.update(
                name=new_username
            ).where(User.id == uid)
        else:
            if current_user.login_validate(new_password):
                current_user = User.update(
                    name=new_username,
                    password=generate_password_hash(new_password)
                ).where(User.id == uid)
            else:
                flash('Failed to update: Password does not match requirements! Your password must have at least 1 number, 1 UPPER case character and 1 lower case character')
                return redirect(url_for('users.edit', uid=session['uid']))

        if current_user.execute():
            flash('Successfully updated details')
            session['username'] = new_username
            return redirect(url_for('users.show', username=session['username']))
        else:
            flash('Failed')
            return redirect(url_for('users.show', username=session['username']))
    else:
        flash('Username not found! Please sign up for an account.')
        return render_template('signin form.html')
