# from flask import Flask, redirect, request, render_template, url_for
# from flask_wtf import FlaskForm
# from wtforms.validators import Email, ValidationError, DataRequired, Length
# from wtforms import SelectField, PasswordField, SubmitField, StringField, EmailField, BooleanField

# class registration(FlaskForm):
    
#     username = StringField("username", validators=[DataRequired])
#     password = PasswordField("password", validators=[DataRequired, Length(min=6, max=30)])
#     email = EmailField("email", validators=[DataRequired, Length(min=4, max=6)])
#     submit = SubmitField("submit")
#     remember_me = BooleanField("Remember me")
    
    
    
    
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
        
#         if user:
#             raise ValidationError("This user is already taken")
        
#     def validate_email(self, email):
#         email = User.query.filter_by(email = email.data).first()
#         if email:
#             raise ValidationError("This is already taken")
        
        
# class loginform(FlaskForm):
#     username = StringField("usename", validators=[DataRequired, Length(min=5, max=30)])
#     password = PasswordField("password", validators=[DataRequired, Length(min=6, max=30)])
    
    
    

# class Complaintform(FlaskForm):
    
#     category = SelectField(
#         ("electricity", "Electricity ki ma ki"),
#         ("food", "food ki ma ki"),
#         ("door", "door ki ma ki"),
#     )






# /user.py
