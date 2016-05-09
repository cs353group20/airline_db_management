from flask import Flask, render_template, request, Response, session, g
import datetime
import flask
import json
import requests
import functools
import mysql.connector
from mysql.connector import errorcode
from subprocess import call
import data
import menu

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

@app.context_processor
def inject_menu_options():
    MENU = menu.get_menu()
    if 'user_type' in session:
        if session['user_type'] in MENU:
            return dict(menu = MENU[session['user_type']])
        else:
            return dict(menu = MENU['passenger'])
    return dict(essek="baki")

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
    if 'isloggedin' in session:
        return flask.redirect('/')

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
                return render_template('login.html', message={
                    'type': 'warning',
                    'str': 'Wrong User ID or Password entered!'
                })

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    db = get_db()
    if 'isloggedin' in session:
        return flask.redirect('/')

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        password_check = request.form['passwordCheck']
        if password != password_check:
            return render_template('register.html', message={
                'type': 'warning',
                'str': 'Passwords doesn\'t match'
            })
        no = request.form['street_number']
        street = request.form['street']
        town = request.form['town']
        city = request.form['city']
        phone = request.form['phone']
        email = request.form['email']
        ret = db.signup(name, password, no, street, town, city, phone, email)
        return render_template('register.html', message={
            'type': 'success',
            'str': 'Sign up complete.User ID is:' + str(ret) + ' Go to login page!'
        })

        #return flask.redirect('/login')

    return render_template('register.html')

@app.route('/')
@login_required
def entry():
    return "YARRAK"

@app.route('/passenger/buy', methods=['POST'])
@login_required
def buy_ticket():
    db = get_db();
    print("ID: {} FLIGHTID: {}".format(session['id'], request.form['flightID']))
    #db.add_ticket(session['id'], request.form['flightID'], 12)
    return render_template('passenger_flight.html', message={
        'type': 'success',
        'str': 'Ticket successfully bought!'
    })

@app.route('/passenger/menu', methods=['POST'])
@login_required
def get_menu():
    flightID = request.form['flightID']
    data = [{
        'id': '121212',
        'name': 'omer',
        'price': '31'
    }]
    return render_template("menu_table.html", data=data)

@app.route('/passenger/reserve', methods=['POST'])
@login_required
def reserver_ticket():
    flightID = request.form['flightID']
    userID = session['id']
    return json.dumps({'type': 'warning', 'str': "YARRAK"})

@app.route('/passenger/flights', methods=['GET', 'POST'])
@login_required
def passenger_flights():
    if request.method == 'POST':
        toStr = request.form['toInput']
        fromStr = request.form['fromInput']
        retData = []
        for i in range(10):
            retData.append({
                "flight_id": str(i + 10),
                "date": "May {}, 2016".format(i),
                "departure": "03:{}".format(i),
                "eta": "{}:03".format(i),
                "from": fromStr,
                "to": toStr,
                "duration": str(i + 31),
                "class": "business",
                "price": str(i * 3)
            });
        return render_template('flight_table.html', data=retData)
    return render_template('passenger_flight.html')

@app.route('/passenger/flight_history', methods=['GET', 'POST'])
@login_required
def passenger_history():
    retData = []
    for i in range(10):
        retData.append({
            "flight_id": str(i + 10),
            "date": "May {}, 2016".format(i),
            "departure": "03:{}".format(i),
            "eta": "{}:03".format(i),
            "from": 'ankara',
            "to": 'istanbul',
            "duration": str(i + 31),
            "class": "business",
            "price": str(i * 3)
        })
    retData[0]['deadline_not_passed'] = True
    if request.method == 'POST':
        # FOR PASSED
        return json.dumps({'type': 'fee', 'fee': 300})
        # FOR NOT PASSED
        return json.dumps({'type': 'success', 'str': request.form['flightID']})
    return render_template('passenger_history.html', data=retData)

@app.route('/passenger/deadline_fee', methods=['POST'])
@login_required
def passenger_fee():
    retData = []
    for i in range(10):
        retData.append({
            "flight_id": str(i + 10),
            "date": "May {}, 2016".format(i),
            "departure": "03:{}".format(i),
            "eta": "{}:03".format(i),
            "from": 'ankara',
            "to": 'istanbul',
            "duration": str(i + 31),
            "class": "business",
            "price": str(i * 3)
        })
    retData[0]['deadline_not_passed'] = True
    flightID = request.form['flight_id']
    return render_template('passenger_history.html', message={
        'type': 'success',
        'str': json.dumps(request.form)
    }, data=retData)

@app.route('/passenger/reservations', methods=['GET', 'POST'])
@login_required
def passenger_reservations():
    retData = []
    for i in range(10):
        retData.append({
            "flight_id": str(i + 10),
            "date": "May {}, 2016".format(i),
            "departure": "03:{}".format(i),
            "eta": "{}:03".format(i),
            "from": 'ankara',
            "to": 'istanbul',
            "duration": str(i + 31),
            "class": "business",
            "price": str(i * 3)
        })
    retData[0]['deadline_not_passed'] = True
    return render_template('passenger_reservations.html', data = retData)

@app.route('/passenger/cancel_reservation', methods=['POST'])
@login_required
def cancel_reservation():
    print(request.form)
    flightID = request.form['flightID']
    return json.dumps({
        'type': 'success',
        'str': "{} cancelled".format(flightID)
    })

@app.route('/passenger/store', methods=['GET', 'POST'])
@login_required
def passenger_store():
    if request.method == 'POST':
        retData = []
        for i in range(1, 10):
            retData.append({
                'airport': 'ankara',
                'store_name': 'adfadsf',
                'owner': 'eben'
            })
        return render_template('store_table.html', data=retData)
    return render_template('passenger_store.html')

@app.route('/profile', methods=['GET'])
@login_required
def profile_screen():
    data = {
        "name": "Omer",
        "ID": '10',
        'email': 'imer@gmail.com',
        'address': 'cankaya',
        'phone': '313131313',
        'expenditure': 'asdfadsf'
    }
    return render_template('profile.html', data=data)

@app.route('/profile/<type>', methods=['POST'])
@login_required
def change_profile_screen(type):
    return render_template('profile.html', data=data, message={
        'type': 'success',
        'str': json.dumps(request.form) + "TYPE: " + type
    })

@app.route('/attendant/current', methods=['GET', 'POST'])
@login_required
def attendant_current():
    if request.method == 'POST':
        flightID = request.form['flightID']
        retData = {
            "flight_id": flightID,
            "plane_id": "palneIDFILED",
            "model": "modelFILD",
            "range": "over 9000",
            "altitude": "10000 feeetetet"
        }
        return render_template("plane_table.html", data = retData)
    retData = []
    for i in range(10):
        retData.append({
            "flight_id": str(i + 10),
            "date": "May {}, 2016".format(i),
            "departure": "03:{}".format(i),
            "eta": "{}:03".format(i),
            "from": 'ankara',
            "to": 'istanbul',
            "duration": str(i + 31),
        })
    return render_template('attendant_current.html', data=retData)

@app.route('/attendant/flight_history')
@login_required
def attendant_history():
    retData = []
    for i in range(10):
        retData.append({
            "flight_id": str(i + 10),
            "date": "May {}, 2016".format(i),
            "departure": "03:{}".format(i),
            "eta": "{}:03".format(i),
            "from": 'ankara',
            "to": 'istanbul',
            "duration": str(i + 31),
        })
    return render_template('attendant_history.html', data=retData)

@app.route('/attendant/food_promotion', methods=['GET', 'POST'])
@login_required
def attendant_food_promotion():
    if request.method == 'POST':
        retData = []
        for i in range(10):
            retData.append({
                'pass_id': str(i + 10),
                'promotion_id': str(i * 3 + 5)
            })
        return render_template('food_table.html', data=retData)
    return render_template('attendant_food.html')

@app.route('/attendant/remove_food_promotion', methods=['POST'])
@login_required
def attendant_cancel_promotion():
    return json.dumps({
        'type': 'success',
        'str': json.dumps(request.form)
    })

@app.route('/ticket_staff/sale', methods=['GET', 'POST'])
@login_required
def ticket_staff_sale():
    if request.method == 'POST':
        if 'action' in request.form:
            if request.form['action'] == 'addWeight':
                return render_template('ticket_staff_sale.html', message={
                    'type': 'success',
                    'str': json.dumps(request.form)
                })
            if request.form['action'] == 'buyTicket':
                return json.dumps({
                    'type': 'success',
                    'str': json.dumps(request.form)
                })
        retData = []
        for i in range(10):
            retData.append({
                'pass_id': str(i + 10),
                'flight_id': str(i * 3 + 5),
                'price': str(i * 100)
            })
        return render_template('sale_table.html', data=retData)
    return render_template('ticket_staff_sale.html')

@app.route('/<user_type>/flight_promotions', methods=['GET', 'POST'])
@login_required
def ticket_staff_flight_promotions(user_type):
    if request.method == 'POST':
        if 'action' in request.form:
            if request.form['action'] == 'removePromotion':
                return json.dumps({
                    'type': 'success',
                    'str': json.dumps(request.form)
                })
        retData = []
        for i in range(10):
            retData.append({
                'pass_id': str(i + 10),
                'promotion_id': str(i * 3 + 5),
                'value': str(i * 100)
            })
        return render_template('ticket_staff_promotion_table.html', data=retData)
    return render_template('ticket_staff_flight_promotions.html')

@app.route('/ticket_staff/history', methods=['GET', 'POST'])
@login_required
def ticket_staff_history():
    if request.method == 'POST':
        retData = []
        for i in range(10):
            retData.append({
                "flight_id": str(i + 10),
                "date": "May {}, 2016".format(i),
                "departure": "03:{}".format(i),
                "eta": "{}:03".format(i),
                "from": 'ankara',
                "to": 'istanbul',
                "duration": str(i + 31),
            })
        return render_template('ticket_staff_history_table.html', data=retData)
    return render_template('ticket_staff_history.html')

@app.route('/admin/delay', methods=['GET', 'POST'])
@login_required
def admin_delay():
    if request.method == 'POST':
        db = get_db()
        status = 'success'
        message = 'Flight #{} succesfully delayed by {} minutes'.format(request.form['flight_id'], request.form['delay'])
        try:
            db.delay_flight(int(request.form['delay']), request.form['flight_id'])
        except mysql.connector.Error as err:
            status = 'warning'
            message = "Something went wrong: {}".format(err)
        return render_template('admin_delay.html', message = {
            'type': status,
            'str': message
        })
    return render_template('admin_delay.html')

@app.route('/admin/flight', methods=['GET', 'POST'])
@login_required
def admin_flight():
    if request.method == 'POST':
        db = get_db()
        status = 'success'
        message = 'Flight successfully added!'
        try:
            if request.form['action'] == 'add_flight':
                dateobj = datetime.datetime.strptime(request.form['date']+'/'+request.form['time'],'%m/%d/%Y/%I:%M%p')
                db.add_flight(dateobj, request.form['plane_id'], request.form['duration'],
                    request.form['econ_price'], request.form['buss_price'],
                    request.form['fromAirport'], request.form['fromCity'], request.form['fromCountry'],
                    request.form['toAirport'], request.form['toCity'], request.form['toCountry'],
                )
            else:
                db.remove_flight(request.form['flight_id'])
                message = 'Flight successfully removed!'
        except mysql.connector.Error as err:
            status = 'warning'
            message = "Something went wrong: {}".format(err)
        return render_template('admin_flight.html', message = {
            'type': status,
            'str': message
        })
    return render_template('admin_flight.html')

@app.route('/admin/crew', methods=['GET', 'POST'])
@login_required
def admin_crew():
    if request.method == 'POST':
        db = get_db()
        status = 'success'
        message = json.dumps(request.form)
        flight_id = request.form['flight_id']
        staff_id = request.form['staff_id']
        try:
            if db.get_user_type(staff_id) == 'pilot':
                message = "Pilot succesfully added!"
                db.assign_pilot_to_flight(staff_id, flight_id)
            else:
                message = "Attendant succesfully added!"
                db.assign_attendant_to_flight(staff_id, flight_id)
        except mysql.connector.Error as err:
            status = 'warning'
            message = "Something went wrong: {}".format(err)
            print err
        return render_template('admin_crew.html', message = {
            'type': status,
            'str': message
        })
    return render_template('admin_crew.html')

@app.route('/admin/account', methods=['GET', 'POST'])
@login_required
def admin_account():
    if request.method == 'POST':
        db = get_db()
        status = 'success'
        message = json.dumps(request.form)
        user_id = request.form['user_id']
        try:
            if request.form['action'] == 'assign_account':
                user_type = request.form['user_type']
                #TUM ASSIGNLAR BURAYA GELCEK
                message = 'User #{} succesfully assigned to {}!'.format(user_id, user_type)
            else:
                db.delete_account(user_id)
                message = 'User succesfully deleted!'
        except mysql.connector.Error as err:
            status = 'warning'
            message = "Something went wrong: {}".format(err)
            print err
        return render_template('admin_account.html', message = {
            'type': status,
            'str': message
        })
    return render_template('admin_account.html')

@app.route('/admin/scheduled', methods=['GET', 'POST'])
@login_required
def admin_scheduled():
    db = get_db()
    retData = db.display_all_flights()
    if request.method == 'POST':
        status = 'success'
        message = 'Flight is succesfully marked as landed!'
        try:
            db.land_flights(request.form['flight_id'])
        except mysql.connector.Error as err:
            status = 'warning'
            message = "Something went wrong: {}".format(err)
            print err
        return render_template('admin_scheduled.html', data=retData, message = {
            'type': status,
            'str': message
        })
    return render_template('admin_scheduled.html', data = retData)

@app.route('/logout')
@login_required
def logout():
    session.pop('id', None)
    session.pop('isloggedin', None)
    session.pop('user_type', None)
    return flask.redirect('/login')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3131, debug=True)
