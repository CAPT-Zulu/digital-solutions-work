#!/usr/bin/env python
import json
import requests
from flask import Flask, render_template

# create instance of Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'myverysecretkey'

url = "https://covid-193.p.rapidapi.com/countries?rapidapi-key=bd06bb2382msh874e76e6ff29000p12bc4djsn26abdf362181"

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "xxxxxxxxxxxxxxxxxxxx"
    }

# Test output to console
response = requests.request("GET", url, headers=headers)
print("The data is: ")
print(response.text)

@app.route('/', methods=['GET'])
def index():
    #req = requests.get('https://cat-fact.herokuapp.com/facts')  # should build in check that request was successful
    req = requests.get(url)  # should build in check that request was successful
    data = json.loads(req.content)
    return render_template('index.html', data=data['get'])


if __name__ == '__main__':
    host = '127.0.0.1'
    #port = 8080
    app.run(debug=True)
