from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, DataRequired, Length, EqualTo

class Registration_form(FlaskForm):
    
    email = StringField('email', validators = [Email(), DataRequired()])
    username = StringField('username', validators = [ DataRequired(), Length(min=2, max=30) ] )
    password = PasswordField('password', validators = [ DataRequired()] )
    confirm_password = PasswordField('confirm_password', validators = [ DataRequired(), EqualTo('password')] )
    submit = SubmitField('Sign up')
    
    
class login_form(FlaskForm):
    
    email = StringField('email', validators = [Email(), DataRequired()])
    password = PasswordField('password', validators = [ DataRequired()] )
    remember = BooleanField('Remember me')
    submit = SubmitField('login')
    
