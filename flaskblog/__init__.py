from flask import Flask #import flask modules. 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import subprocess
from sqlalchemy.engine.create import create_engine

# Get the Database URL using Heroku CLI
# -------------------------------------
# Running the following from Python: $heroku config:get DATABASE_URL --app your-app-name
heroku_app_name = "your-app-name"

# Assumption: HEROKU_API_KEY is set in your terminal
# You can confirm that it's set by running the following python command os.environ["HEROKU_API_KEY"]
raw_db_url = subprocess.run(
    ["heroku", "config:get", "DATABASE_URL", "--app", heroku_app_name],
    capture_output=True  # capture_output arg is added in Python 3.7
).stdout 

# Convert binary string to a regular string & remove the newline character
db_url = raw_db_url.decode("ascii").strip()

# Convert "postgres://<db_address>"  --> "postgresql+psycopg2://<db_address>" needed for SQLAlchemy
final_db_url = "postgresql+psycopg2://" + db_url.lstrip("postgres://")  # lstrip() is more suitable here than replace() function since we only want to replace postgres at the start!


# Create SQLAlchemy engine
# ------------------------
engine = create_engine(final_db_url)


app = Flask(__name__)  #create Flask project 
app.config['SECRET_KEY']='8cea2065c057138b1193f0134c0f0c7e' #set up key to protect web application
app.config['SQLALCHEMY_DATABASE_URI'] =final_db_url #'postgresql+psycopg2://postgres:somerabbit@ec2-23-21-215-184.compute-1.amazonaws.com:5432/flaskblog?sslmode=require'   #set databse URI at sqlite  #'sqlite:///site.db' # 



db=SQLAlchemy(app) #set db by using SQLAlchemy class with input app
bcrypt =Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'
from flaskblog import routes
