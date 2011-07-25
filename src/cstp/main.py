'''
Created on 2011/3/18

@author: korprulu
'''

import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import re
from google.appengine.api import users

class Introduction(webapp.RequestHandler):
    def get(self):
        
        template_values = {}
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')
                  
        path = os.path.join(os.path.dirname(__file__), '../templates/cstp/introduction.html')
        self.response.out.write(template.render(path, template_values))

class Features(webapp.RequestHandler):
    def get(self):
        
        template_values = {}
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')
                  
        path = os.path.join(os.path.dirname(__file__), '../templates/cstp/features.html')
        self.response.out.write(template.render(path, template_values))    

class Courses(webapp.RequestHandler):
    def get(self):
        
        template_values = {}
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')
                  
        path = os.path.join(os.path.dirname(__file__), '../templates/cstp/courses.html')
        self.response.out.write(template.render(path, template_values))  
        
class ApplyProcess(webapp.RequestHandler):
    def get(self):
        
        template_values = {}
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')     
                         
        path = os.path.join(os.path.dirname(__file__), '../templates/cstp/applyprocess.html')
        self.response.out.write(template.render(path, template_values))                      

class Admission(webapp.RequestHandler):
    
    def get(self):
        template_values = {}
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')
            
        path = os.path.join(os.path.dirname(__file__), '../templates/cstp/admission.html')
        self.response.out.write(template.render(path, template_values))

class Download(webapp.RequestHandler):
    
    def get(self):
        template_values = {}
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')
        
        path = os.path.join(os.path.dirname(__file__), '../templates/cstp/download.html')
        self.response.out.write(template.render(path, template_values))

class CSTP(webapp.RequestHandler):
    def get(self):
        pattern = '.*(symbian|smartphone|midp|wap|phone|pda|mobile|mini|palm|netfront|android|bada).*'
        prog = re.compile(pattern, re.IGNORECASE)
        match = prog.search(str(self.request))
        if match:
            #self.response.out.write("You are in mobile")
            self.redirect("/mobile/cstp")
        else:
            #self.response.out.write("You are in PC")
            self.redirect("/cstp/introduction")
#self.response.out.write(self.request)

application = webapp.WSGIApplication([('/cstp', CSTP),
                                      ('/cstp/introduction', Introduction),
                                      ('/cstp/features', Features),
                                      ('/cstp/courses', Courses),
                                      ('/cstp/applyprocess', ApplyProcess),
                                      ('/cstp/admission', Admission),
                                      ('/cstp/download', Download),
                                      ('/cstp/.*', CSTP)],
                                      debug=False)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()