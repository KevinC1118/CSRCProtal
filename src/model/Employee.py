from google.appengine.ext import db

class Employee(db.Model):
    id = db.IntegerProperty()
    mail = db.UserProperty()
    name = db.StringProperty()
    hourly_pay = db.IntegerProperty()
    
    
