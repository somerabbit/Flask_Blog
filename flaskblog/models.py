from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):  # create User class
    id = db.Column(db.Integer, primary_key=True)   
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  #create relationship with Post. set up 'author' to locate the person of a post. lazy:load data from database. 

    def __repr__(self): # represent string 
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):  # create User class
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # user.id connect to id in User class

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"