from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    '''
    A database class holding the information about each user
    id: Unique ID for each user
    username: Unique uppercase username for each user
    password: Password of the user 
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300), unique=True)
    password = db.Column(db.String(300))
    articles = db.relationship("Article", backref="user", lazy="dynamic")
    authenticated = False

    def __repr__(self):
        return '{}{}{}'.format(self.id, self.username, self.password)
    
    def get_id(self):
        return str(self.id)
    
    def is_authenticated(self):
        return self.authenticated
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False


class Article(db.Model):
    '''
    A database class holding the information about the articles 
    published on the website.
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    content = db.Column(db.String(100000))
    likes = db.Column(db.Integer,default=0)
    laughs = db.Column(db.Integer,default=0)
    grimaces = db.Column(db.Integer,default=0)
    blanks = db.Column(db.Integer,default=0)
    surprises = db.Column(db.Integer,default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    def __repr__(self):
        return '{}{}{}{}{}'.format(self.id,self.title,self.content,self.author,self.category)

class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(300), unique=True)
    articles = db.relationship("Article", backref="category", lazy="dynamic")
    def __repr__(self):
        return '{}{}'.format(self.id,self.category)
