from flask_wtf import FlaskForm # used to write forms that will convert them into html 
from flask_babel import Babel as gettext, lazy_gettext
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
        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError('That email is already taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    
    # allows users to stay logged in by using a secure cookie
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class QuizForm(FlaskForm):
    first = StringField('First Name', [validators.InputRequired()])
    last = StringField('Last Name', [validators.InputRequired()])
    age = IntegerField('Age',[validators.NumberRange(min=10, message='Must be at least %(min)d years old.')])
    gender = StringField('Gender', [validators.InputRequired(message='What is your gender? Male or Female')])
    allergies = StringField('Do You Have Allergies? Yes or No', [validators.InputRequired(message='Do you have allergies? Yes or No')])
    exercise = StringField('Do you Exercise More than 3 times a week? Yes or No', [validators.InputRequired(message='Do you workout more than 3 days a week? Yes or No')])
    high_bp = StringField('Do you have High Blood Pressure? Yes or No', [validators.InputRequired(message='Do you have high blood pressure? Yes or No')])
    diabetes = StringField('Do you have Diabetes yes or no?', [validators.InputRequired(message='Do you have diabetes? Yes or No')])
    muscle_building = StringField('Are you trying to build muscle? Yes or No', [validators.InputRequired(message='Are you trying to build muscle? Yes or No')])
    weight_loss = StringField('Are you trying to loss weight? Yes or No', [validators.InputRequired(message='Are you trying to lose weight? Yes or No')])
    hungry_often = StringField('Are you hungry often? Yes or No', [validators.InputRequired(message='Are you hungry often? Yes or No')])
    eat_snacks = StringField('Do you eat snacks? Yes or No', [validators.InputRequired(message='Do you eat snacks? Yes or No')])

    submit = SubmitField('View Free Plan')
