from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from ..models.user import User

class RegistrationForm(FlaskForm):

    email = StringField(
        'Email',
        validators=[Email(), DataRequired()]
    )

    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=4, max=30)]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6)]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )

    # hostel = StringField(
    #     'Hostel Name',
    #     validators=[DataRequired()]
    # )
    
    hostel = SelectField(
        "Hostel",
        choices=[
            ("SNM", "SNM"),
            ("SJ", "SJ"),
            ("JD", "JD"),
            ("BJ", "BJ"),
            ("Bakhungri", "Bakhungri"),
            ("Gambari", "Gambari"),
        ],
        validators=[DataRequired()]
    )   #new

    room_no = StringField(
        'Room No',
        validators=[DataRequired()]
    )
    

    submit = SubmitField('Sign up')

   
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is already taken. Please choose another one.'
            )
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is already registered. Please choose another one.'
            )


class LoginForm(FlaskForm):

    email = StringField(
        'Email',
        validators=[Email(), DataRequired()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    remember = BooleanField('Remember me')
    submit = SubmitField('Login')




class ComplaintForm(FlaskForm):
    category = SelectField(
        "Category",
        choices=[
            ("Electricity", "Electricity"),
            ("Water", "Water Supply"),
            ("Cleanliness", "Cleanliness"),
            ("Food", "Mess / Food"),
            ("Furniture", "Furniture"),
            ("Internet", "WiFi / Internet"),
            ("Security", "Security"),
            ("Bathroom", "Bathroom / Toilet"),
            ("Other", "Other"),
        ],
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description of Issue",
        validators=[DataRequired()]
    )
    hostel = StringField("Hostel")
    
    image = FileField(
        "Upload Image (optional)",
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "Images only!")
        ]
    )

    submit = SubmitField("Submit Complaint")
