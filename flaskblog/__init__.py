from flask import Flask #import flask modules. 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)  #create Flask project 
app.config['SECRET_KEY']='8cea2065c057138b1193f0134c0f0c7e' #set up key to protect web application

# run program at different mode-----------------------------------------------------------------------
ENV='prod'
if ENV=='dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:somerabbit@localhost/blog'

else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://edgsqtentxumxq:5a8815f18889fcbd5c6755b4a6269ae826215773abb8940af9de4f684a12e371@ec2-34-228-100-83.compute-1.amazonaws.com:5432/d20c58lko8m93n' #set databse URI at sqlite  #'sqlite:///site.db' # 
#------------------------------------------------------------------------------------------------

db=SQLAlchemy(app) #set db by using SQLAlchemy class with input app
bcrypt =Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'
from flaskblog import routes
