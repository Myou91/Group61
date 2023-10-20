from . import db
from datetime import datetime, date, time
from flask_login import UserMixin



class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    userId = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailAddress = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)
    mobilePhoneNumber = db.Column(db.Integer,unique=True, nullable=False)
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
        # string print method
    def __repr__(self):
        
        
        return f"Name: {self.name}"




class Events(db.Model):
    __tablename__ = 'events'
    eventId = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(50))
    eventDate = db.Column(db.Date)
    eventTime = db.Column(db.Time)
    location = db.Column(db.String(50))
    description = db.Column(db.String(400))
    image = db.Column(db.String(200))
    numberOfTickets = db.Column(db.Integer)
    status = db.Column(db.String(200))
    owner = db.Column(db.String(40))
    # add the foreign keys
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))
    # relation to call events.comments and comment.created_by
    comments = db.relationship('Comment', backref='events')
    # relation to call events.user and event.created_by
    user = db.relationship('User', backref='events')

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.String(1024))
    address = db.Column(db.String(300))
    date = db.Column(db.Date, nullable=False)
    #Proj Req 1.  event by category 
    category = db.Column(db.Integer, default=0)
    start_time = db.Column(db.Time, nullable=False)
    finish_time = db.Column(db.Time, nullable=False)
    price = db.Column(db.Numeric(5,2), nullable=False)
    ticket_max = db.Column(db.Integer)
    ticket_remain = db.Column(db.Integer)
    #boolean Event cancelled
    cancel = db.Column(db.Boolean, default=False, nullable=False)
    image = db.Column(db.String(400))
    comments = db.relationship('Comment', backref='event')
    
    

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"
    
class Comment(db.Model):
    __tablename__ = 'comments'
    commentId = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign keys
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))
    eventId = db.Column(db.Integer, db.ForeignKey('events.eventId'))

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"
    
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    ticket = db.Column(db.Integer)
    paymentdate = db.Column(db.DateTime, default=datetime.now())
    amount = db.Column(db.Numeric(10,2))
    #No order confirm because when giving out bookingID is already confirm
    reference = db.Column(db.String(6))
    consume = db.Column(db.Boolean, default=False, nullable=False)
    refund = db.Column(db.Boolean, default=False, nullable=False)
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


class Bookings(db.Model):
    __tablename__ = 'bookings'
    bookingId = db.Column(db.Integer, primary_key=True)
    numberOfTicketsBought = db.Column(db.Integer)
    orderConfirmation = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign keys
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))
    eventId = db.Column(db.Integer, db.ForeignKey('events.eventId'))

    user = db.relationship('User', backref='bookings')

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"    
