from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .models import Event, User, Booking
from .forms import EventForm, CommentForm, BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user


bookingbp = Blueprint('booking', __name__, url_prefix='/bookings')

@bookingbp.route('/ebks')
def evbooking():
    bookings = db.session.scalars(db.select(Booking)).all()    
    return render_template('userbooking.html', bookings=bookings)
