from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()    
    return render_template('index.html', events=events)

@mainbp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(db.select(Event).where(Event.description.like(query)))
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))


@mainbp.route('/age-group')
def age_group(category):
    age_groups = {
        1: 'Age group 0-3',
        2: 'Age group 4-8',
        3: 'Age group 9-16'
    }

    if category in age_groups:
        return age_groups[category]
    else:
        return 'Invalid index'
