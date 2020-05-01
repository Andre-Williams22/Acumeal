from flask_wtf import FlaskForm # used to write forms that will convert them into html 
from flask.ext.babel import Babel as lazy_gettext
from flask_babel import Babel
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError 
from flaskapp.models import User 

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4, max=20), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError('That email is already taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    
    # allows users to stay logged in by using a secure cookie
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class QuizForm(FlaskForm):
    name = StringField(lazy_gettext(u'Name'), [validators.InputRequired(lazy_gettext(u'Please provide your name'))])
    age = IntegerField(lazy_gettext(u'Age'),[validators.NumberRange(min=10, message=lazy_gettext(u'Must be at least %(min)d years old.'))])
    gender = StringField(lazy_gettext(u'Gender'), [validators.InputRequired(lazy_gettext(u'What is your gender? Male or Female'))])
    allergies = StringField(lazy_gettext(u'Allergies'), [validators.InputRequired(lazy_gettext(u'Do you have allergies? Yes or No'))])
    exercise = StringField(lazy_gettext(u'Exercise'), [validators.InputRequired(lazy_gettext(u'Do you workout more than 3 days a week? Yes or No'))])
    high_bp = StringField(lazy_gettext(u'High Blood Pressure'), [validators.InputRequired(lazy_gettext(u'Do you have high blood pressure? Yes or No'))])
    diabetes = StringField(lazy_gettext(u'Diabetes'), [validators.InputRequired(lazy_gettext(u'Do you have diabetes? Yes or No'))])
    muscle_building = StringField(lazy_gettext(u'Strength Training'), [validators.InputRequired(lazy_gettext(u'Are you trying to build muscle? Yes or No'))])
    weight_loss = StringField(lazy_gettext(u'Weight Loss'), [validators.InputRequired(lazy_gettext(u'Are you trying to lose weight? Yes or No'))])
    hungry_often = StringField(lazy_gettext(u'Apetite'), [validators.InputRequired(lazy_gettext(u'Are you hungry often? Yes or No'))])
    eat_snacks = StringField(lazy_gettext(u'Snacking'), [validators.InputRequired(lazy_gettext(u'Do you eat snacks? Yes or No'))])

    submit = SubmitField('Buy Now')
