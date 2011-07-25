from google.appengine.ext import db

class WorkingHours(db.Model):
    id = db.IntegerProperty()
    worker = db.UserProperty(auto_current_user=True)
    working_date = db.DateProperty()
    working_bhour = db.StringProperty() 
    working_ehour = db.StringProperty() 
    subtotal = db.FloatProperty()
    pay = db.IntegerProperty()
    working_area = db.StringProperty()
    working_content = db.StringProperty(multiline=True)  
    
    
