from app import app, db, admin
from flask import render_template, flash, redirect, request
from flask_admin.contrib.sqla import ModelView
from .forms import WelcomeForm, LoginForm, ArticleForm
from .models import User, Article, Category
from .Library import *
from flask_login import LoginManager, login_user, logout_user
from flask_login import login_required, current_user
import logging
import json

logging.basicConfig(filename="log.log", encoding="utf-8", level=logging.DEBUG)

# Below lines used for rendering admin view, potential
# security risk if remains uncommented
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Article, db.session))
# admin.add_view(ModelView(Category, db.session))

# Setup the flask-login tools
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
def index():
    '''
    Main page for the website, containg the username field.
    '''
    if not current_user.is_authenticated:
        form = WelcomeForm()
        if form.validate_on_submit():
            logging.info("Validated welcome form")
            form = LoginForm(username=form.username.data)
            if user_exists((form.username.data)):
                logging.info("Redirected to /login/"+form.username.data)
                return redirect("/login/"+form.username.data)
            else:
                logging.info("Redirected to /signup/"+form.username.data)
                return redirect("/signup/"+form.username.data)
        return render_template("welcome.html",
                               title="Connect & Reflect",
                               form=form)
    else:
        return redirect("/discover")


@app.route("/login/", methods=["GET", "POST"])
@app.route("/login/<string:username>", methods=["GET", "POST"])
def login(username=None):
    '''
    Login page for returning users, passes through to the
    discover page if the credentials are valid.
    '''
    form = LoginForm(username=username)
    if form.validate_on_submit():
        logging.info("Validated signin form")
        if check_creds(form.username.data, form.password.data):
            signed_in_as = form.username.data
            user_id = get_id("user", signed_in_as)
            user_object = User.query.get(user_id)
            login_user(user_object)
            return redirect("/")
        flash("Invalid username and password combination")
    return render_template("login.html",
                           title="Login",
                           form=form, submit_message="Log In")


@app.route("/signup/", methods=["GET", "POST"])
@app.route("/signup/<string:username>", methods=["GET", "POST"])
def signup(username=None):
    '''
    Signup page for new users, passes through
    to the discover page if credentials are new and unique.
    '''
    form = LoginForm(username=username)
    if form.validate_on_submit():
        logging.info("Validated signup form")
        if user_exists(form.username.data.upper()):
            flash("""The username chosen is taken.
                  If this is you, please sign in.""")
            return render_template("signup.html",
                                   title="Sign Up",
                                   form=form, submit_message="Sign Up")

        hashed_password = hash_data(form.password.data)
        user = User(username=form.username.data.upper(),
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        logging.info("Redirected to base")
        signed_in_as = form.username.data
        user_id = get_id("user", signed_in_as)
        user_object = User.query.get(user_id)
        login_user(user_object)
        return redirect("/")
    return render_template("signup.html",
                           title="Sign Up",
                           form=form, submit_message="Sign Up")


@app.route("/discover")
@login_required
def discover():
    '''
    Renders the main discover page - if the user is authenticated.
    Lists all the articles in order of number of likes.
    '''
    return render_template("discover.html", title="Discover",
                           username=current_user.username,
                           all_articles=Article.query.order_by
                           (Article.likes.desc()).all())


@app.route("/portfolio")
@login_required
def portfolio():
    '''
    Renders the portfolio page - listing all the articles written by
    the user signed in. Requires the user to be signed in.
    '''
    user_id = get_id("user", current_user.username)
    user_articles = Article.query.filter_by(author_id=user_id).all()
    total_reactions = 0
    for article in user_articles:
        total_reactions += (article.likes + article.laughs +
                            article.grimaces + article.blanks +
                            article.surprises)
    return render_template("portfolio.html",
                           title="Portfolio",
                           all_articles=user_articles,
                           total_reactions=total_reactions)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    '''
    Renders the page for writing an article, and adds it to the database
    when submitted. Requires the user to be signed in.
    '''
    form = ArticleForm()
    if form.validate_on_submit():
        logging.info("Validated Article Form")
        status = validate_article(form.title.data, form.content.data)
        logging.info(status)
        if not status:
            flash(status)
            return render_template("create.html",
                                   title="Write Article",
                                   form=ArticleForm(title=form.title.data,
                                                    content=form.content.data,
                                                    category=form.category.
                                                    data,
                                                    submit_message="""
Create Article"""
                                                    ))
        category_id = get_id("category", form.category.data)
        author_id = get_id("user", current_user.username)
        article = Article(title=form.title.data, content=form.content.data,
                          category_id=category_id, author_id=author_id)
        db.session.add(article)
        db.session.commit()
        return redirect("/portfolio")

    return render_template("create.html",
                           title="Write Article",
                           form=form,
                           submit_message="Create Article")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    '''
    Opens up an article for editing, if the user is the owner
    of the article they are attempting to edit. Handles
    editing the article in the database if edits are made.
    Requires the user to be signed in.
    '''
    article = Article.query.get(id)
    if article.author_id != get_id("user", current_user.username):
        return redirect("/discover")
    form = ArticleForm(title=article.title,
                       content=article.content, category=article.category)
    if form.validate_on_submit():
        logging.info("Validated Article Form")
        status = validate_article(form.title.data,
                                  form.content.data,
                                  article.title,
                                  article.content)
        logging.info(status)
        if not status:
            flash(status)
            return render_template("edit.html",
                                   title="Edit Article",
                                   form=ArticleForm(title=form.title.data,
                                                    content=form.content.data,
                                                    category=form.category.
                                                    data),
                                   submit_message="Edit Article")
        article.title = form.title.data
        article.content = form.content.data
        article.category_id = get_id("category", form.category.data)
        db.session.commit()
        return redirect("/portfolio")
    return render_template("edit.html",
                           title="Edit Article",
                           form=form,
                           submit_message="Edit Article")


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    '''
    Responsible for deleting an article from the database,
    if the article requested for deletion was published by
    the signed in user.
    Requires the user to be signed in.'''
    article = Article.query.get(id)
    if article.author_id != get_id("user", current_user.username):
        return redirect("/discover")
    db.session.delete(article)
    db.session.commit()
    return redirect("/portfolio")


@app.route("/view/<int:id>")
@login_required
def view(id):
    '''
    Creates an enlarged page to view an individual article
    '''
    article = Article.query.get(id)
    return render_template("view_article.html",
                           title=article.title,
                           article=article)


@app.route("/react", methods=["POST"])
@login_required
def react():
    '''
    Handles the addition of the reactions to the backend
    database for the article which has recieved a reaction.
    '''
    data = request.get_json()
    logging.info(data)
    article_id = int(data.get("article_id"))
    reaction = data.get("reaction")
    article = Article.query.get(article_id)
    if reaction == "likes":
        logging.info("here")
        article.likes += 1
    elif reaction == "laughs":
        article.laughs += 1
    elif reaction == "grimaces":
        article.grimaces += 1
    elif reaction == "blanks":
        article.blanks += 1
    elif reaction == "surprises":
        article.surprises += 1

    db.session.commit()

    return json.dumps({
        "status": "OK",
        "likes": article.likes,
        "laughs": article.laughs,
        "grimaces": article.grimaces,
        "blanks": article.blanks,
        "surprises": article.surprises
    })


@app.route("/quit")
@login_required
def quit():
    '''
    Logs out the user, ending the session and returning
    to the main welcome screen.
    '''
    logout_user()
    return redirect("/")
