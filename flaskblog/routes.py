from flask import render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post



#input data
posts=[
    {
        'author':'Corey Schafer',
        'title':'Blog Post 1',
        'content':'First post content',
        'date_posted':'April 20,2018'
    },
    {
        'author':'Jane Doe',
        'title':'Blog Post 2',
        'content':'Second post content',
        'date_posted':'April 21,2018'
    }

]

#set up website page
@app.route("/")
@app.route("/home") #route to website page "home". 
def home():
    return render_template('home.html',posts=posts) # return information from home.html,input(variable) posts=xxx goes to home.html


@app.route("/about")#route to website page "about". 
def about():
    return render_template('about.html',title='About') # return information from home.html,input(variable) title=xxx goes to about.html

@app.route("/register",methods=['GET','POST']) # allow GET and POST data in this route
def register():
    form=RegistrationForm()  #filling form
    if form.validate_on_submit(): # check if form is filled correctly
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hash password. decode:remove bite at beginning
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)#input user information
        db.session.add(user) # add user in db
        db.session.commit()  # complete adding 
        flash(f'Your account has been created! You are now able to log in','success') #record a message at the end of a request and access it next request and only next request.
        return redirect(url_for('login')) # redirect to home.html
    return render_template('register.html',title='Register', form=form) # return information from home.html,input(variable) form=form goes to home.html. if form is not filled correctly, it will still pass form to register html 

@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    #if form.validate_on_submit():
      # user=User.query.filter_by(email=form.email.data).first()
       #if user and bcrypt.check_password_hash(user.password)
                #flash('Login Unsuccessful. Please check username and password','danger')
    return render_template('login.html',title='Login', form=form)
 