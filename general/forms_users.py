from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")

    submit = SubmitField("Log in")


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password_1 = PasswordField("Password", validators=[DataRequired()])
    password_2 = PasswordField("Repeat password", validators=[DataRequired(), EqualTo('password_1')])

    submit = SubmitField("Register")
