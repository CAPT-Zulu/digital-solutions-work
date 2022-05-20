#!/usr/bin/env python  #step 1 import library
import json  #Step1 import libraries
import requests, time, hashlib
from flask import Flask, render_template

# Step2 - create instance of Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'myverysectretkey'

response_API = requests.get('https://api.covid19india.org/state_district_wise.json')
#print(response_API.status_code)
# if 200 = success
data = response_API.text
# requests.get helps us pull the data from the API
parse_json = json.loads(data)
active_case = parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
print("Active cases in South Andaman:", active_case)

@app.route('/', methods=['GET'])
def index():
    active_case = parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
    return render_template('index.html', data=active_case)


if __name__ == '__main__':
    host = '127.0.0.1'
    #port = 8080
    app.run(debug=True)
