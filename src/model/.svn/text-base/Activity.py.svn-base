'''
Created on 2011/3/6
  
@author: Leo
'''
from google.appengine.ext import db
class Activitydb(db.Model):
    activity_id = db.IntegerProperty()  #activity id(Serial number in future)
    activity_name = db.StringProperty() #activity name
    content = db.StringProperty(multiline=True) #Activity described
    sign_start = db.DateTimeProperty() #sign up start time
    sign_end = db.DateTimeProperty()   #sign up deadline
    activity_start = db.DateTimeProperty() #activity start time
    activity_end = db.DateTimeProperty()   #activity deadline
    limit_num = db.IntegerProperty()    #how many people can sign up
    site = db.StringProperty()    #activity in where

class Peopledb(db.Model):
    #author = db.UserProperty()
    #content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    name = db.StringProperty()
    stu_id = db.IntegerProperty()
    mail = db.StringProperty()
    phone = db.StringProperty()
    activity_id = db.IntegerProperty()


class Forumdb(db.Model):
    activity_id = db.IntegerProperty()
    forum_id = db.IntegerProperty()
    content = db.StringProperty(multiline=True)
    time = db.DateTimeProperty() #post time
    sequence = db.IntegerProperty()
    editor = db.StringProperty()
