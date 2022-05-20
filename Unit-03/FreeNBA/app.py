#!/usr/bin/env python  #step 1 import library
import json  # Step1 import libraries
import requests
from flask import Flask, render_template

# Step2 - create instance of Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'myverysectretkey'

url = "https://eonet.gsfc.nasa.gov/api/v3/events?limit=10"

@app.route('/', methods=['GET'])
def index():
    req = requests.get(url)
    data = json.loads(req.content)
    return render_template('index.html', data=data['events'])

#response = requests.request("GET", url, headers=headers, params=querystring)
#print(response.text)

if __name__ == '__main__':
    # host = '0.0.0.0'
    # port = 8080
    app.run(debug=True)
