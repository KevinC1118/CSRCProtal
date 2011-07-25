# -*- coding: utf-8 -*-
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    def get(self):
            template_values = {'userName': users.get_current_user().nickname().split('@')[0],
                               'logout': users.create_logout_url('/')}

            path = os.path.join(os.path.dirname(__file__),'../../templates/activitymain.html')
            self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/ActivityMain', MainPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()