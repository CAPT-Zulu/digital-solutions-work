#!/usr/bin/env python  #step 1 import library
import json  #Step1 import libraries
import requests, time, hashlib
from flask import Flask, render_template

# Step2 - create instance of Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'myverysectretkey'

timestamp = str(time.time())
publickey = "xxxxxxxxxxxxxxxxxxxx"
privatekey = "xxxxxxxxxxxxxxxxxxxx"
hash_string = timestamp + privatekey + publickey  #adding the string together for hashing
hash = hashlib.md5(hash_string.encode("utf-8")).hexdigest()
parameters = {"ts": timestamp, "apikey": publickey, "hash": hash}

url = "http://gateway.marvel.com/v1/public/comics/1111"
request = requests.get(url, params=parameters)
print(request.status_code)

@app.route('/', methods=['GET'])
def index():
    response = requests.get(url, params=parameters).json()
    return render_template('index.html', data=response)
#request = requests.get(url, params=parameters, proxies=None, auth=proxy_auth).json()
request = requests.get(url, params=parameters).json()

print(request)  # to display all the wrapper and container data
#print(request["data"]["results"])  # displays comic data only
print(request["data"]["results"][0]["title"])  # displays the title of the first comic result

if __name__ == '__main__':
    host = '127.0.0.1'
    #port = 8080
    app.run(debug=True)
