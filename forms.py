from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Optional


class RegisterUserForm(FlaskForm):
    username = StringField("Enter your username", validators=[
                           InputRequired(message="Your username cannot be left blank")])
    password = PasswordField("Enter your password", validators=[
                           InputRequired(message="Your password cannot be left blank")])
    email = StringField("Enter your email", validators=[
                           InputRequired(message="Your email cannot be left blank"), Email("Email Required")])
    first_name = StringField("Enter your first name", validators=[
                             InputRequired(message="Your first name cannot be left blank")])
    last_name = StringField("Enter your last name", validators=[
                            InputRequired(message="Your last name cannot be left blank")])


class LoginForm(FlaskForm):
    username = StringField("Enter your username", validators=[
                           InputRequired(message="Your username cannot be left blank")])
    password = PasswordField("Enter your password", validators=[
                           InputRequired(message="Your password cannot be left blank")])
    
    
class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(message="Please enter a title")])
    content = StringField("Content", validators=[InputRequired(message="Please fill in this section")])
    
    
class EditFeedbackForm(FlaskForm):
    title = StringField("Title", validators=[Optional()])
    content = StringField("Content", validators=[Optional()])