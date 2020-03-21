import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import MyUser
from attribute import atti

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname("E:\\GCD\\Sem 2\\Cloud Computing\\EV DATABASE\\")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class add(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url_string = ''
        url = ''
        add = ''
        search = ''
        status = 0

        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.user_id())
                myuser.put()

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
                'url' : url,
                'url_string' : url_string,
                'myuser' : myuser,
                'note' : status,
        }

        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        url_string = ''
        url = ''
        add = ''
        search = ''
        status = 0

        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.user_id())
                myuser.put()

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        AttributeChecking = atti.query(
        atti.atti_name == self.request.get('atti_name'),
        atti.atti_manufacture == self.request.get('atti_manufacture'),
        atti.atti_year == int(self.request.get('atti_year'))
        ).fetch()

        if len(AttributeChecking) == 0:
            add_b = atti(id=self.request.get('atti_name')+""+self.request.get('atti_manufacture')+""+self.request.get('atti_year'))
            add_b.atti_name = self.request.get('atti_name')
            add_b.atti_manufacture = self.request.get('atti_manufacture')
            add_b.atti_year = int(self.request.get('atti_year'))
            add_b.atti_battery_size = int(self.request.get('atti_battery_size'))
            add_b.atti_WLTP_range = int(self.request.get('atti_WLTP_range'))
            add_b.atti_cost = int(self.request.get('atti_cost'))
            add_b.atti_power = int(self.request.get('atti_power'))
            add_b.put()
            status = 1
            print 'add'
            print status

        else:
            status = 2
            print 'Exists'
            print status

        template_values = {
                'url' : url,
                'url_string' : url_string,
                'myuser' : myuser,
                'note' : status,
        }

        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/add', add),
], debug=True)
