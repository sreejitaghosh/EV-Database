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
from attribute import atti

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class compareElements(webapp2.RequestHandler):
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

        template = JINJA_ENVIRONMENT.get_template('compareElements.html')
        self.response.write(template.render(template_values))

    def post(self):
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

        checkboxdata = {}
        checkboxdata = self.request.get_all('checkboxdata')
        ErrorMessage = 0
        Attributes_All_Data = {}
        if len(checkboxdata) < 2:
            ErrorMessage = 1
            Total_Data = []
        else:
            i = 0
            while i<len(checkboxdata):
                Attribute_Data = ndb.Key('atti',checkboxdata[i])
                Attributes_All_Data[i] = Attribute_Data.get()
                i = i+1
            i=0
            year = []
            battery = []
            wltp = []
            cost = []
            power = []

            while i<len(checkboxdata):
                year.append(Attributes_All_Data[i].atti_year)
                battery.append(Attributes_All_Data[i].atti_battery_size)
                wltp.append(Attributes_All_Data[i].atti_WLTP_range)
                cost.append(Attributes_All_Data[i].atti_cost)
                power.append(Attributes_All_Data[i].atti_power)
                i = i+1

            Total_Data = [min(year),max(year),min(battery),max(battery),min(wltp),max(wltp),min(cost),max(cost),min(power),max(power)]

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'ErrorMessage' : ErrorMessage,
            'Attributes_All_Data' : Attributes_All_Data,
            'Total_Data' : Total_Data
        }

        template = JINJA_ENVIRONMENT.get_template('compareElements.html')
        self.response.write(template.render(template_values))



app = webapp2.WSGIApplication([
    ('/compareElements', compareElements)
], debug=True)
