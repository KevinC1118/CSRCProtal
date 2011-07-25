# -*- coding: utf-8 -*-
import os

from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from model import Activity, Mail

class MainPage(webapp.RequestHandler):
    def get(self):
        getallactivity = db.GqlQuery("SELECT * FROM Activitydb")
        template_values = {
                           'allactivity':getallactivity,
                           'userName': users.get_current_user().nickname().split('@')[0],
                           'logout': users.create_logout_url('/')
                           }
        path = os.path.join(os.path.dirname(__file__),'../../templates/activitymodifylist.html')
        self.response.out.write(template.render(path, template_values))
class SearchActivity(webapp.RequestHandler):
    def post(self):
        temp = int(self.request.get('search_activity_id'))
        searchactivity = db.GqlQuery("SELECT * FROM Activitydb WHERE activity_id = :1",temp)  #get who sign up the activity.
        template_values = {
                           'search_id': temp,
                           'searchactivity':searchactivity,
                           'search_tag':1
                           }
        path = os.path.join(os.path.dirname(__file__),'../../templates/activitymodifylist.html')
        self.response.out.write(template.render(path, template_values))
        
application = webapp.WSGIApplication([('/ActivityModify/Main', MainPage),('/ActivityModify/GoSearch',SearchActivity)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
