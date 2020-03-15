from google.appengine.ext import ndb

class atti(ndb.Model) :
    atti_name = ndb.StringProperty()
    atti_manufacture = ndb.StringProperty()
    atti_year = ndb.StringProperty()
    atti_batter_size = ndb.StringProperty()
    atti_WLTP_range = ndb.StringProperty()
    atti_cost = ndb.StringProperty()
    atti_power = ndb.StringProperty()
