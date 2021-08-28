import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm,PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/test") #route to website page "home". 
def test():
    
    return render_template('test.html') # return information from home.html,input(variable) posts=xxx goes to home.html



#set up website page
@app.route("/")
@app.route("/home") #route to website page "home". 
def home():
    posts=Post.query.all()
    return render_template('home.html',posts=posts) # return information from home.html,input(variable) posts=xxx goes to home.html


@app.route("/about")#route to website page "about". 
def about():
    return render_template('about.html',title='About') # return information from home.html,input(variable) title=xxx goes to about.html

@app.route("/register",methods=['GET','POST']) # allow GET and POST data in this route
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data) 
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('login.html',title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _, f_ext=os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path=os.path.join(app.root_path, 'static/profile_pics',picture_fn)
    
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()  
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method =='GET':
        print("testing")
        form.username.data=current_user.username
        form.email.data=current_user.email
        print(form.username.data) 

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Accout',image_file=image_file,form=form )


@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        print("testing")
        post=Post(title=form.title.data,content=form.content.data,author=current_user)
        print(post.title)
        db.session.add(post)
        db.session.commit( )
        flash('Your post has been created!','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form,legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)

@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form= PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method =='GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html', title='Update Post',form=form,legend='Update Post')


@app.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    
    return redirect(url_for('home'))
