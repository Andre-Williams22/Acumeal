from datetime import datetime 
from flaskapp import db, login_manager
# used to manage our sessions
from flask_login import UserMixin

@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))


# Models for Database 
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}' "

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # not columns but is a query that allows us to grab this data from our users
    posts = db.relationship('Posts', backref='author', lazy=True) # related to posts: 1 to many relationship
    mealplan = db.relationship('Mealplan', backref='author', lazy=True) # 1 to many relationship with user
    meal = db.relationship('Meal', backref='author', lazy=True) 

    #meal = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)

    def __repr__(self): # makes our object a string when it's printed when we print it out
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# quiz form data
class Mealplan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(20), nullable=False)
    last = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    allergies = db.Column(db.String(20), nullable=False)
    exercise = db.Column(db.String(20), nullable=False)
    high_bp = db.Column(db.String(20), nullable=False)
    diabetes = db.Column(db.String(20), nullable=False)
    muscle_building = db.Column(db.String(20), nullable=False)
    weight_loss = db.Column(db.String(20), nullable=False)
    hungry_often = db.Column(db.String(20), nullable=False)
    eat_snacks = db.Column(db.String(20), nullable=False)
    # references user class that creates a relationship between meapl plan and user 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"MealPlan('{self.age}', '{self.gender}', '{self.exercise}')"

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.String(20), nullable=False)
    breakfast = db.Column(db.String(20), nullable=False)
    lunch = db.Column(db.String(20), nullable=False)
    dinner = db.Column(db.String(20), nullable=False)
    snack = db.Column(db.String(20), nullable=False)
    total = db.Column(db.String(20), nullable=False)
    measurement = db.Column(db.String(20), nullable=False)
    # one mealplan has many users 
   #user = db.relationship('User', backref='user', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"{self.week}, {self.breakfast}, {self.lunch}, {self.dinner}, {self.snack}, {self.total}, {self.measurement}"

# $ python 
# from flaskapp import db
# db.create_all()
# from flaskapp.models import User, Posts, Mealplan, Meal
# user_1 = User(username='corey',email='c@gmail.com', password='password')
# db.session.add(user_1)
# db.session.commit()
# mealplan = Mealplan(first='Andre',last='Williams',age=19,gender='male',allergies='No',exercise='Yes',high_bp='No',
#   diabetes='No',muscle_building='Yes',weight_loss='No',hungry_often='No',eat_snacks='No', user_id=user_1)
#  meal_1 = Meal(week='1', breakfast='oatmeal', lunch='potatoes', dinner='salad', snack='cheese', total='200', measurement='grams', user_id=user.id)


# user = User.query.first() or User.query.get(1)
# user.posts
# user.meal

# queries
# User.query.all()
# User.query.first()
# User.query.filter_by(username='corey').all()
# user = User.query.get(1)
# user.posts
# db.drop_all() ## deletes everything in our database