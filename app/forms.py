from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from .Library import get_all_categories

class WelcomeForm(FlaskForm):
    '''
    Form class holding the fields for initial sign up/sign in to the app
    '''
    username = StringField("Title", validators=[DataRequired(),
                                                Length(min=1,max=299)])

class LoginForm(WelcomeForm):
    '''
    Form class holding the fields for data entry into the database
    '''
    password = PasswordField("Password", validators=[DataRequired(),
                                                   Length(min=7,max=299)])


class ArticleForm(FlaskForm):
    '''
    Form class holding the fields for creating an article
    '''
    title = StringField("Title", validators=[DataRequired(),
                                             Length(min=1,max=299)])
    content = TextAreaField("Content",validators=[DataRequired(),
                                                Length(min=1,max=99999)])
    categories = get_all_categories()
    category = SelectField("Category",choices=categories)