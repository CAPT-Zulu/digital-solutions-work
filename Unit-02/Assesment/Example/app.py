from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_bootstrap import Bootstrap
from datetime import datetime, date
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectMultipleField, SelectField
from wtforms.fields.html5 import DateField # see https://stackoverflow.com/questions/26057710/datepickerwidget-with-flask-flask-admin-and-wtforms
from wtforms.validators import DataRequired, URL, Optional, InputRequired

import random

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'ddksididkdkdl'

Bootstrap(app)

# configure file uploads used when registering an act
app.config['UPLOADED_IMAGES_DEST'] = 'static/images/acts'




### Form models ####

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


########## routes ##########


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')



@app.route('/logout')
def logout():
    # clear out the session
    flash("You have successfully logged out")
    return redirect(url_for('index'))


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    app.run(host, port, debug=True)
