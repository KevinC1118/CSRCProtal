'''
Created on 2011/3/17

@author: korprulu
'''
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Introduction(webapp.RequestHandler):
    
    def get(self):    
        template_values = {'': ''}          
        path = os.path.join(os.path.dirname(__file__), '../../templates/mobile/cstp/introduction.html')
        self.response.out.write(template.render(path, template_values))

class Features(webapp.RequestHandler):
    
    def get(self):
        template_values = {'': ''}          
        path = os.path.join(os.path.dirname(__file__), '../../templates/mobile/cstp/features.html')
        self.response.out.write(template.render(path, template_values))    

class Courses(webapp.RequestHandler):
    
    def get(self):
        template_values = {'': ''}          
        path = os.path.join(os.path.dirname(__file__), '../../templates/mobile/cstp/courses.html')
        self.response.out.write(template.render(path, template_values))  
        
class Rules(webapp.RequestHandler):
    
    def get(self):
        template_values = {'': ''}          
        path = os.path.join(os.path.dirname(__file__), '../../templates/mobile/cstp/rules.html')
        self.response.out.write(template.render(path, template_values))  

class Admission(webapp.RequestHandler):
    
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), '../../templates/mobile/cstp/admission.html')
        self.response.out.write(template.render(path, template_values))

class CSTP(webapp.RequestHandler):
    
    def get(self):
        self.redirect("/mobile/cstp/introduction")

application = webapp.WSGIApplication([('/mobile/cstp', CSTP),
                                      ('/mobile/cstp/introduction', Introduction),
                                      ('/mobile/cstp/introduction/.*', Introduction),
                                      ('/mobile/cstp/features', Features),
                                      ('/mobile/cstp/features/.*', Features),
                                      ('/mobile/cstp/courses', Courses),
                                      ('/mobile/cstp/courses/.*', Courses),
                                      ('/mobile/cstp/rules', Rules),
                                      ('/mobile/cstp/rules/.*', Rules),
                                      ('/mobile/cstp/admission', Admission),
                                      ('/mobile/cstp/admission/.*', Admission),
                                      ('/mobile/cstp/.*', CSTP)],
                                      debug=False)

def main():
    run_wsgi_app(application) 

if __name__ == '__main__':
    main()