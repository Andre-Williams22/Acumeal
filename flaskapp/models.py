from datetime import datetime 
from flaskapp import db 


# Models for Database 
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}' "
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    meal_plan = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Posts', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.meal_plan}')"


# $python 
# from flaskapp import db
# db.create_all()
# from flaskapp.models import User, Posts
# user_1 = User(username='corey',email='c@gmail.com',meal_plan='low', password='password')
# db.session.add(user_1)
# db.session.commit()

# queries
# User.query.all()
# User.query.first()
# User.query.filter_by(username='corey').all()
# user = User.query.get(1)
# user.posts
# db.drop_all() ## deletes everything in our database