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
                myuser.email_address = user.email()
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

    def isEmpty(self, Check_Value):
        if Check_Value == '':
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
                myuser.email_address = user.email()
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

        if self.isEmpty(Atti_Name) != True and self.isEmpty(Atti_Manufacture) != True and self.isEmpty(Atti_Year_From) != True and self.isEmpty(Atti_Year_To) != True:
            Atti_Year_From = int(Atti_Year_From)
            Atti_Year_To = int(Atti_Year_To)
            Data_Query1 = Raw_Data.filter(atti.atti_name == Atti_Name and atti.atti_manufacture == Atti_Manufacture and atti.atti_year >= Atti_Year_From)
            Data_Query2 = Raw_Data.filter(atti.atti_name == Atti_Name and atti.atti_manufacture == Atti_Manufacture and atti.atti_year <= Atti_Year_To)
            Data_Query1 = Data_Query1.fetch(keys_only=True)
            Data_Query2 = Data_Query2.fetch(keys_only=True)
            Data = ndb.get_multi(set(Data_Query1).intersection(Data_Query2))

        elif self.isEmpty(Atti_Name) != True and self.isEmpty(Atti_Manufacture) != True:
            Data_Query = Raw_Data.filter(atti.atti_name == Atti_Name and atti.atti_manufacture == Atti_Manufacture)
            Data = Data_Query.fetch()

        elif (self.isEmpty(Atti_Name) != True) and (self.isEmpty(Atti_Year_From) != True) and (self.isEmpty(Atti_Year_To) != True):
            Atti_Year_From = int(Atti_Year_From)
            Atti_Year_To = int(Atti_Year_To)
            Data_Query1 = Raw_Data.filter(atti.atti_name == Atti_Name)
            Data_Query2 = Raw_Data.filter(atti.atti_year <= Atti_Year_To)
            Data_Query3 = Raw_Data.filter(atti.atti_year >= Atti_Year_From)
            Data_Query1 = Data_Query1.fetch(keys_only=True)
            Data_Query2 = Data_Query2.fetch(keys_only=True)
            Data_Query3 = Data_Query3.fetch(keys_only=True)
            Data = ndb.get_multi(set(Data_Query1).intersection(Data_Query2, Data_Query3))

        elif (self.isEmpty(Atti_Manufacture) != True) and (self.isEmpty(Atti_Year_From) != True) and (self.isEmpty(Atti_Year_To) != True):
            Atti_Year_From = int(Atti_Year_From)
            Atti_Year_To = int(Atti_Year_To)
            Data_Query1 = Raw_Data.filter(atti.atti_manufacture == Atti_Manufacture)
            Data_Query2 = Raw_Data.filter(atti.atti_year >= Atti_Year_From)
            Data_Query3 = Raw_Data.filter(atti.atti_year <= Atti_Year_To)
            Data_Query1 = Data_Query1.fetch(keys_only=True)
            Data_Query2 = Data_Query2.fetch(keys_only=True)
            Data_Query3 = Data_Query3.fetch(keys_only=True)
            Data = ndb.get_multi(set(Data_Query1).intersection(Data_Query2, Data_Query3))

        elif self.isEmpty(Atti_Name) != True:
            Data_Query = Raw_Data.filter(atti.atti_name == Atti_Name)
            Data = Data_Query.fetch()

        elif self.isEmpty(Atti_Manufacture) != True:
            Data_Query = Raw_Data.filter(atti.atti_manufacture == Atti_Manufacture)
            Data = Data_Query.fetch()

        elif self.isEmpty(Atti_Year_From) != True and self.isEmpty(Atti_Year_To) != True:
            Atti_Year_From = int(Atti_Year_From)
            Atti_Year_To = int(Atti_Year_To)
            Data_Query1 = Raw_Data.filter(atti.atti_year >= Atti_Year_From)
            Data_Query2 = Raw_Data.filter(atti.atti_year <= Atti_Year_To)
            Data_Query1 = Data_Query1.fetch(keys_only=True)
            Data_Query2 = Data_Query2.fetch(keys_only=True)
            Data = ndb.get_multi(set(Data_Query1).intersection(Data_Query2))
        else:
            Data = ''

        if self.isEmpty(Atti_battery_size_from) != True and self.isEmpty(Atti_battery_size_to) != True:
            Atti_battery_size_from = int(Atti_battery_size_from)
            Atti_battery_size_to = int(Atti_battery_size_to)
            Data_Query1 = Raw_Data.filter(atti.atti_battery_size >= int(Atti_battery_size_from))
            Data_Query2 = Raw_Data.filter(atti.atti_battery_size <= int(Atti_battery_size_to))
            Data_Query1 = Data_Query1.fetch(keys_only=True)
            Data_Query2 = Data_Query2.fetch(keys_only=True)
            Data = ndb.get_multi(set(Data_Query1).intersection(Data_Query2))

        if self.isEmpty(Atti_WLTP_range_from) != True and self.isEmpty(Atti_WLTP_range_to) != True:
            Atti_WLTP_range_from = int(Atti_WLTP_range_from)
            Atti_WLTP_range_to = int(Atti_WLTP_range_to)
            Data_Query1 = Raw_Data.filter(atti.atti_WLTP_range >= int(Atti_WLTP_range_from))
            Data_Query2 = Raw_Data.filter(atti.atti_WLTP_range <= int(Atti_WLTP_range_to))
            Data_Query1 = Data_Query1.fetch(keys_only=True)
            Data_Query2 = Data_Query2.fetch(keys_only=True)
            Data = ndb.get_multi(set(Data_Query1).intersection(Data_Query2))

        if self.isEmpty(Atti_cost_from) != True and self.isEmpty(Atti_cost_to) != True:
            Atti_cost_from = int(Atti_cost_from)
            Atti_cost_to = int(Atti_cost_to)
            Data_Query1 = Raw_Data.filter(atti.atti_cost >= int(Atti_cost_from))
            Data_Query2 = Raw_Data.filter(atti.atti_cost <= int(Atti_cost_to))
            Data_Query1 = Data_Query1.fetch(keys_only=True)
            Data_Query2 = Data_Query2.fetch(keys_only=True)
            Data = ndb.get_multi(set(Data_Query1).intersection(Data_Query2))

        if self.isEmpty(Atti_power_from) != True and self.isEmpty(Atti_power_to) != True:
            Atti_power_from = int(Atti_power_from)
            Atti_power_to = int(Atti_power_to)
            Data_Query1 = Raw_Data.filter(atti.atti_power >= int(Atti_power_from))
            Data_Query2 = Raw_Data.filter(atti.atti_power <= int(Atti_power_to))
            Data_Query1 = Data_Query1.fetch(keys_only=True)
            Data_Query2 = Data_Query2.fetch(keys_only=True)
            Data = ndb.get_multi(set(Data_Query1).intersection(Data_Query2))

        if len(Data) != 0:
            Final_Data = Data
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
