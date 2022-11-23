from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()


class LogInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()


class ReviewForm(FlaskForm):
    dealership_name = StringField('Dealership', validators=[DataRequired()])
    dealership_address = StringField('Address', validators=[DataRequired()])
    rating = StringField('Rating', validators=[DataRequired()])
    msrp = StringField('Dealer MSRP', validators=[DataRequired()])
    markup = StringField('Markup', validators=[DataRequired()])
    sold = StringField('Total Price', validators=[DataRequired()])
    comment = StringField('Comments', validators=[DataRequired()])
    submit = SubmitField()