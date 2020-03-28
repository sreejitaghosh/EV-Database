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

class Element(webapp2.RequestHandler):
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
                myuser.put()

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
                'url' : url,
                'url_string' : url_string,
                'user' : user
        }

        template = JINJA_ENVIRONMENT.get_template('searchElement.html')
        self.response.write(template.render(template_values))

    def isEmptyOrNullorZero(self, Check_Value):
        if Check_Value == '' or Check_Value == None or Check_Value == 0:
            return True
        else:
            return False

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
                myuser.put()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        Atti_Name = self.request.get('atti_name')
        Atti_Manufacture = self.request.get('atti_manufacture')
        Atti_Year_From = self.request.get('atti_year_from')
        Atti_Year_To = self.request.get('atti_year_to')
        Atti_battery_size_from = self.request.get('atti_battery_size_from')
        Atti_battery_size_to = self.request.get('atti_battery_size_to')
        Atti_WLTP_range_from = self.request.get('atti_WLTP_range_from')
        Atti_WLTP_range_to = self.request.get('atti_WLTP_range_to')
        Atti_cost_from = self.request.get('atti_cost_from')
        Atti_cost_to = self.request.get('atti_cost_to')
        Atti_power_from = self.request.get('atti_power_from')
        Atti_power_to = self.request.get('atti_power_to')

        Raw_Data = atti.query()
        Data = ''
        if self.isEmptyOrNullorZero(Atti_Name) != True:
            Data = Raw_Data.filter(atti.atti_name == Atti_Name)

        if self.isEmptyOrNullorZero(Atti_Manufacture) != True:
            Data = Raw_Data.filter(atti.atti_manufacture == Atti_Manufacture)

        if self.isEmptyOrNullorZero(Atti_Year_From) != True:
            Data = Raw_Data.filter(atti.atti_year >= int(Atti_Year_From))
        if self.isEmptyOrNullorZero(Atti_Year_To) != True:
            Data = Raw_Data.filter(atti.atti_year <= int(Atti_Year_To))

        if self.isEmptyOrNullorZero(Atti_battery_size_from) != True:
            Data = Raw_Data.filter(atti.atti_battery_size >= int(Atti_battery_size_from))
        if self.isEmptyOrNullorZero(Atti_battery_size_to) != True:
            Data = Raw_Data.filter(atti.atti_battery_size <= int(Atti_battery_size_to))

        if self.isEmptyOrNullorZero(Atti_WLTP_range_from) != True:
            Data = Raw_Data.filter(atti.atti_WLTP_range >= int(Atti_WLTP_range_from))
        if self.isEmptyOrNullorZero(Atti_WLTP_range_to) != True:
            Data = Raw_Data.filter(atti.atti_WLTP_range <= int(Atti_WLTP_range_to))

        if self.isEmptyOrNullorZero(Atti_cost_from) != True:
            Data = Raw_Data.filter(atti.atti_cost >= int(Atti_cost_from))
        if self.isEmptyOrNullorZero(Atti_cost_to) != True:
            Data = Raw_Data.filter(atti.atti_cost <= int(Atti_cost_to))

        if self.isEmptyOrNullorZero(Atti_power_from) != True:
            Data = Raw_Data.filter(atti.atti_power >= int(Atti_power_from))
        if self.isEmptyOrNullorZero(Atti_power_to) != True:
            Data = Raw_Data.filter(atti.atti_power <= int(Atti_power_to))

        if len(Data) != 0:
            Final_Data = Data.fetch()
        else:
            Final_Data = Raw_Data.fetch()

        template_values = {
                'url' : url,
                'url_string' : url_string,
                'user' : user,
                'Search_Data' : Final_Data
        }

        template = JINJA_ENVIRONMENT.get_template('searchElement.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/searchElement', Element),
], debug=True)
