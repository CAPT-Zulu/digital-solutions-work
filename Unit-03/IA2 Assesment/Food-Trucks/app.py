# --- Import Libraries --- #
# Flask Libraries (used to run the actual website)
from flask import Flask, render_template, request, redirect, flash, session, url_for  # General Flask
from flask_wtf import FlaskForm  # For Flask forms
from flask_bcrypt import Bcrypt  # For encryption
# WTForms Libraries (used for the websites forms)
from wtforms import StringField, SubmitField, EmailField, PasswordField, validators
# Miscellaneous Libraries
import sqlite3  # To connect and run query's for the database
import requests  # To request and download data from APIs
import json  # Required to be able to view and manage the json files and format
from apscheduler.schedulers.background import \
    BackgroundScheduler  # Used to run the get data and clear data functions every 30 minutes
import atexit  # Used for scheduler to shut down the schedules when the app is exited
from datetime import datetime, date, timedelta  # For getting the current or future datetime


# TODO
#   Add data page with summery infromation and statistics { Not enough time :'( }
#   Make the website look nice { Not enough time :'( }
#   Fix the search page bugs { Not enough time :'( }
#   Add change email or password for / user page { Not enough time :'( }
#   Change out placeholder images / icons for the website { This is a prototype so no need }


# --- Assign flask app --- #
app = Flask(__name__)

# --- Assign Bcrypt --- #
bcrypt = Bcrypt(app)

# --- Security Key --- #
app.config['SECRET_KEY'] = """
    b'\xaa\x8f\xde\xbe\xa5?Fj\n\t\x88\xf6\x0fk1+\x0c\x80\xe9\xd1v7\x9d\xbb[\xbd\xb3Y\xbd\x93T\xfc"""
# Created using os.urandom


# --- Connect database ---#
con = sqlite3.connect('system.db', check_same_thread=False)  # connect to the websites database
cur = con.cursor()  # Set cur to equal the database cursor


# --- Form models --- #
# Login form
class LoginForm(FlaskForm):
    # Username
    username = StringField('Username:', validators=[
        validators.DataRequired()])

    # Password
    password = PasswordField('Password:', validators=[
        validators.DataRequired()])

    # Login form with a submit button which isn't required but added for user ability
    submit = SubmitField('Log In!')


# Sign up form
class SignUp(FlaskForm):
    # Username
    username = StringField('Username:', validators=[
        validators.DataRequired(),
        validators.Length(3, 12, "The username must be 3 characters min and 12 characters max")])

    # Password with a confirmation password
    password = PasswordField('Password:', validators=[
        validators.DataRequired(),
        validators.Length(3, 64, "The password must be 3 characters min and 64 characters max"),
        validators.EqualTo('password_confirmation', message='Passwords must match')])

    password_confirmation = PasswordField('Repeat Password', validators=[
        validators.DataRequired(),
        validators.Length(3, 64, "The password must be 3 characters min and 64 characters max"),
        validators.EqualTo('password', message='Passwords must match')])

    # Email has email validator and has a confirmation field
    email = EmailField('Email:', validators=[
        validators.DataRequired(),
        validators.Email(),
        validators.EqualTo('email_confirmation', message='Emails must match')])

    email_confirmation = EmailField('Repeat Email:', validators=[
        validators.DataRequired(),
        validators.Email(),
        validators.EqualTo('email', message='Emails must match')])

    # Sign up form with a submit button which isn't required but added for user ability
    submit = SubmitField('Create an Account!')


# --- Functions --- #
# getData downloads and converts the API jsons to SQL
def getData():
    # Print to console
    print('Downloading Data, Time: ', datetime.now())

    # Download, convert and merge trucks json to sql
    try:
        # Replaces url everytime the function is called to make sure the url isn't changed
        trucks_page = requests.get("https://www.bnefoodtrucks.com.au/api/1/trucks")
        # Convert page to readable json / dict format
        trucks_json = json.loads(trucks_page.text)
        # For every element in the json file
        for truck_x in trucks_json:
            # Execute INSERT OR REPLACE INTO the truck's table for each truck
            cur.execute("""
                INSERT OR REPLACE INTO trucks(truck_id, name, category, bio, avatar_src, avatar_alt, 
                avatar_title, cover_photo_src, cover_photo_alt, cover_photo_title, website, facebook_url, 
                instagram_handle, twitter_handle)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (
                            truck_x.get('truck_id'), truck_x.get('name'), truck_x.get('category'), truck_x.get('bio'),
                            str(truck_x['avatar']['src'] if truck_x['avatar'] != "" else ""),
                            str('Avatar image of ' + truck_x.get('name')), truck_x.get('name'),
                            str(truck_x['cover_photo']['src'] if truck_x['cover_photo'] != "" else ""),
                            # Avatar photo alt and title replaced with name of truck
                            str('Cover photo of ' + truck_x.get('name')), truck_x.get('name'),
                            # Cover photo alt and title replaced with name of truck
                            truck_x.get('website'), truck_x.get('facebook_url'), truck_x.get('instagram_handle'),
                            truck_x.get('twitter_handle'),))
            # use .get instead of data[''] as if the value doesn't exist it will return null.

        # Commit changes to the table after for loop is complete.
        con.commit()
    except Exception as e:  # If an error occurs print the error code and an error message.
        print(e)
        print("Error: Could not download or convert trucks database")

    # Download, convert and merge sites json to sql
    try:
        # Replaces url everytime the function is called to make sure the url isn't changed
        sites_page = requests.get("https://www.bnefoodtrucks.com.au/api/1/sites")
        # Convert page to readable json / dict format
        sites_json = json.loads(sites_page.text)
        # For every element in the json file
        for site_x in sites_json:
            # Execute INSERT OR REPLACE INTO the site's table for each site
            cur.execute("""
                INSERT OR REPLACE INTO sites(site_id, title, description, street, suburb, state, 
                postcode, country, latitude, longitude, spots, cost, image_src, image_alt, 
                image_title, map_src, map_alt, map_title) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (
                            site_x.get('site_id'), site_x.get('title'), site_x.get('description'), site_x.get('street'),
                            site_x.get('suburb'), site_x.get('state'), site_x.get('postcode'), site_x.get('country'),
                            site_x.get('latitude'), site_x.get('longitude'), site_x.get('spots'), site_x.get('cost'),
                            str(site_x['image']['src'] if site_x['image'] != "" else ""),
                            str('Image of ' + site_x.get('title'), site_x.get('title')),
                            str(site_x['map']['src'] if site_x['map'] != "" else ""),
                            (str(site_x.get('street')) + ", " + str(site_x.get('suburb')) + ", " +
                             str(site_x.get('state')) + ", " + str(site_x.get('postcode')) + ", " +
                             str(site_x.get('country'))),
                            (str(site_x.get('street')) + ", " + str(site_x.get('suburb')) + ", " +
                             str(site_x.get('state')) + ", " + str(site_x.get('postcode')) + ", " +
                             str(site_x.get('country'))),))  # replaced map and image alt and title with custom values

        # Commit changes to the table after for loop is complete.
        con.commit()
    except Exception as e:  # If an error occurs print the error code and an error message.
        print(e)
        print("Error: Could not download or convert sites database")

    # Download, convert and merge bookings json to sql
    try:
        # Replaces url everytime the function is called to make sure the url isn't changed
        bookings_page = requests.get("https://www.bnefoodtrucks.com.au/api/1/bookings")
        # Convert page to readable json / dict format
        bookings_json = json.loads(bookings_page.text)
        # For every element in the json file
        for booking_x in bookings_json:
            # Execute INSERT OR REPLACE INTO the site's table for each site
            cur.execute("""
                INSERT OR REPLACE INTO bookings(title, truck_id, site_id, start, finish)
                VALUES (?,?,?,?,?)""",
                        (
                            booking_x.get('title'), booking_x.get('truck_id'), booking_x.get('site_id'),
                            booking_x.get('start'), booking_x.get('finish'),))

        # Commit changes to the table after for loop is complete.
        con.commit()
    except Exception as e:  # If an error occurs print the error code and an error message.
        print(e)
        print("Error: Could not download or convert bookings database")

    # Download, convert and merge drive up bookings json to sql
    try:
        # Replaces url everytime the function is called to make sure the url isn't changed
        driveup_page = requests.get("https://www.bnefoodtrucks.com.au/api/1/driveup-bookings")
        # Convert page to readable json / dict format
        driveup_json = json.loads(driveup_page.text)
        # For every element in the json file
        for driveup_x in driveup_json:
            # Execute INSERT OR REPLACE INTO the booking's table for each drive up bookings
            cur.execute("""
                INSERT OR REPLACE INTO bookings(title, truck_id, site_id, start, finish, address, latitude, longitude)
                VALUES (?,?,?,?,?,?,?,?)""",
                        (
                            driveup_x.get('title'), driveup_x.get('Food truck'), '', driveup_x.get('Check in time'),
                            driveup_x.get('Check out time'), driveup_x.get('Address'),
                            driveup_x['Geolocation']['latitude'], driveup_x['Geolocation']['longitude'],))

        # Commit changes to the table after for loop is complete.
        con.commit()
    except Exception as e:  # If an error occurs print the error code and an error message.
        print(e)
        print("Error: Could not download or convert drive up bookings database")

    # Clean old data
    cleanData()


# cleanData clears month old data to make sure the database runs efficiently
def cleanData():
    # Will clean the database of old files to make sure the db runs smoothly
    try:
        # Delete bookings that finished a month ago or more
        cur.execute("""
            DELETE FROM bookings
            WHERE finish <= date('now', '-1 month');""")
        # Commit changes to the table
        con.commit()
    except Exception as e:  # If an error occurs print the error code and an error message.
        print(e)
        print("Error: Could not delete old data from the bookings table")


# getLocation converts a string of a suburb or postcode and gets the most likely coordinates
def getLocation(q):
    # Set the url for the get request
    url = "https://v0.postcodeapi.com.au/suburbs.json?q=" + q

    # Try to get request and parse it
    try:
        # Request the url for json
        location_request = requests.get(url)
        # Convert text to readable json / dict format
        location_json = json.loads(location_request.text)
        # Parse the json
        return location_json

    except Exception as e:  # If an error occurs print the error code and an error message.
        print(e)
        print("Error: Could not request the location")
        # Parse null
        return []


# getBookings gets bookings happening between a start time and end time
def getBookings(startTime, endTime):
    # Get Bookings
    sql_bookings = """
        SELECT * 
        FROM sites s, bookings b, trucks t 
        WHERE s.site_id = b.site_id
        AND b.truck_id = t.truck_id
        AND b.finish > (?)
        AND b.finish < (?)
        ORDER BY b.start;"""
    cur.execute(sql_bookings, (startTime, endTime,))
    results_bookings = cur.fetchall()

    # Abandoned geojson concept for string location data
    # geo_json_list = []
    # for booking in results_bookings:
    #     # code to generate your geoJSON
    #     crood = Point((booking[9],booking[8]))
    #     point = Feature(geometry=crood, properties={"name": "test1", "amenity": "test2", "popupContent": "test3"})
    #     geo_json_list.append(point)
    # with open('static/jsons/geodata.json', 'a') as f:
    #     json.dump(geo_json_list, f, indent=4)

    # Return results
    return results_bookings


# getTrucks returns all the trucks in the db (Not finished)
def getTrucks():
    # Get Trucks
    # This function needs to be change to allow for ordering by random
    sql_trucks = """
        SELECT *
        FROM trucks;"""
    cur.execute(sql_trucks)
    results_trucks = cur.fetchall()

    # Return results
    return results_trucks


# getUsersFavourites gets the users favourite trucks
def getUsersFavourites():
    # Get Users Favourite Trucks
    sql_fav_trucks = """
        SELECT truck_id
        FROM users_favourites
        WHERE user_id = ?;"""
    cur.execute(sql_fav_trucks, (session.get('user_id'),))
    results_fav_trucks = cur.fetchall()

    # Return results
    return results_fav_trucks


# getTruck gets all the information about a particular truck
def getTruck(id_x):
    # Get Truck
    sql_trucks = """
        SELECT *
        FROM trucks
        WHERE truck_id = ?;"""
    cur.execute(sql_trucks, (id_x,))
    results_truck = cur.fetchone()

    # Return results
    return results_truck


# getTruckRatings gets a trucks ratings
def getTruckRatings(id_x):
    # Get Truck Ratings
    sql_ratings = """
        SELECT rating
        FROM users_ratings
        WHERE truck_id = ?;"""
    cur.execute(sql_ratings, (id_x,))
    results_ratings = cur.fetchall()

    # Return results
    return results_ratings


# getSites gets all the sites in the db
def getSites():
    # Get Sites
    sql_sites = """
            SELECT *
            FROM sites;"""
    cur.execute(sql_sites)
    results_sites = cur.fetchall()

    # Return results
    return results_sites


# getSite gets all the information about a particular site
def getSite(id_x):
    # Get Site
    sql_sites = """
            SELECT *
            FROM sites
            WHERE site_id = ?;"""
    cur.execute(sql_sites, (id_x,))
    results_site = cur.fetchone()

    # Return results
    return results_site


# loginReturn handles the login form and system on every page of the website
def loginReturn(form):
    if form.validate_on_submit():
        # Set email and password variables
        un = form.username.data
        pw = form.password.data

        # Check users if the combination of username and password exists
        sql_user = """
                        select *
                        from users 
                        where username = ?;"""
        cur.execute(sql_user, (un,))
        result_user = cur.fetchall()

        # If a user with that username and password combination exists set session values with the users data
        if len(result_user) == 1 and bcrypt.check_password_hash(result_user[0][2], pw):
            flash(str(result_user[0][1]) + " has successfully logged in!", 'message')
            session['user_id'] = result_user[0][0]
            session['username'] = result_user[0][1]
        else:
            flash("Username or password incorrect!", 'error')
    else:
        flash("There is something missing!", 'error')


# signupReturn handles the signup form and system on the signup page
def signupReturn(form):
    if form.validate_on_submit():
        # Set username, password and email variables
        un = form.username.data
        em = form.email.data
        pw = form.password.data

        # Encrypt Password
        pw_hash = bcrypt.generate_password_hash(pw)
        # Encrypt Email
        em_hash = bcrypt.generate_password_hash(em)

        try:
            # Check users if the email already exists
            sql_user = """
                            select *
                            from users
                            where username = ?;"""
            cur.execute(sql_user, (un,))
            if len(cur.fetchall()) >= 1:
                # If an account already exists with the inputted username flash an error
                flash("An account with that username already exists!", 'error')
                return None

            # Check users if the email already exists
            # No longer WORKS due to email being encrypted FIX THIS!!!
            sql_user = """
                            select *
                            from users
                            where email = ?;"""
            cur.execute(sql_user, (em_hash,))
            if len(cur.fetchall()) >= 1:
                # If an account already exists with the inputted email flash an error
                flash("An account with that email already exists!", 'error')
                return None

            try:
                # Insert new user into database with encrypted password and email
                cur.execute("INSERT INTO users(username,password,email) VALUES (?,?,?)", (un, pw_hash, em_hash,))
                con.commit()

                # Flash success message
                flash(un + " has successfully created an account!", 'message')

                # Attempt login
                loginReturn(form)
            except Exception as e:  # If an error occurs print the error code and an error message.
                print(e)
                print("Error: Could not upload account to database!", 'error')
                # Flash error message
                flash("An error occurred and the account could not be created! Please try again later.", 'error')
        except Exception as e:  # If an error occurs print the error code and an error message.
            print(e)
            print("Error: Account already existed!")
            # Flash error message
            flash("Please try again.", 'error')
    else:
        flash("There is something missing!", 'error')


# --- Schedules --- #
schedule_0 = BackgroundScheduler()  # Sets up the background scheduler
schedule_0.add_job(func=getData, trigger='interval', minutes=30)  # Sets getData function to run every 30 minutes
schedule_0.start()  # Starts the schedules
atexit.register(lambda: schedule_0.shutdown())  # Sets up the schedular to shut down when the app is exited


# --- Routes --- #
# Main page contains the map and relate information and links to the rest of the site
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # Set Login Form
    loginform = LoginForm()
    # If the page request method is POST
    if request.method == 'POST':
        # Contacts the loginReturn function which will check if the user exists and logs in and or return a flash msg
        loginReturn(loginform)

    # This should be moved to javascript when possible most likely using jquery $.get() so the page doesn't have to be
    # refreshed
    # If trying to get suburb
    suburb = request.args.get('sub')  # could be '4056' or 'Bald Hills'
    time = request.args.get('tme')  # Format: 2022-05-17

    # Complex 1 line versions of the code however its abandoned as its inefficient
    # suburb = getLocation(request.args.get('sub'))[0] if request.args.get('sub') else crd = ""
    # time = datetime.strptime(request.args.get('tme').replace('-', '/')[2:], '%y/%m/%d') if \
    #     request.args.get('tme') else time = date.today()  # Format: 2022-05-17

    # If the suburb request exists get and set location else set it too brisbane
    if suburb:
        location = getLocation(suburb)
        location = location[0] if len(location) >= 1 else ""
    else:
        location = {'latitude': '-27.474', 'longitude': '153.038'}

    # If the time request exists convert the string to a datetime else get today's date
    if time:
        time = datetime.strptime(time.replace('-', '/')[2:], '%y/%m/%d')
    else:
        time = date.today()

    # Get bookings for the given date
    bookings = getBookings(time, (time + timedelta(days=1)))
    trucks = getTrucks()

    # Render the page
    return render_template('index.html', title='Food Trucks', loginform=loginform, bookings=bookings, trucks=trucks,
                           crd=location)


# Logout page logsout the user and redirect the user back to the index page
@app.route('/logout', methods=['GET'])
def logout():
    # clear out the session
    if session.get('user_id'):
        session['user_id'] = None
        session['username'] = None
        flash("You have successfully logged out", 'message')
    else:
        flash("You have to be logged in to do that!", 'error')
    return redirect(url_for('index'))


# Signup page has the sign up form for users to create an account
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # If user is already logged in flash a message and redirect them back to the index page
    if session.get('user_id'):
        flash("You are already logged in!", 'error')
        return redirect(url_for('index'))

    # Set SignUp Form
    signup_form = SignUp()
    # Set Login Form
    login_form = LoginForm()

    # If the page request method is POST
    if request.method == 'POST':
        if signup_form.validate():
            # Contacts the signupReturn function which will check the data returned and create an account and or
            # return a flash msg
            signupReturn(signup_form)
        else:
            # Contacts the loginReturn function which will check if the user exists and logs in and or return a flash
            # msg
            loginReturn(login_form)

    return render_template('signup.html', title='Create an account!', loginform=login_form, form=signup_form)


# Search page has all thr trucks you can easily search through with queries
@app.route('/search', methods=['GET', 'POST'])
def search():
    # Set Login Form
    loginform = LoginForm()
    # If the page request method is POST
    if request.method == 'POST':
        # Contacts the loginReturn function which will check if the user exists and logs in and or return a flash msg
        loginReturn(loginform)

    # For search bar in navbar
    q = request.args.get('q') if request.args.get('q') is not None else ""

    # Get Trucks
    trucks = getTrucks()

    return render_template('search.html', title='Search Trucks!', loginform=loginform, trucks=trucks, q=q)


# Truck page contains relent information to a clicked on truck
@app.route('/truck', methods=['GET', 'POST'])
def truck():
    # For search bar in navbar
    id_x = request.args.get('id')

    # If truck exists get data
    truck_x = getTruck(id_x)

    # If truck id is valid render page if not return to index with an error
    if truck_x:
        # Set Login Form
        loginform = LoginForm()

        if session.get('user_id'):
            # Get users favourite trucks
            user_fav = getUsersFavourites()
        else:
            # Set user favourites empty
            user_fav = ""

        # If the page request method is POST
        if request.method == 'POST':
            if loginform.validate():
                # Contacts the loginReturn function which will check if the user exists and logs in and or return a
                # flash msg
                loginReturn(loginform)
            else:
                if session.get('user_id'):
                    # Inserts or places the users rating with the data supplied from the form
                    rating = request.form.get('rating')
                    if rating:
                        cur.execute(
                            """INSERT OR REPLACE INTO users_ratings(user_id, truck_id, rating) VALUES (?,?,?)""",
                            (session.get('user_id'), id_x, rating,))
                        con.commit()
                        flash('You have successfully changed your rating for this truck!')

            # Favourite or un-favourite get and set
            if session.get('user_id'):
                if request.form.get("fav_btn") == 'fav':  # Check if user is trying to favourite a truck
                    sql_fav = """
                                    INSERT OR REPLACE INTO users_favourites (user_id, truck_id)
                                    VALUES (?, ?, ?);"""
                    cur.execute(sql_fav, (session['user_id'], id_x,))  # Favourite truck
                    con.commit()
                    flash("Successfully favourited truck!")
                elif request.form.get("fav_btn") == 'un_fav':  # Check if user is trying to un-favourite a truck
                    sql_un_fav = """
                                    DELETE FROM users_favourites
                                    WHERE user_id = ?
                                    AND truck_id = ?;"""
                    cur.execute(sql_un_fav, (session['user_id'], id_x,))  # Un-favourite truck
                    con.commit()
                    flash("Successfully un-favourited truck!")

        # Get Truck Rating
        results_ratings = getTruckRatings(id_x)

        # Check if any ratings exist
        if results_ratings:
            # Set an average rating variable
            avg_rating = 0
            # For every rating += the average rating
            for rating in results_ratings:
                avg_rating += rating[0]
            # Finally, divide the avg_rating variable by the count of ratings and round it to 0 decimal places
            avg_rating = round((avg_rating / len(results_ratings)), 0)
        else:
            # If no ratings are found set the avg_ratings to 0
            avg_rating = 0

        # Get Booking History
        sql_bookings = """
            SELECT * 
            FROM bookings b, sites s 
            WHERE b.truck_id = ?
            AND b.site_id = s.site_id
            ORDER BY b.start;"""
        cur.execute(sql_bookings, (id_x,))
        bookings = cur.fetchall()
        
        return render_template('truck.html', title=truck_x[1], loginform=loginform, truck=truck_x, rating=avg_rating,
                               user_fav=user_fav, bookings=bookings)
    else:
        flash("We couldn't find a truck with that id. Please try again!", 'error')
        return redirect(url_for('index'))


# Sites page contains a map showing all the sites in the database
@app.route('/sites', methods=['GET', 'POST'])
def sites():
    # Set Login Form
    loginform = LoginForm()

    # If the page request method is POST
    if request.method == 'POST':
        # Contacts the loginReturn function which will check if the user exists and logs in and or return a
        # flash msg
        loginReturn(loginform)

    # Get Sites
    sites_x = getSites()
    return render_template('sites.html', title='Sites', loginform=loginform, sites=sites_x)


# Site page contains relent information to a clicked on site
@app.route('/site', methods=['GET', 'POST'])
def site():
    # For search bar in navbar
    id_x = request.args.get('id')

    # If truck exists get data
    site_x = getSite(id_x)

    # If truck id is valid render page if not return to index with an error
    if site_x:
        # Set Login Form
        loginform = LoginForm()

        # If the page request method is POST
        if request.method == 'POST':
            # Contacts the loginReturn function which will check if the user exists and logs in and or return a
            # flash msg
            loginReturn(loginform)

        # Get Bookings
        sql_bookings = """
            SELECT * 
            FROM bookings b, trucks t 
            WHERE b.site_id = ?
            AND b.truck_id = t.truck_id
            ORDER BY b.start;"""
        cur.execute(sql_bookings, (id_x,))
        bookings = cur.fetchall()

        return render_template('site.html', title=site_x[1], loginform=loginform, site=site_x, bookings=bookings)
    else:
        flash("We couldn't find a site with that id. Please try again!", 'error')
        return redirect(url_for('index'))


# User page contains relvent infromation to the user and the ability to change email, password or delete the account
@app.route('/user', methods=['GET', 'POST'])
def user():
    # Wasn't added due to time constraints but would have included an ability to change the users email or password
    return render_template('user.html', title='User Settings!')


# Redirect most common error pages
@app.errorhandler(404)
@app.errorhandler(403)
@app.errorhandler(410)
@app.errorhandler(500)
def page_not_found(e):
    flash("Whoops, " + str(e), 'error')
    return redirect(url_for('index'))


# --- Website Startup --- #
if __name__ == '__main__':
    # Start App
    port = 7250  # Port to be hosted on
    app.run('', port, debug=True)  # Run the app
