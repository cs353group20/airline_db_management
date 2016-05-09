import mysql.connector
from mysql.connector.errors import Error
import datetime
import time

class database:
    def __init__(self, db):
        if db is None:
            raise("Error")
        self.db = db

    def close(self):
        self.db.close()

    def check_login(self, userid, password):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM person WHERE person_id='{}' and password='{}'".format(userid, password))
        data = cursor.fetchone()
        if data == None:
            return False
        return True

    def get_user_type(self, userid):
        cursor = self.db.cursor()
        if userid == 1:
            return "admin"

        cursor.execute("SELECT * FROM passenger WHERE pass_id='{}'".format(userid))
        data = cursor.fetchone()
        if data != None:
            return "passenger"

        cursor.execute("SELECT * FROM pilot WHERE pilot_id='{}'".format(userid))
        data = cursor.fetchone()
        if data != None:
            return "pilot"

        cursor.execute("SELECT * FROM flight_attendant WHERE att_id='{}'".format(userid))
        data = cursor.fetchone()
        if data != None:
            return "attendant"

        cursor.execute("SELECT * FROM store_staff WHERE store_staff_id='{}'".format(userid))
        data = cursor.fetchone()
        if data != None:
            return "store_staff"

        cursor.execute("SELECT * FROM ticket_staff WHERE ticket_staff_id='{}'".format(userid))
        data = cursor.fetchone()
        if data != None:
            return "ticket_staff"
        return "nan"

    def signup(self, name, password, no, street, town, city, phone, email):
        cursor = self.db.cursor()

        cursor.execute("INSERT INTO person(person_name, password, address_no, street, town, city) "
            " VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(name, password, no, street, town, city))
        cursor.execute("SELECT LAST_INSERT_ID()")
        data = cursor.fetchone()
        cursor.execute("INSERT INTO passenger(pass_id, expenditure, prom_expenditure)"
            " VALUES('{}', 0, 0)".format(data[0]))
        cursor.execute("INSERT INTO person_phone(person_id, phone)"
            " VALUES('{}', '{}')".format(data[0], phone))
        cursor.execute("INSERT INTO person_email(person_id, email)"
            " VALUES('{}', '{}')".format(data[0], email))
        self.db.commit()
        return data[0]

    def display_direct_flights(self, source, dest):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM flight AS F NATURAL JOIN flight_arrival"
        " WHERE EXISTS(SELECT city_name, country FROM airport AS A WHERE F.dep_airport_name = A.airport_name AND city_name "
        "LIKE CONCAT('%', '{}', '%'))"
        " AND EXISTS(SELECT city_name, country FROM airport AS A WHERE F.arr_airport_name = A.airport_name AND city_name "
        "LIKE CONCAT('%', '{}', '%'))"
        " ORDER BY F.flight_id".format(source, dest))
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'flight_id': row[0], 'date': row[1], 'plane_id': row[2], 'dep_airport_name': row[3],
                    'dep_city_name': row[4], 'dep_country': row[5], 'arr_airport_name': row[6], 'arr_city_name': row[7],
                    'arr_country': row[7], 'duration': row[8], 'econ_price': row[9], 'business_price': row[10],
                    'landed': row[11]}
            list.append(dict)
        return list

    def add_reservation(self, pass_id, flight_id, deadline, seat_no):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO reservation(pass_id, flight_id, deadline, seat_no)"
                   " VALUES('{}', '{}', '{}', '{}')".format(pass_id, flight_id, deadline, seat_no))
        self.db.commit()

    def add_ticket(self, pass_id, flight_id, staff_id):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO ticket(flight_id, pass_id, staff_id)"
                    " VALUES('{}', '{}', '{}')".format(flight_id, pass_id, staff_id))
        self.db.commit()

    def display_passenger_history(self, pass_id):
        cursor = self.db.cursor()
        create_pass_history_view()
        cursor.execute("SELECT * FROM pass_history_view")
        drop_pass_history_view()
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'flight_id': row[0], 'pass_id': row[1]}
            list.append(dict)
        return list

    def cancel_ticket(self, pass_id, flight_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM ticket WHERE pass_id = '{}' AND flight_id = '{}'".format(pass_id, flight_id))
        db.commit()

    def display_reservations(self, pass_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM reservation WHERE pass_id = '{}'".format(pass_id))
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'flight_id': row[0], 'pass_id': row[1], 'deadline': row[2], 'seat_no': row[3]}
            list.append(dict)
        return list

    def cancel_reservation(self, pass_id, flight_id, seat_no):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM reservation WHERE pass_id = '{}' AND flight_id = '{}' AND seat_no = '{}'".format(pass_id, flight_id, seat_no))
        self.db.commit()

    def display_stores(self, airport_name):
        cursor = self.db.cursor()
        cursor.execute("SELECT store_id, store_name, owner FROM store NATURAL JOIN airport "
                   "WHERE airport_name LIKE CONCAT('%', '{}', '%')".format(airport_name))
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'store_id': row[0], 'store_name': row[1], 'owner': row[2]}
            list.append(dict)
        return list

    def display_menu_option(self, flight_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT option_id, option_name "
                   "FROM menu_option WHERE flight_id = '{}'".format(flight_id))
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'option_id': row[0], 'option_name': row[1]}
            list.append(dict)
        return list

    def display_profile(self, person_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM person WHERE person_id = '{}'".format(person_id))
        data = cursor.fetchone()
        dict = {'person_id': data[0], 'password': data[1], 'person_name': data[2], 'address_no': data[3],
                'street': data[4], 'town': data[5], 'city': data[6]}
        return dict

    def update_password(self, old, new, person_id):
        cursor = self.db.cursor()
        cursor.execute("SET person UPDATE password = '{}' WHERE password = '{}' "
                   "person_id = '{}'".format(new, old, person_id))
        self.db.commit()

    def delete_phone(self, phone, person_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FR0M person_phone WHERE person_id = '{}' AND "
                   "phone = '{}'".format(person_id, phone))
        self.db.commit()

    def add_phone(self, phone, person_id):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO person_phone VALUES('{}', '{}')".format(person_id, phone))
        self.db.commit()

    def delete_email(self, email, person_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FR0M person_email WHERE person_id = '{}' AND "
                   "email = '{}'".format(person_id, email))
        self.db.commit()

    def add_email(self, email, person_id):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO person_email VALUES('{}', '{}')".format(person_id, email))
        self.db.commit()

    def delete_account(self, person_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM person WHERE person_id = '{}'".format(person_id))
        if cursor.rowcount == 0:
            raise Error("User not found!")
        self.db.commit()

    def browse_pilot_schudule(self, pilot_id):
        cursor = self.db.cursor()
        create_pilot_schedule_view(self, pilot_id)
        cursor.execute("SELECT * FROM pilot_schedule")
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'flight_id': row[0], 'date': row[1], 'plane_id': row[2], 'dep_airport_name': row[3],
                    'dep_city_name': row[4], 'dep_country': row[5], 'arr_airport_name': row[6], 'arr_city_name': row[7],
                    'arr_country': row[7], 'duration': row[8], 'econ_price': row[9], 'business_price': row[10],
                    'landed': row[11]}
            list.append(dict)
        drop_pilot_schedule_view(self)
        return list

    def browse_att_schudule(self, att_id):
        cursor = self.db.cursor()
        create_att_schedule_view(self, att_id)
        cursor.execute("SELECT * FROM att_schedule")
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'flight_id': row[0], 'date': row[1], 'plane_id': row[2], 'dep_airport_name': row[3],
                    'dep_city_name': row[4], 'dep_country': row[5], 'arr_airport_name': row[6], 'arr_city_name': row[7],
                    'arr_country': row[7], 'duration': row[8], 'econ_price': row[9], 'business_price': row[10],
                    'landed': row[11]}
            list.append(dict)
        drop_att_schedule_view(self)
        return list

    def display_plane_info(self, pilot_id):
        cursor = self.db.cursor()
        create_plane_view(self, pilot_id)
        cursor.execute("SELECT * FROM plane_view")
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'plane_id': row[0], 'model': row[1], 'capacity': row[2], 'plane_range': row[3], 'altitude': row[4]}
            list.append(dict)
        drop_plane_view(self)
        return list

    def display_flight_pers_history(self, flight_pers_id):
        cursor = self.db.cursor()
        create_pers_history_view(self, flight_pers_id)
        cursor.execute("SELECT * FROM pers_history_view")
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'flight_pers_id': row[0], 'flight': row[1]}
            list.append(dict)
        drop_pers_history_view()
        return list

    def display_food_promotion(self, pass_id):
        cursor = self.db.cursor()
        create_food_promotion_view()
        cursor.execute("SELECT * FROM food_promotion_view WHERE pass_id = '{}'".format(pass_id))
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'pass_id': row[0], 'prom_id': row[1], 'food_type': row[2]}
            list.append(dict)
        drop_food_promotion_view()
        return list

    def record_usage_of_food_prom(self, att_id, prom_id):
        cursor = self.db.cursor()
        create_food_promotion_view(self, att_id)
        cursor.execute("DELETE FROM food_promotion_view WHERE prom_id = '{}'".format(prom_id))
        drop_food_promotion_view(self)
        self.db.commit()

    def record_ticket_sales(self, flight_id, pass_id, ticket_id, staff_id, luggage):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO ticket VALUES('{}', "
                       "'{}', '{}', '{}', '{}')'".format(ticket_id, flight_id, pass_id, staff_id, luggage))
        self.db.commit()

    def update_luggage_weight(self, luggage, ticket_id):
        cursor = self.db.cursor()
        cursor.execute("UPDATE ticket SET luggage = '{}' WHERE ticket_id = '{}'".format(luggage, ticket_id))
        self.db.commit()

    def display_flight_prom(self, pass_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM flight_promotion WHERE pass_id = '{}'".format(pass_id))
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'pass_id': row[0], 'prom_id': row[1], 'domestic': row[2]}
            list.append(dict)
        drop_food_promotion_view()
        return list

    def record_usage_of_flight_prom(self, prom_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM flight_promotion WHERE prom_id = '{}'".format(prom_id))
        self.db.commit()

    def add_flight(self, date, plane_id, duration, econ_price, business_price, dep_airport_name,
                    dep_city_name, dep_country, arr_airport_name, arr_city_name, arr_country):
        cursor = self.db.cursor()
        print """INSERT INTO flight VALUES(default, '{}', '{}',
                       '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
                       0)""".format(date, plane_id, dep_airport_name, dep_city_name,
                       dep_country, arr_airport_name, arr_city_name, arr_country, duration, econ_price,
                       business_price)
        cursor.execute("""INSERT INTO flight VALUES(default, '{}', '{}',
                       '{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
                       0)""".format(date, plane_id, dep_airport_name, dep_city_name,
                       dep_country, arr_airport_name, arr_city_name, arr_country, duration, econ_price,
                       business_price))
        self.db.commit()
        arrival = date + datetime.timedelta(seconds=delay*60)
        cursor.execute("INSERT INTO flight_arrival VALUES('{}', '{}', '{}')"
                       " WHERE NOT EXISTS(SELECT * FROM flight_arrival WHERE "
                       "date = '{}' AND duration = '{}')".format(date, duration, arrival, date, duration))
        self.db.commit()

    def remove_flight(self, flight_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM flight WHERE flight_id = '{}'".format(flight_id))
        if cursor.rowcount == 0:
            raise Error('Flight not found!')
        self.db.commit()

    def add_plane(self, plane_id, model, capacity, plane_range, altitude):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO plane VALUES('{}', '{}')".format(plane_id, model))
        self.db.commit()
        cursor.execute("INSERT INTO plane_model VALUES('{}', '{}', '{}',"
                       "'{}') WHERE NOT EXISTS(SELECT * FROM plane_model WHERE model = "
                       "'{}')".format(model, capacity, plane_range, altitude, model))
        self.db.commit()

    def remove_plane(self, plane_id):
        cursor = self.db.cursor()
        cursor.execute("WITH a_model(model) AS (SELECT model FROM plane WHERE plane_id = '{}') "
                       "DELETE FROM plane_model WHERE (SELECT CNT(*) FROM plane WHERE model = a_model.model) = 1 AND "
                       "model = a_model.model".format(plane_id))
        self.db.commit()
        cursor.execute("DELETE FROM plane WHERE plane_id = '{}'".format(plane_id))
        self.db.commit()

    def delay_flight(self, delay, flight_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT date FROM flight WHERE flight_id = '{}'".format(flight_id))
        date = cursor.fetchone()
        if date is None:
            raise Error('Flight not found!')
        new_date = date[0] + datetime.timedelta(seconds=delay*60)
        cursor.execute("UPDATE flight SET date = '{}' WHERE flight_id = '{}'".format(new_date, flight_id))
        self.db.commit()

    def assign_attendant_to_flight(self, att_id, flight_id):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO flight_att VALUES('{}', '{}')".format(flight_id, att_id))
        self.db.commit()

    def assign_pilot_to_flight(self, pilot_id, flight_id):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO flight_pilot VALUES('{}', '{}')".format(flight_id, pilot_id))
        self.db.commit()

    def add_menu_option(self, flight_id, option_id, option_name, price):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO menu_option VALUES('{}', '{}', '{}', "
                       "'{}')".format(flight_id, option_id, option_name, price))
        self.db.commit()

    def remove_menu_option(self, flight_id, option_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM menu_option WHERE flight_id = '{}' "
                       "AND option_id = '{}'".format(flight_id, option_id))
        self.db.commit()

    def add_store(self, store_id, store_name, owner):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO store VALUES('{}', '{}', '{}')"
                       "".format(store_id, store_name, owner))
        self.db.commit()

    def remove_store(self, store_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM store WHERE store_id = '{}'".format(store_id))
        self.db.commit()

    def assign_person_as_passenger(self, person_id):
        delete_account(self, person_id)
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO passenger VALUES('{}', 0, 0)".format(person_id))
        self.db.commit()

    def assign_person_as_attendant(self, person_id, salary, start_date, duty):
        delete_account(self, person_id)
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO flight_attendant VALUES('{}', 0, 0)".format(person_id, salary, start_date, duty))
        self.db.commit()

    def assign_person_as_pilot(self, person_id, salary, start_date, rank, certificate_type):
        delete_account(self, person_id)
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO pilot VALUES('{}', '{}', '{}', '{}', '{}')".format(person_id,
                        salary, start_date, rank, certificate_type))
        self.db.commit()

    def assign_person_as_ticket_staff(self, person_id, salary, start_date):
        delete_account(self, person_id)
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO ticket_staff VALUES('{}', '{}', '{}', 0)".format(person_id,
                        salary, start_date))
        self.db.commit()

    def assign_person_as_store_staff(self, person_id, salary, start_date):
        delete_account(self, person_id)
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO store_staff VALUES('{}', '{}', '{}', 0)".format(person_id,
                        salary, start_date))
        self.db.commit()

    def display_all_flights(self):
        cursor = self.db.cursor()
        cursor.execute("""SELECT flight_id, date, arrival, duration, arr_city_name, arr_country
                       FROM flight NATURAL JOIN flight_arrival WHERE landed = 0 ORDER BY flight_id""")
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'flight_id': row[0], 'date': row[1], 'arrival': row[2], 'duration': row[3],
                    'arr_city_name': row[4], 'arr_country_name': row[5]}
            list.append(dict)
        return list

    def land_flights(self, flight_id):
        cursor = self.db.cursor()
        cursor.execute("UPDATE flight SET landed = 1 WHERE flight_id = '{}'".format(flight_id))
        self.db.commit()

    def create_pass_history_view(self, pass_id):
        cursor = self.db.cursor()
        cursor.execute("CREATE VIEW pass_history_view AS"
                   " SELECT * FROM pass_history WHERE pass_id = '{}'".format(pass_id))

    def drop_pass_history_view(self):
        cursor = self.db.cursor()
        cursor.execute("DROP VIEW pass_history_view")

    def create_pilot_schedule_view(self, pilot_id):
        cursor = self.db.cursor()
        cursor.execute("CREATE VIEW pilot_schedule AS SELECT * FROM flight WHERE flight_id IN (SELECT flight_id FROM "
                        "flight_pilot WHERE pilot_id = '{}')".format(pilot_id))

    def drop_pilot_schedule_view(self):
        cursor = self.db.cursor()
        cursor.execute("DROP VIEW pilot_schedule")

    def create_att_schedule_view(self, att_id):
        cursor = self.db.cursor()
        cursor.execute("CREATE VIEW att_schedule AS SELECT * FROM flight WHERE flight_id IN (SELECT flight_id FROM "
                        "flight_att WHERE att_id = '{}')".format(att_id))

    def drop_att_schedule_view(self):
        cursor = self.db.cursor()
        cursor.execute("DROP VIEW att_schedule")

    def create_plane_view(self, pilot_id):
        cursor = self.db.cursor()
        cursor.execute("CREATE VIEW plane_view AS SELECT * FROM plane NATURAL JOIN plane_model WHERE plane_id IN (SELECT plane_id FROM "
                        "flight WHERE flight_id IN (SELECT flight_id FROM flight_pilot WHERE pilot_id = '{}'))".format(pilot_id))

    def drop_plane_view(self):
        cursor = self.db.cursor()
        cursor.execute("DROP VIEW plane_view")

    def create_food_promotion_view(self, att_id):
        cursor = self.db.cursor()
        cursor.execute("CREATE VIEW food_promotion_view AS "
                       "SELECT * FROM food_promotion WHERE "
                       "pass_id IN (SELECT pass_id FROM ticket "
                       "WHERE flight_id IN (SELECT flight_id "
                       "FROM flight_att WHERE att_id = '{}'".format(att_id))

    def create_flight_promotion_view(self, store_staff_id):
        cursor = self.db.cursor()
        cursor.execute("CREATE VIEW ")

    def drop_flight_promotion_view(self):
        cursor = self.db.cursor()
        cursor.execute("DROP VIEW flight_promotion_view")

    def create_pers_history_view(self, flight_pers_id):
        cursor = self.db.cursor()
        cursor.execute("CREATE VIEW pers_history_view AS SELECT * FROM pers_history "
                        "WHERE flight_pers_id = '{}'".format(flight_pers_id))

    def drop_pers_history_view(self):
        cursor = self.db.cursor()
        cursor.execute("DROP VIEW pers_history_view")

    def sale_report(self):
        cursor = self.db.cursor()
        cursor.execute("select pass_id, person_name, count(*) as ticket_count, sum(price) as total_price "
                       "from ticket natural join (passenger join person on pass_id = person_id)"
                       "group by pass_id")
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'pass_id': row[0], 'pass_name': row[1], 'ticket_count': row[2], 'total_price': row[3]}
            list.append(dict)
        return list

    def att_report(self):
        cursor = self.db.cursor()
        cursor.execute("select flight_id, count(att_id) as att_count "
                       "from flight_att natural join flight "
                       "group by flight_id")
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'flight_id': row[0], 'no_of_att': row[1]}
            list.append(dict)
        return list

    def pilot_report(self):
        cursor = self.db.cursor()
        cursor.execute("select flight_id, count(pilot_id) as pilot_count "
                       "from flight_pilot natural join flight "
                       "group by flight_id")
        data = cursor.fetchall()
        list = []
        for row in data:
            dict = {'flight_id': row[0], 'no_of_pilot': row[1]}
            list.append(dict)
        return list

    def get_pass(self, pass_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM passenger WHERE pass_id = '{}'".format(pass_id))
        return cursor.fetchone()

if __name__ == "__main__":
    db = mysql.connector.connect(user="root", passwd="omer")
    try:
        db.database = "airline_company"
    except mysql.connector.Error as err:
        pass
    db = database(db)

    ###### TEST CODE GOES HERE
    print(db.display_direct_flights('ankara', 'istanbul'))
