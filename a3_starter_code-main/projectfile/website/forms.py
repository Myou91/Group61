from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, BooleanField 
from wtforms.fields import SelectField, TimeField, DateField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed, FileSize

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

#Create new event
class EventForm(FlaskForm):
  name = StringField('Event Name', validators=[InputRequired(), Length(max=256)])
  description = TextAreaField('Description', validators=[InputRequired(), Length(max=1024)])
  address = TextAreaField('Event Address', validators=[InputRequired(), Length(max=300)])
  date = DateField ('Event Date', format='%d%m%Y', validators=[DataRequired()]) 
  group = SelectField ('Age Group', choices=[('0', '0-3'),('1', '4-8')('2','9-16')], validators=[DataRequired()])
  start_time = TimeField ('Start Time', format='%H:%M', validators=[DataRequired()])
  finish_time = TimeField ('Finish Time', format='%H:%M', validators=[DataRequired()])
  price = DecimalField ('Price $', places=2, validators=[DataRequired()])
  ticket_max = IntegerField ('Event Ticket Available', validators=[DataRequired()])
  cancel = BooleanField('Event Cancel')

  image = FileField('Destination Image', validators=[
    FileRequired(message = 'Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG'), 
    FileSize(max_size=2097152, message='File size 2MB max')])
  submit = SubmitField("Create Event")

#User comment for event
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', validators=[InputRequired()])
  submit = SubmitField("Submit Comment")

#Event Booking Form
class BookingForm(FlaskForm):
  ticket = IntegerField ('Event Ticket Purchase (6 tickets max)', validators=[DataRequired(), NumberRange(max=6)])
  submit = SubmitField('Purchase Ticket')
