from flask import redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from general import cardb, database
from general.forms_users import LoginForm, RegistrationForm
from general.models.user import User


@cardb.route("/user/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:

        flash("You are already logged in.", "info")
        return redirect(url_for("overview_instances"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter(User.username == form.username.data).first()

        if user is None or not user.check_password(form.password.data):

            flash("Incorrect username or password.", "warning")
            return redirect(url_for("login"))

        else:

            login_user(user, remember=form.remember_me.data)
            flash("You have successfully logged in.", "success")

            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('overview_instances')
            return redirect(next_page)

    return render_template("users_login.html",
                           title="Log in",
                           heading="Log in",
                           form=form)


@cardb.route("/user/logout", methods=['GET', 'POST'])
def logout():

    logout_user()
    return redirect(url_for("overview_instances"))


@cardb.route("/user/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("overview_instances"))

    form = RegistrationForm()
    users = User.query.all()

    if form.validate_on_submit():

        new_user = User()
        new_user.username = form.username.data
        new_user.set_password(form.password_1.data)

        if len(users) >= 1:
            flash("Only one user in this app is allowed.", "warning")
            return redirect(url_for('overview_instances'))

        database.session.add(new_user)
        database.session.commit()

        flash("The new user {} has been registered.".format(new_user.username), "success")
        return redirect(url_for('login'))

    return render_template('users_register.html',
                           title='Register',
                           heading="Register a new user",
                           form=form)
