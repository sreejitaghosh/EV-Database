import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import MyUser
from add import add
from search import search
from searchElement import Element
from editDelete import editDelete
from compare import compare
from compareElements import compareElements

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url_string = ''
        url = ''
        add = ''
        search = ''
        compare = ''


        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            myuser_details = ndb.Key('MyUser', user.user_id())
            myuser = myuser_details.get()
            if myuser == None:
                myuser = MyUser(id=user.user_id())
                myuser.email_address = user.email()
                welcome = 'Welcome to the application'
                myuser.put()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user
        }

        template = JINJA_ENVIRONMENT.get_template('ev.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add', add),
    ('/search', search),
    ('/searchElement', Element),
    ('/editDelete', editDelete),
    ('/compare', compare),
    ('/compareElements', compareElements)
], debug=True)
