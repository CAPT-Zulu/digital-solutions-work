import requests
import json
import sqlite3

# Connect database
con = sqlite3.connect('database2.db', check_same_thread=False) # connect to the websites database
cur = con.cursor() # Set cur to equal the database cursor

def getData():
    # Download, convert and merge trucks json to sql
    try:
        trucks_page = requests.get("https://www.bnefoodtrucks.com.au/api/1/trucks")  # Replaces url everytime the function is called to make sure the url isnt changed
        trucks_json = json.loads(trucks_page.text) # Convert page to readable json / dict format
        for truck in trucks_json: # For every element in the json file
            # Do not use MURGE because of ...
            cur.execute("""INSERT OR REPLACE INTO trucks(truck_id, name, category, bio, avatar,cover_photo, website, facebook_url, instagram_handle, twitter_handle)VALUES (?,?,?,?,?,?,?,?,?,?)""", (truck.get('truck_id'),truck.get('name'),truck.get('category'),truck.get('bio'),str(truck.get('avatar')),str(truck.get('cover_photo')),truck.get('website'),truck.get('facebook_url'),truck.get('instagram_handle'),truck.get('twitter_handle'),)) # use .get instead of data[''] as if the value doesnt exists it will return null. Have to convert the json for the images to string before parsing it to prevent errors in the future.
        con.commit() # Commit changes to the table after for loop is complete.
    except IOError as e: # If an error occurs print the error code and an error message.
        print(e)
        print("Error: Could not download or convert trucks database")

    # Download, convert and merge sites json to sql
    try:
        sites_page = requests.get("https://www.bnefoodtrucks.com.au/api/1/sites")  # Replaces url everytime the function is called to make sure the url isnt changed
        sites_json = json.loads(sites_page.text) # Convert page to readable json / dict format
        for site in sites_json: # For every element in the json file
            # Do not use MURGE because of ...
            cur.execute("""INSERT OR REPLACE INTO sites(site_id, title, description, street, suburb, state, postcode, country, latitude, longitude, spots, cost, image, map) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (site.get('site_id'),site.get('title'),site.get('description'),site.get('street'),site.get('suburb'),site.get('state'),site.get('postcode'),site.get('country'),site.get('latitude'),site.get('longitude'),site.get('spots'),site.get('cost'),str(site.get('image')),str(site.get('map'),)))
        con.commit() # Commit changes to the table after for loop is complete.
    except IOError as e: # If an error occurs print the error code and an error message.
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

getData()