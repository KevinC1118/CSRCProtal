import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class MainPage(webapp.RequestHandler):
    def get(self):
        
        user = users.get_current_user()
        
        template_values = {}
        
        if user:
            template_values['userName'] = user.nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')
        
        if users.is_current_user_admin():                        
            path = os.path.join(os.path.dirname(__file__), '../templates/admin/index.html')
            self.response.out.write(template.render(path, template_values))
        else:        
            self.redirect("/employee/")
    
application = webapp.WSGIApplication(
                                     [('/admin', MainPage)],
                                     debug=False)

def main():
    run_wsgi_app(application)    

if __name__ == "__main__":
    main()
    