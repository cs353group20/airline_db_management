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
    if session['user_type'] == 'passenger':
        return flask.redirect('/passenger/flights')
    if session['user_type'] == 'pilot':
        return flask.redirect('/attendant/current')
    if session['user_type'] == 'attendant':
        return flask.redirect('/attendant/current')
    if session['user_type'] == 'ticket_staff':
        return flask.redirect('/ticket_staff/sale')
    if session['user_type'] == 'store_staff':
        return flask.redirect('/store_staff/flight_promotions')
    if session['user_type'] == 'admin':
        return flask.redirect('/admin/delay')


@app.route('/passenger/buy', methods=['POST'])
@login_required
def buy_ticket():
    db = get_db();
    status = 'success'
    message = 'Ticket succesfully bought!'
    try:
        db.add_ticket(session['id'], request.form['flightID'], 22, request.form['seat_no'])
    except mysql.connector.Error as err:
        status = 'warning'
        message = 'Error: {}'.format(err)
    return render_template('passenger_flight.html', message={
        'type': status,
        'str': message
    })

@app.route('/passenger/menu', methods=['POST'])
@login_required
def get_menu():
    db = get_db()
    flightID = request.form['flightID']
    retData = db.display_menu_option(flightID)
    return render_template("menu_table.html", data=retData)

@app.route('/passenger/reserve', methods=['POST'])
@login_required
def reserver_ticket():
    db = get_db()
    flightID = request.form['flightID']
    userID = session['id']
    status = 'success'
    message = 'Ticket succesfully bought!'
    try:
        db.add_reservation(session['id'], request.form['flightID'])
    except mysql.connector.Error as err:
        status = 'warning'
        message = 'Error: {}'.format(err)
    return json.dumps({'type': status, 'str': message})

@app.route('/passenger/flights', methods=['GET', 'POST'])
@login_required
def passenger_flights():
    db = get_db()
    if request.method == 'POST':
        toStr = request.form['toInput']
        fromStr = request.form['fromInput']
        retData = db.display_direct_flights(toStr, fromStr)
        return render_template('flight_table.html', data=retData)
    airports = db.get_airports()
    return render_template('passenger_flight.html', airports = json.dumps(airports))

@app.route('/passenger/flight_history', methods=['GET', 'POST'])
@login_required
def passenger_history():
    db = get_db()
    retData = db.display_passenger_history(session['id'])
    print retData
    if request.method == 'POST':
        # FOR PASSED
        return json.dumps({'type': 'fee', 'fee': 300})
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
    db = get_db()
    retData = db.display_reservations(session['id'])
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
    db = get_db()
    if request.method == 'POST':
        retData = db.display_stores(request.form['storeName'])
        return render_template('store_table.html', data=retData)
    return render_template('passenger_store.html', airports = json.dumps(db.get_airports()))

@app.route('/profile', methods=['GET'])
@login_required
def profile_screen():
    db = get_db()
    retData = db.display_profile(session['id'])
    return render_template('profile.html', data=retData)

@app.route('/profile/<ty>', methods=['POST'])
@login_required
def change_profile_screen(ty):
    db = get_db()
    status = 'success'
    message = 'BANANE LAN'
    if ty == 'delete_account':
        flag = True
        try:
            db.delete_account(session['id'])
        except mysql.connector.Error as err:
            status = 'warning'
            flag = False
            message = 'Err: {}'.format(err)

        if flag:
            return flask.redirect('/logout')

    if ty == 'change_profile':
        message = 'Profile is successfully changed'
        if request.form['email'] != "":
            try:
                db.delete_email(session['id'])
                db.add_email(request.form['email'], session['id'])
            except mysql.connector.Error as err:
                status = 'warning'
                message = 'Err: {}'.format(err)
                print err
        if request.form['phone'] != "":
            try:
                db.delete_phone(session['id'])
                db.add_phone(request.form['phone'], session['id'])
            except mysql.connector.Error as err:
                status = 'warning'
                message = 'Err: {}'.format(err)
                print err
        if request.form['address'] != '':
            try:
                db.update_address(session['id'], request.form['address'])
            except mysql.connector.Error as err:
                status = 'warning'
                message = 'Err: {}'.format(err)
                print err

    if ty == 'change_password':
        old_pass = request.form['old_pass']
        new_pass = request.form['new_pass']
        aga_pass = request.form['new_pass_again']
        message = 'Password succesfully changed!'
        if new_pass != aga_pass:
            status = 'warning'
            message = 'New password does not match!'
        else:
            try:
                db.update_password(old_pass, new_pass, session['id'])
            except mysql.connector.Error as err:
                status = 'warning'
                message = 'Err: {}'.format(err)
                print err

    retData = db.display_profile(session['id'])
    return render_template('profile.html', data=retData, message={
        'type': status,
        'str': message
    })

@app.route('/attendant/current', methods=['GET', 'POST'])
@login_required
def attendant_current():
    db = get_db()
    if request.method == 'POST':
        flightID = request.form['flightID']
        retData = {}
        try:
            retData = db.display_plane_info(session['id'], flightID)
        except mysql.connector.Error as err:
            status = 'warning'
            message = 'Err: {}'.format(err)
            print err
        return render_template("plane_table.html", data = retData)
    if session['user_type'] == 'pilot':
        retData = db.browse_pilot_schedule(session['id'])
    else:
        retData = db.browse_att_schedule(session['id'])
    return render_template('attendant_current.html', data=retData)

@app.route('/attendant/flight_history')
@login_required
def attendant_history():
    db = get_db()
    retData = []
    try:
        retData = db.display_flight_pers_history(session['id'])
    except mysql.connector.Error as err:
        status = 'warning'
        message = 'Err: {}'.format(err)
        print err
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

@app.route('/admin/plane', methods=['GET', 'POST'])
@login_required
def admin_plane():
    if request.method == 'POST':
        db = get_db()
        status = 'success'
        message = 'Plane successfully added!'
        try:
            if request.form['action'] == 'add_plane':
                db.add_plane(request.form['model'], request.form['capacity'], request.form['range'], request.form['altitude'])
            else:
                db.remove_plane(request.form['plane_id'])
                message = 'Plane successfully removed!'
            #pass
        except mysql.connector.Error as err:
            status = 'warning'
            message = "Something went wrong: {}".format(err)
        print status, message
        return render_template('admin_plane.html', message = {
            'type': status,
            'str': message
        })
    return render_template('admin_plane.html')

@app.route('/admin/menu', methods=['GET', 'POST'])
@login_required
def admin_menu():
    if request.method == 'POST':
        db = get_db()
        status = 'success'
        message = 'Menu option successfully added!'
        try:
            if (request.form['action'] == 'add_food'):
                db.add_menu_option(request.form['flight_id'], request.form['name'], request.form['price'])
        except mysql.connector.Error as err:
            status = 'warning'
            message = "Something went wrong: {}".format(err)
        print status, message
        return render_template('admin_menu.html', message = {
            'type': status,
            'str': message
        })
    return render_template('admin_menu.html')

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
                if user_type == 'attendant':
                    db.assign_person_as_attendant(user_id)
                if user_type == 'pilot':
                    db.assign_person_as_pilot(user_id)
                if user_type == 'ticket_staff':
                    db.assign_person_as_ticket_staff(user_id)
                if user_type == 'store_staff':
                    db.assign_person_as_store_staff(user_id)
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
