from core import db
from datetime import datetime
import uuid

# board db model
class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), index=True)
    
    name = db.Column(db.String(50))

    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    zip = db.Column(db.String(5))
    street = db.Column(db.String(50))
    housenumber = db.Column(db.String(10))
    building = db.Column(db.String(20))
    
    gpslong = db.Column(db.Float)
    gpslat = db.Column(db.Float)
    gpsele = db.Column(db.Float)
    gpstime = db.Column(db.DateTime)

    active = db.Column(db.Boolean)
    qrcode = db.Column(db.String(100))
    
    create_date = db.Column(db.DateTime)   
    
    def __init__(self, name, state, city, zip, street, housenumber, building, gpslong=None, gpslat=None, gpsele=None, gpstime=None, active=False, qrcode=None):
        
        self.uuid = str(uuid.uuid4())

        self.name = name
         
        self.state = state
        self.city = city
        self.zip = zip
        self.street = street
        self.housenumber = housenumber
        self.building = building

        self.gpslong = gpslong
        self.gpslat = gpslat
        self.gpsele = gpsele
        #self.gpstime = gpstime

        self.active = active
        self.qrcode = qrcode

        self.create_date = datetime.utcnow()

    def __repr__(self):
        return '<Board %r>' % self.name


# Create Database from scratch
def reset_database():
    db.drop_all()
    db.create_all()