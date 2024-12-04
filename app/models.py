from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    '''
    A database class holding the information about each user

    @fields
    Integer id - Primary Key: Unique ID for each user
    String username: Unique uppercase username for each user
    String password: Password of the user
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300), unique=True)
    password = db.Column(db.String(300))
    articles = db.relationship("Article", backref="user", lazy="dynamic")
    authenticated = False

    def __repr__(self):
        # Return the table row for the current user
        return '{}{}{}'.format(self.id, self.username, self.password)

    def get_id(self):
        # Returns the id for the current user
        return str(self.id)

    def is_authenticated(self):
        # Returns whether the user is signed in
        return self.authenticated

    def is_active(self):
        # Returns whether the user is active or depriciated
        # This isn't actually relevant to this program, but
        # is required for flask-login
        return True

    def is_anonymous(self):
        # Returns whether the user is an 'anonymous' user
        # Again not necessary, since my website does not
        # allow anonymous users
        return False


class Article(db.Model):
    '''
    A database class holding the information about the articles
    published on the website.

    @Fields
    Integer id - Primary Key: Unique ID assigned for each article
    String title: Title of the article
    String (long) content: Large field for the article contents
    Integer likes: Number of like reactions the article has recieved
    Integer laughs: Number of laugh reactions the article has recieved
    Integer grimaces: Number of grimace reactions the article has recieved
    Integer blanks: Number of blank reactions the article has recieved
    Integer surprises: Number of surprise reactions the article has recieved
    Integer author_id - Foreign Key: user ID of
                        the user who created the article
    Integer category_id - Foreign Key: ID of the category type of the article
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    content = db.Column(db.String(100000))
    likes = db.Column(db.Integer, default=0)
    laughs = db.Column(db.Integer, default=0)
    grimaces = db.Column(db.Integer, default=0)
    blanks = db.Column(db.Integer, default=0)
    surprises = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        # Return the table row for the current article
        return '{}{}{}{}{}'.format(self.id, self.title,
                                   self.content, self.author, self.category)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(300), unique=True)
    articles = db.relationship("Article", backref="category", lazy="dynamic")

    def __repr__(self):
        # Return the table row for the current category
        return '{}{}'.format(self.id, self.category)
