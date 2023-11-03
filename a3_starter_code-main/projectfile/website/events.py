from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .models import Event, Comment, Booking
from .forms import EventForm, CommentForm, BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user
import random, string, secrets

eventbp = Blueprint('event', __name__, url_prefix='/events')

@eventbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    cform = CommentForm()
    eform = BookingForm()    
    return render_template('events/show.html', event=event, cform=cform, form=eform)

@eventbp.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()
        flash('Event updated successfully!', 'success')
    return redirect(url_for('event.show', id=id))




@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(name=form.name.data,description=form.description.data, address=form.address.data,
    date=form.date.data, category=form.category.data, start_time=form.start_time.data,
    finish_time=form.finish_time.data, price=form.price.data, ticket_max=form.ticket_max.data,
    ticket_remain = form.ticket_max.data, cancel=form.cancel.data, image=db_file_path)

    print(form.date.data)
     # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created a new event', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('event.create'))
  return render_template('events/create.html', form=form)

def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

#Handle Comment field in Event detail page
@eventbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    #get the event object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data, event=event,
                        user=current_user) 
      #here the back-referencing works - comment.event is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      #flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to event.show
    return redirect(url_for('event.show', id=id))

#Random string generator
def gen_random_string():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

#Handle Event booking field in Event detail page
@eventbp.route('/<id>/booking', methods=['GET', 'POST'])  
@login_required
def booking(id):  
    form = BookingForm()  
    #get the event object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      #System rules no user book more than 6 ticket
      if  form.ticket.data > 6 and form.ticket.data < 1:
        flash('Ticket request is more than 6', 'error')
      else:
         #Handle ticket remain not enough to user request
         if form.ticket.data > event.ticket_remain:
           flash('Only '+str(event.ticket_remain)+' ticket(s) available! Please order less ticket(s)', 'warning')
         else:
            #Create booking for user and update event.ticket_remain
            #read the ticket request from the form
            event.ticket_remain -= form.ticket.data
            bprice = event.price * form.ticket.data
            print(event.ticket_remain)
            print(bprice, id)
            print(current_user.id)
            print(gen_random_string())
            #Call function to update event.ticket_remain after ticket sold
            update_event_ticketsold(id, event.ticket_remain)
            booking = Booking(ticket = form.ticket.data, reference = gen_random_string(), event_id=event.id,
                        user_id=current_user.id, amount = bprice) 
            print(booking)         
            #here the back-referencing works - comment.event is set
            # and the link is created
            db.session.add(booking) 
            db.session.commit() 
            #flashing a message which needs to be handled by the html
            flash('Your booking has been confirmed. Payment $'+str(bprice)+' received', 'success')  
            # print('Your comment has been added', 'success') 
          # using redirect sends a GET request to event.show
      return redirect(url_for('event.show', id=id))
    
def update_event_ticketsold(id, sold):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    event.ticket_remain = sold
    db.session.commit() 

@eventbp.route('/<id>/calculate_ticket_price', methods=['POST'])
def calculate_ticket_price(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    ticket_order = request.form['ticket']
    # Calculate total price based on ticket order
    total_price = int(ticket_order) * event.price
    return jsonify({'total_price': total_price})
