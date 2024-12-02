import hashlib, logging
from .models import User, Article, Category
from app import app


def check_creds(username,password):
    all_users = User.query.all()
    for user in all_users:
        if user.username == username.upper() and user.password == hash_data(password):
            return True
    return False

def validate_article(title,content):
    all_articles = Article.query.all()
    for article in all_articles:
        if article.title == title:
            return "There is already an article with that name. Please choose a different name for your article."
        if article.content == content:
            return "The content of the article is a copy of a previously existing article."
    return True

def hash_data(data):
    hasher = hashlib.new("sha256")
    hasher.update(data.encode())
    return hasher.hexdigest()

def get_by_id(table,data):
    if table == "category":
        for item in Category.query.all():
            if item.category == data:
                return item.id
    elif table == "user":
        for item in User.query.all():
            if item.username == data.upper():
                return item.id
    elif table == "article":
        for item in Article.query.all():
            if item.title == data:
                return item.id
    else:
        logging.error("Error in Library - get_by_id: Unable to detect table")
        return False
    return False

def get_all_categories():
    with app.app_context():
        categories = []
        for item in Category.query.all():
            categories.append(item.category)
        return categories

def user_exists(user):
    '''
    Find if a username is in the database, return True if they are, False if not
    '''
    if User.query.filter_by(username=user.upper()).first():
        return True
    return False
