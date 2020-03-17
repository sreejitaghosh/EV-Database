from google.appengine.ext import ndb

class atti(ndb.Model) :
    atti_name = ndb.StringProperty()
    atti_manufacture = ndb.StringProperty()
    atti_year = ndb.IntegerProperty()
    atti_battery_size = ndb.IntegerProperty()
    atti_WLTP_range = ndb.IntegerProperty()
    atti_cost = ndb.IntegerProperty()
    atti_power = ndb.IntegerProperty()
