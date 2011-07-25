#!/bin/python
# -*- coding: utf-8 -*-
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model.Publish import Publish
from google.appengine.ext import db
import sys
type = sys.getfilesystemencoding()
import time, datetime
from google.appengine.api import users


class MainPage(webapp.RequestHandler):
    def get(self):

        publish_query = Publish.all().order('-publish_date')
        publishs = publish_query.fetch(10)

        template_values = {'publishs': publishs,
                           'userName': users.get_current_user().nickname().split('@')[0],
                           'logout': users.create_logout_url('/')}
                  
        path = os.path.join(os.path.dirname(__file__), '../../templates/admin/publish.html')
        self.response.out.write(template.render(path, template_values))

class Insert_Publish(webapp.RequestHandler):
    def post(self):
                
        max = 0
        publish_query = Publish.all().order('-id')
        publishs = publish_query.fetch(5)
        for publish in publishs :
            if max < publish.id:
                max = publish.id
            
        bulletin = Publish()            
        bulletin.title = self.request.get('title')
        bulletin.content = self.request.get('content')
        bulletin.type = self.request.get('type')
        bulletin.id = max+1
#        bulletin.publish_date = datetime.datetime.now(TaiwanTimeZone())
        bulletin.put()
        self.redirect('/admin/publish')

class Delete_Publish(webapp.RequestHandler):
    def post(self, delete_id):
        
        q = db.GqlQuery("SELECT * FROM Publish WHERE id = :1", int(delete_id))
        results = q.fetch(10)
        for result in results:
            result.delete()
            
        self.redirect('/admin/publish')
        
class Edit_Publish(webapp.RequestHandler):
    def post(self, update_id):
               
        q = db.GqlQuery("SELECT * FROM Publish WHERE id = :1", int(update_id))
        results = q.fetch(10)
    
        template_values = {'publishs': results,
                            'userName': users.get_current_user().nickname().split('@')[0],
                            'logout': users.create_logout_url('/')}
            
        path = os.path.join(os.path.dirname(__file__), '../../templates/admin/updatepublish.html')
        self.response.out.write(template.render(path, template_values))
        
class Update_Publish(webapp.RequestHandler):
    def post(self, update_id):
        
        q = db.GqlQuery("SELECT * FROM Publish WHERE id = :1", int(update_id))
        results = q.fetch(10)
        for data in results:
            data.title = self.request.get('new_title')
            data.content = self.request.get('new_content')
            data.type = self.request.get('new_type')

            time_format = "%Y-%m-%d"                             
            data.publish_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(self.request.get('new_date'), time_format)))
            #data.publish_date = self.request.get('new_date')
        db.put(results)
        self.redirect('/admin/publish')

class Publish_Detail(webapp.RequestHandler):
    def get(self, looking_id):

        q = db.GqlQuery("SELECT * FROM Publish WHERE id = :1 ", int(looking_id))        
        results = q.fetch(10)
                       
        template_values = {'publishs': results,
                           'userName': users.get_current_user().nickname().split('@')[0],
                           'logout': users.create_logout_url('/')}
    
        path = os.path.join(os.path.dirname(__file__), '../../templates/admin/publish_detail.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/admin/publish', MainPage),                                      
                                      ('/publish/insert_publish', Insert_Publish),
                                      ('/publish/delete_publish/(.*)', Delete_Publish),
                                      ('/publish/edit_publish/(.*)', Edit_Publish),
                                      ('/publish/update_publish/(.*)', Update_Publish),                      
                                      ('/publish/publish_detail/(.*)',Publish_Detail)], debug=False)        
        
def main():
    run_wsgi_app(application)
    
if __name__ == "__main__":
    main()