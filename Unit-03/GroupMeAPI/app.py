#!/usr/bin/env python  #step 1 import library
import json  # Step1 import libraries
import requests
from flask import Flask, render_template, request
from flask import jsonify


# Use JSONPlaceHolder as an example
req = requests.get('https://jsonplaceholder.typicode.com/todos/1')
print(req.text)


# Step2 - create instance of Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'myverysectretkey'

url = "https://free-nba.p.rapidapi.com/players"






@app.errorhandler(404)
def page_not_found(e):
    return "Oops, looks like your lost!"


if __name__ == '__main__':
    host = '127.0.0.1'
    # port = 8080
    app.run(debug=True)
