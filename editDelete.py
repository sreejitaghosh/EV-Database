import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import MyUser
from attribute import atti

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class editDelete(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url_string = ''
        url = ''
        add = ''
        search = ''
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.user_id())
                myuser.email_address = user.email()
                myuser.put()

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'


        edit_atti_name = self.request.GET.get('atti_name')
        edit_atti_manufacture = self.request.GET.get('atti_manufacture')
        edit_atti_year = self.request.GET.get('atti_year')
        atti_Key = edit_atti_name+''+edit_atti_manufacture+''+edit_atti_year
        details = ndb.Key('atti', atti_Key)
        details = details.get()

        template_values = {
                'url' : url,
                'url_string' : url_string,
                'user' : user,
                'details' : details
        }

        template = JINJA_ENVIRONMENT.get_template('editDelete.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        url_string = ''
        url = ''
        add = ''
        search = ''
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.user_id())
                myuser.email_address = user.email()
                myuser.put()

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        if user:
            edit_atti_name = self.request.GET.get('atti_name')
            edit_atti_manufacture = self.request.GET.get('atti_manufacture')
            edit_atti_year = self.request.GET.get('atti_year')
            atti_Key = edit_atti_name+''+edit_atti_manufacture+''+edit_atti_year

            if self.request.get('Button') == 'Delete':
                ndb.Key('atti', atti_Key).delete()
                self.redirect('/')
                add_b=''
            else:
                ndb.Key('atti', atti_Key).delete()
                add_b = atti(id=self.request.get('atti_name_new')+""+self.request.get('atti_manufacture_new')+""+self.request.get('atti_year_new'))
                add_b.atti_name = self.request.get('atti_name_new')
                add_b.atti_manufacture = self.request.get('atti_manufacture_new')
                add_b.atti_year = int(self.request.get('atti_year_new'))
                add_b.atti_battery_size = int(self.request.get('atti_battery_size_new'))
                add_b.atti_WLTP_range = int(self.request.get('atti_WLTP_range_new'))
                add_b.atti_cost = int(self.request.get('atti_cost_new'))
                add_b.atti_power = int(self.request.get('atti_power_new'))
                add_b.put()
        else:
            add_b=''
            self.redirect('/')

        template_values = {
                'url' : url,
                'url_string' : url_string,
                'user' : user,
                'details' : add_b
        }

        template = JINJA_ENVIRONMENT.get_template('editDelete.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/editDelete', editDelete),
], debug=True)
