# Import Libraries
import sqlite3 # To connect and run querys for the database
import requests # To request and download data from API's
import json # Required to be able to view and manage the json files and format
from datetime import datetime, date, timedelta # For getting the current or future datetime (This isn't being used at the momment)
from geojson import Point, Feature

con = sqlite3.connect('system.db', check_same_thread=False) # connect to the websites database
cur = con.cursor() # Set cur to equal the database cursor

try:
    sites_page = requests.get(
        "https://www.bnefoodtrucks.com.au/api/1/sites")  # Replaces url everytime the function is called to make sure the url isnt changed
    sites_json = json.loads(sites_page.text)  # Convert page to readable json / dict format
    for site in sites_json:  # For every element in the json file
        # Do not use MURGE because of ...
        cur.execute(
            """INSERT OR REPLACE INTO sites(site_id, title, description, street, suburb, state, postcode, country, latitude, longitude, spots, cost, image_src, image_alt, image_title, map_src, map_alt, map_title) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (site.get('site_id'),site.get('title'),site.get('description'),site.get('street'),site.get('suburb'),
             site.get('state'),site.get('postcode'),site.get('country'),site.get('latitude'),site.get('longitude'),
             site.get('spots'),site.get('cost'),str((site.get('image')).get('src')),str((site.get('image')).get('alt')),str((site.get('title')).get('src')),str((site.get('map')).get('src')),str((site.get('map')).get('alt')),str((site.get('map')).get('title')),))
    con.commit()  # Commit changes to the table after for loop is complete.
except IOError as e:  # If an error occurs print the error code and an error message.
    print(e)
    print("Error: Could not download or convert sites database")