from flask import Flask, render_template, request, redirect, flash, url_for, session
app = Flask(__name__)

#########################################################################
# HTTP Routes
#########################################################################
@app.route('/')
def home():
    if request.args:
        if request.args.get('lang') != 'en':
            return 'no'
        return 'nothing'
    else:
        return 'This is the home page route'

@app.route('/menu')
@app.route('/menus')
def menu():
    return 'Menu or menus'

@app.route('/about')
def index():
    return 'You have found the about page route'

@app.route('/contact')
def contact():
    if request.args:
        if request.args.get('from') == 'facebook':
            return 'Facebook me?'
        else:
            return 'Email me.'
    else:
        return 'bonk'
#########################################################################
if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    app.run(host, port, debug=True)