import os

WTF_CSRT_ENABLED = True
SECRET_KEY = "usmct-Hausm-Lopps"

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir, "app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = True
