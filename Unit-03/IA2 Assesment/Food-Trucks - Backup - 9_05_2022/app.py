# Import Libraries
from flask import Flask, render_template, request, redirect, flash, session, url_for # Flask the main libary to run the actual website
from flask_wtf import FlaskForm # To use flask forms
import sqlite3 # To connect and run querys for the database
import requests # To request and download data from API's
import json # Required to be able to view and manage the json files and format

from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectMultipleField, SelectField, validators, ValidationError
from wtforms.validators import DataRequired, Email, Optional, InputRequired
from wtforms.fields import EmailField

# from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectMultipleField, SelectField, widgets # Wtfomrs for the websites get and post forms
# from wtforms.validators import DataRequired, Email, Optional, InputRequired # Validators for wtforms to ensure correct data in inputted into the database

from datetime import datetime, date, timedelta # For getting the current or future datetime (This isn't being used at the momment)
#from geojson import Point, Feature

# TODO
#   Split the py files
#   Encyrpt password
#   Finish search page
#   Work on data page with a data visualizer
#   Incorparte index page map with search function
#   Make the website look nice

# Assign flask app
app = Flask(__name__)

# Security Key
app.config['SECRET_KEY'] = 'MY_SECRET_KEY' # Due to this being a prototype a secret key won't be created

# Connect database
con = sqlite3.connect('system.db', check_same_thread=False) # connect to the websites database
cur = con.cursor() # Set cur to equal the database cursor

### Form models ####
class NoValSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        """per_validation is disabled"""
    # Due to an known bug for pre validation with select multiple fields in wtforms
    # this work around has been advised by developers of wtforms

class LoginForm(FlaskForm):
    # Username
    username = StringField('Username:', validators=[validators.DataRequired()])
    # Password
    password = PasswordField('Password:', validators=[validators.DataRequired()])
    # Login form with a submit button which isn't required but added for user ability
    submit = SubmitField('Log In!')

class SignUp(FlaskForm):
    # Username
    username = StringField('Username:', validators=[validators.DataRequired()])
    # Password with a confirmation password
    password = PasswordField('Password:', validators=[validators.DataRequired(), validators.EqualTo('password_confirmation', message='Passwords must match')])
    password_confirmation = PasswordField('Repeat Password', validators=[validators.DataRequired(), validators.EqualTo('password', message='Passwords must match')])
    # Email thats optional, has email validator and has a confirmation field
    email = EmailField('Email:', validators=[validators.DataRequired(), validators.Email(), validators.EqualTo('email_confirmation', message='Emails must match')])
    email_confirmation = EmailField('Repeat Email:', validators=[validators.DataRequired(), validators.Email(), validators.EqualTo('email', message='Emails must match')])
    # Sign up form with a submit button which isn't required but added for user ability
    submit = SubmitField('Create an Account!')

### Functions ###
def getData():
    # Download, convert and merge trucks json to sql
    try:
        trucks_page = requests.get("https://www.bnefoodtrucks.com.au/api/1/trucks")  # Replaces url everytime the function is called to make sure the url isnt changed
        trucks_json = json.loads(trucks_page.text)  # Convert page to readable json / dict format
        for truck in trucks_json:  # For every element in the json file
            # Do not use MURGE because of ...
            cur.execute(
                """INSERT OR REPLACE INTO trucks(truck_id, name, category, bio, avatar_src,avatar_alt,avatar_title,cover_photo_src, cover_photo_alt, cover_photo_title, website, facebook_url, instagram_handle, twitter_handle)VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (truck.get('truck_id'), truck.get('name'), truck.get('category'), truck.get('bio'),
                 str(truck['avatar']['src'] if truck['avatar'] != "" else ""), truck.get('name'),
                 truck.get('name'), str(truck['cover_photo']['src'] if truck['cover_photo'] != "" else ""), # Avater photo alt and title replaced with name of truck
                 truck.get('name'), truck.get('name'), # Cover photo alt and title replaced with name of truck
                 truck.get('website'), truck.get('facebook_url'), truck.get('instagram_handle'), truck.get(
                    'twitter_handle'),))  # use .get instead of data[''] as if the value doesnt exists it will return null. Have to convert the json for the images to string before parsing it to prevent errors in the future.
        con.commit()  # Commit changes to the table after for loop is complete.
    except IOError as e:  # If an error occurs print the error code and an error message.
        print(e)
        print("Error: Could not download or convert trucks database")

    # Download, convert and merge sites json to sql
    try:
        sites_page = requests.get("https://www.bnefoodtrucks.com.au/api/1/sites")  # Replaces url everytime the function is called to make sure the url isnt changed
        sites_json = json.loads(sites_page.text)  # Convert page to readable json / dict format
        for site in sites_json:  # For every element in the json file
            # Do not use MURGE because of ...
            cur.execute(
                """INSERT OR REPLACE INTO sites(site_id, title, description, street, suburb, state, postcode, country, latitude, longitude, spots, cost, image_src, image_alt, image_title, map_src, map_alt, map_title) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                site.get('site_id'),site.get('title'),site.get('description'),site.get('street'),site.get('suburb'),
                site.get('state'),site.get('postcode'),site.get('country'),site.get('latitude'),
                site.get('longitude'),
                site.get('spots'), site.get('cost'),str(site['image']['src'] if site['image'] != "" else ""),
                site.get('title'),site.get('title'),
                str(site['map']['src'] if site['map'] != "" else ""),(str(site.get('street')) + ", " + str(site.get('suburb')) + ", " + str(site.get('state')) + ", " + str(site.get('postcode')) + ", " + str(site.get('country'))),
                (str(site.get('street')) + ", " + str(site.get('suburb')) + ", " + str(site.get('state')) + ", " + str(site.get('postcode')) + ", " + str(site.get('country'))),)) # replaced map and image alt and title with custom values

        con.commit()  # Commit changes to the table after for loop is complete.
    except IOError as e:  # If an error occurs print the error code and an error message.
        print(e)
        print("Error: Could not download or convert sites database")

    # Download, convert and merge bookings json to sql
    try:
        bookings_page = requests.get("https://www.bnefoodtrucks.com.au/api/1/bookings")  # Replaces url everytime the function is called to make sure the url isnt changed
        bookings_json = json.loads(bookings_page.text) # Convert page to readable json / dict format
        for booking in bookings_json: # For every element in the json file
            # Do not use MURGE because of ...
            cur.execute("""INSERT OR REPLACE INTO bookings(title, truck_id, site_id, start, finish)VALUES (?,?,?,?,?)""", (booking.get('title'),booking.get('truck_id'),booking.get('site_id'),booking.get('start'),booking.get('finish'),))
        con.commit() # Commit changes to the table after for loop is complete.
    except IOError as e: # If an error occurs print the error code and an error message.
        print(e)
        print("Error: Could not download or convert bookings database")

def cleanData():
    # Will clean the database of old files to make sure the db runs smoothly
    print('nothin yet')

# getData()

def getBookings(time, time2):
    # Create geojson file

    sql_bookings = """
        SELECT *
        FROM sites s, bookings b, trucks t
        WHERE s.site_id = b.site_id
        AND b.truck_id = t.truck_id
        AND b.finish > (?)
        AND b.finish < (?);"""
    cur.execute(sql_bookings, (time,time2,))
    results_bookings = cur.fetchall()
    # print(results_bookings)

    # geo_json_list = []
    # for booking in results_bookings:
    #     # code to generate your geoJSON
    #     crood = Point((booking[9],booking[8]))
    #     point = Feature(geometry=crood, properties={"name": "test1", "amenity": "test2", "popupContent": "test3"})
    #     geo_json_list.append(point)
    # with open('static/jsons/geodata.json', 'a') as f:
    #     json.dump(geo_json_list, f, indent=4)

    return (results_bookings)

def getTrucks():
    # Create geojson file

    sql_trucks = """
        SELECT *
        FROM trucks;"""
    cur.execute(sql_trucks)
    results_trucks = cur.fetchall()

    return(results_trucks)

def loginReutrn(form):
    if form.validate_on_submit():
        # Set username and password variables
        un = form.username.data
        pw = form.password.data

        # Check users if the combination of username and password exists
        sql_user = """
                        select *
                        from users 
                        where username = ?
                        and password = ?;"""
        cur.execute(sql_user, (un, pw,))
        result_user = cur.fetchall()

        # If a user with that username and password combination exists set session values with the users data
        if len(result_user) == 1:
            flash(result_user[0][1] + " has successfully logged in!")
            session['user_id'] = result_user[0][0]
            session['username'] = result_user[0][1]

        else:
            flash("Username or password incorrect!")
    else:
        flash("There is something missing!")

def signupReturn(form):
    if form.validate_on_submit():
        # Set username, password and email variables
        un = form.username.data
        pw = form.password.data
        em = form.email.data

        # Check users if the email already exists
        sql_user = """
                        select *
                        from users
                        where email = ?;"""
        cur.execute(sql_user, (em,))
        result_user = cur.fetchall()

        # If a user with that email already exists flash the user with a message else input user into the database
        if len(result_user) >= 1:
            flash("An account with that email already exists!")
        else:
            try:
                cur.execute("INSERT INTO users(username,password,email) VALUES (?,?,?)",(un,pw,em,))
                con.commit()
                flash(un + " you have successfully created an account. You can now log in!")
            except IOError as e:  # If an error occurs print the error code and an error message.
                print(e)
                print("Error: Could not upload account to database!")
                flash("An error occurred and the account could not be created! Please try again later.")
    else:
        flash("There is something missing!")

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    # Set Login Form
    loginform = LoginForm()
    # If the page request method is POST
    if request.method == 'POST':
        # Contacts the loginReturn function which will check if the user exists and logs in and or return a flash msg
        loginReutrn(loginform)

    bookings = getBookings(date.today(), (date.today() + timedelta(days=1)))
    trucks = getTrucks()
    return render_template('index.html', title='Food Trucks', loginform=loginform, bookings=bookings, trucks=trucks)

@app.route('/logout', methods=['GET'])
def logout():
    # clear out the session
    if session.get('user_id'):
        session['user_id'] = None
        session['username'] = None
        flash("You have successfully logged out")
    else:
        flash("You have to be logged in to do that!")
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    # If user is already logged in flash a message and redirect them back to the index page
    if session.get('user_id'):
        flash("You are already logged in!")
        return redirect(url_for('index'))

    # Set Login Form
    loginform = LoginForm()
    # If the page request method is POST
    if request.method == 'POST':
        # Contacts the loginReturn function which will check if the user exists and logs in and or return a flash msg
        loginReutrn(loginform)

    # Set SignUp Form
    form = SignUp()
    if request.method == 'POST':
        # Contacts the signupReturn function which will check the data returned and create an account and or return a flash msg
        signupReturn(form)

    return render_template('signup.html', title='Create an account!', loginform=loginform, form=form)

@app.route('/search', methods=['GET','POST'])
def search():
    # Set Login Form
    loginform = LoginForm()
    # If the page request method is POST
    if request.method == 'POST':
        # Contacts the loginReturn function which will check if the user exists and logs in and or return a flash msg
        loginReutrn(loginform)

    if request.args.get('q'):
        name = request.args.get('q')
        flash(name)
    if request.args.get('t'):
        types = request.args.get('t')
        flash(types)

    trucks = getTrucks()

    return render_template('search.html', title='Search Trucks!', loginform=loginform, trucks=trucks)

# Website Startup
if __name__ == '__main__':
    port = 7250 # Port to be hosted on
    app.run('', 7250, debug=True) # Run the app