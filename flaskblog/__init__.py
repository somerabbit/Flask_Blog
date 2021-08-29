from flask import Flask #import flask modules. 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)  #create Flask project 
app.config['SECRET_KEY']='8cea2065c057138b1193f0134c0f0c7e' #set up key to protect web application
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql+psycopg2://postgres:somerabbit@ec2-23-21-215-184.compute-1.amazonaws.com:5432/dd71doth8gopgh?sslmode=require' #set databse URI at sqlite  #'sqlite:///site.db' # 
db=SQLAlchemy(app) #set db by using SQLAlchemy class with input app
bcrypt =Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'
from flaskblog import routes
