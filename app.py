from flask import Flask, render_template, request, Response, session, g
import flask
import json
import requests
import functools
import mysql.connector
from mysql.connector import errorcode
from subprocess import call
import data

app = Flask(__name__)
app.config.update(dict(
    DATABASE="airline_company",
    DEBUG=True,
    SECRET_KEY='eskihafiz',
    USER="root",
    PASS="omer"
))

def connect_db():
    db = mysql.connector.connect(user=app.config['USER'], passwd=app.config['PASS'])
    try:
        db.database = app.config['DATABASE']
    except mysql.connector.Error as err:
        return None
    return data.database(db)

def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        #session.pop('isloggedin', None)
        if 'isloggedin' in session:
            return method(*args, **kwargs)
        else:
            return flask.redirect('/login')
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    #if 'isloggedin' in session:
    #    return flask.redirect('/')

    if request.method == 'POST':
        print request.form.keys()
        if 'id' in request.form and 'password' in request.form:
            userid = request.form['id']
            password = request.form['password']
            if db.check_login(userid, password):
                session['id'] = userid
                session['isloggedin'] = True
                session['user_type'] = db.get_user_type(userid)
                return flask.redirect('/')
            else:
                return flask.redirect('/login')

    return render_template('loginv2.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    db = get_db()
    #if 'isloggedin' in session:
    #    return flask.redirect('/')

    if request.method == 'POST':
        return render_template('registerv2.html')

    return render_template('registerv2.html')

@app.route('/')
@login_required
def init_screen():
    if session['user_type'] == 'passenger':
        return flask.redirect('/flights')
    return session['user_type']

@app.route('/flights')
@login_required
def flight_passenger_screen():
    pass_id = session['id']
    source_filter = None
    dest_filter = None
    flight_id = None
    return render_template("flight_passenger.html")

@app.route('/history')
@login_required
def history_screen():
    return render_template("history_passenger.html")

@app.route('/reservations')
@login_required
def reservations_screen():
    return render_template("reservations_passenger.html")

@app.route('/stores')
@login_required
def store_screen():
    return render_template("store_passenger.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3131, debug=True)
