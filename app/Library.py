import hashlib
import logging
from .models import User, Article, Category
from app import app


def check_creds(username, password):
    '''
    Checks if the password entered by the user
    matches the one in the database.

    @params
    username (String): username to check
    password (String): password to check

    @return
    Boolean True: on valid credentials
    Boolean False: on invalid credentials
    '''
    all_users = User.query.all()
    for user in all_users:
        if (user.username == username.upper() and
                user.password == hash_data(password)):
            return True
    return False


def validate_article(title, content,
                     original_title=None, original_content=None):
    '''
    Checks if the article title and content matches
    the title or content of an article in the database.

    @params
    title (string): title to check
    content (string): content to check
    original_title (string): title to ignore
    original_content(string): content to ignore

    @return
    String: Error message string describing error on matching content
    Boolean True: if no match of title and article
    '''
    all_articles = Article.query.all()
    for article in all_articles:
        if article.title == title and article.title != original_title:
            return """There is already an article with that name.
Please choose a different name for your article."""
        if article.content == content and article.content != original_content:
            return """The content of the article is a copy of
 a previously existing article."""
    return True


def hash_data(data):
    '''
    Hashes the data using an inbuilt python library to enable
    secure storing of passwords.

    @params
    data (String): Data to hash

    @return
    String: Hexadecimal SHA256 hash of the data
    '''
    hasher = hashlib.new("sha256")
    hasher.update(data.encode())
    return hasher.hexdigest()


def get_id(table, data):
    '''
    Converts the main database field of table to the
    ID value in the database.

    @params:
    table (String): table to query one of
                        ("user","category","article")
    data (String): category, username or title of a database item

    @return
    Integer: Database ID of the element found
    Boolean False: Error or ID not found (ie elemtn doesn't exist)
    '''
    if not data:
        return False
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
        logging.error("Error in Library - get_id: Unable to detect table")
        return False
    return False


def get_all_categories():
    '''
    Gets all the categories from the categories table.

    @return
    List: A list of all the categories currently stored in the
          Category table.
    '''
    with app.app_context():
        categories = []
        for item in Category.query.all():
            categories.append(item.category)
        return categories


def user_exists(user):
    '''
    Finds if a username appears in the database

    @params
    String user: username to check

    @return
    Boolean True: If matching username in the database
    Boolean False: If username is not in the databse
    '''
    if User.query.filter_by(username=user.upper()).first():
        return True
    return False
