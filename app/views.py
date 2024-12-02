from app import app, db, admin
from flask import render_template, flash, redirect, request
from flask_admin.contrib.sqla import ModelView
from .forms import WelcomeForm, LoginForm, ArticleForm
from .models import User, Article, Category
from .Library import *
import logging, json

logging.basicConfig(filename="log.log",encoding="utf-8",level=logging.DEBUG)
signed_in_as = False
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(Category, db.session))



@app.route("/", methods=["GET","POST"])
def index(username=None):
    # c = Category(category="Cyber Security")
    # db.session.add(c)
    # db.session.commit()
    if not signed_in_as:
        form = WelcomeForm()
        logging.debug("HERE")
        if form.validate_on_submit():
            logging.info("Validated welcome form")
            form = LoginForm(username=form.username.data)
            if user_exists((form.username.data)):
                logging.info("Redirected")
                return redirect("/login/"+form.username.data)
            else:
                logging.info("Redirected")
                return redirect("/signup/"+form.username.data)
        return render_template("welcome.html",
                               title="Connect & Reflect",
                               form=form)
    else:
        return redirect("/discover")

@app.route("/login/",methods=["GET","POST"])
@app.route("/login/<string:username>",methods=["GET","POST"])
def login(username=None):
    global signed_in_as
    form = LoginForm(username=username)
    if form.validate_on_submit():
        logging.info("Validated signin form")
        if check_creds(form.username.data,form.password.data):
            signed_in_as = form.username.data
            return redirect("/")
        flash("Invalid username and password combination")
    return render_template("login.html",
                           title="Login",
                           form=form,submit_message="Log In")

@app.route("/signup/",methods=["GET","POST"])
@app.route("/signup/<string:username>",methods=["GET","POST"])
def signup(username=None): 
    global signed_in_as
    form = LoginForm(username=username)
    if form.validate_on_submit():
        logging.info("Validated signup form")
        if user_exists(form.username.data.upper()):
            flash("The username chosen is taken. If this is you, please sign in.")
            return render_template("signup.html",
                                   title="Sign Up",
                                   form=form,submit_message="Sign Up")

        hashed_password = hash_data(form.password.data)
        user = User(username=form.username.data.upper(),password=hashed_password)
        db.session.add(user)
        db.session.commit()
        signed_in_as = form.username.data
        logging.info("Redirected to base")
        return redirect("/")
    return render_template("signup.html",
                           title="Sign Up",
                           form=form,submit_message="Sign Up")

@app.route("/discover")
def discover():
    if not signed_in_as:
        return redirect("/")         
    return render_template("discover.html",
                           title="Discover",
                    username=signed_in_as,
                    all_articles=Article.query.order_by(Article.likes.desc()).all())

@app.route("/portfolio")
def portfolio():
    if not signed_in_as:
        return redirect("/")         
    user_id = get_by_id("user",signed_in_as)
    user_articles = Article.query.filter_by(author_id=user_id).all()
    return render_template("portfolio.html",
                           title="Portfolio",
                           all_articles=user_articles)

@app.route("/create", methods=["GET","POST"])
def create():
    if not signed_in_as:
        return redirect("/")
    form = ArticleForm()
    if form.validate_on_submit():
        logging.info("Validated Article Form")
        status = validate_article(form.title.data,form.content.data)
        logging.info(status)
        if status != True:
            flash(status)
            return render_template("create.html",
                           title="Write Article",
                           form=ArticleForm(title=form.title.data,content=form.content.data,category=form.category.data))
        category_id = get_by_id("category",form.category.data)
        author_id = get_by_id("user",signed_in_as)
        article = Article(title=form.title.data,content=form.content.data,category_id=category_id,author_id=author_id)
        db.session.add(article)
        db.session.commit()
        return redirect("/portfolio")

    return render_template("create.html",
                           title="Write Article",
                           form=form)

@app.route("/like",methods=["POST"])
def like():
    data = json.loads(request.data)
    article_id = int(data.get("article_id"))
    article = Article.query.get(article_id)
    article.likes += 1
    db.session.commit()
    return json.dumps({"satus":"OK","likes":article.likes})


@app.route("/quit")
def quit():
    global signed_in_as
    signed_in_as=False
    return redirect("/")
