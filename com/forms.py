from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from com.models import UsersDB
from com import BCRYPT

class RegisterForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=4, max=30), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Your Account')

    def validate_username(self, username):
        user = UsersDB.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already taken!")

    def validate_email(self, email):
        email_add = UsersDB.query.filter_by(email=email.data).first()
        if email_add:
            raise ValidationError("This email is already registered!")

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')

class PurchaseForm(FlaskForm):
    submit = SubmitField(label='Confirm Purchase')

class SellForm(FlaskForm):
    submit = SubmitField(label='Confirm Sell')