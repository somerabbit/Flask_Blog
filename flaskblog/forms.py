from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from flaskblog.models import User
class RegistrationForm(FlaskForm):
    username =StringField('Username',
                            validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password= PasswordField('Password',validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])

    submit=SubmitField('Sign up')

    def validate_username(self,username):  #check if username is exist in db. here username is variable input from above
        user=User.query.filter_by(username=username.data).first() # use username to search if user is exist
        if user: #if user is exist 
            raise ValidationError('That username is taken. Please choose a different one ')
 
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()# use email to search if user is exist
        if user:
            raise ValidationError('That email is taken. Please choose a different one ')

class LoginForm(FlaskForm):
    email=StringField('Email',
                      validators=[DataRequired(),Email()])

    password= PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')