from google.appengine.ext import db


class DocAccount(db.Model):
    email = db.StringProperty(required=True)
    password = db.StringProperty(required=True)