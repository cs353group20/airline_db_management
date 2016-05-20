import mysql.connector
from mysql.connector import errorcode

conn = mysql.connector.connect(user= "root", passwd= "omer")
cursor = conn.cursor(buffered=True)

DB_NAME = 'airline_company'

cursor.execute( "DROP DATABASE IF EXISTS airline_company")

try:
    cursor.execute( "CREATE DATABASE if not exists airline_company ")
except mysql.connector.Error as err:
    print('Failed creating database: {}'.format(err))
    exit(1)

try:
    conn.database = DB_NAME
except mysql.connector.Error as err:
    if (err.errno == errorcode.ER_BAD_DB_ERROR):
        create_database(cursor)
        conn.database = DB_NAME
    else:
        print(err)
        exit(1)

# Create tables
tables = []
tables.append(
     "CREATE TABLE person(  "
     "person_id int PRIMARY KEY AUTO_INCREMENT,  "
     "password varchar(40) NOT NULL,  "
     "person_name varchar(40) NOT NULL,  "
     "address_no int,  "
     "street varchar(40),  "
     "town varchar(40), "
     "city varchar(40)"
     ") ENGINE=InnoDB ")

tables.append(
     "CREATE TABLE person_phone(  "
     "person_id int,  "
     "phone varchar(20),  "
     "PRIMARY KEY(person_id, phone),  "
     "FOREIGN KEY(person_id) references person(person_id)  "
     "ON DELETE CASCADE) ENGINE=InnoDB ")

tables.append(
     "CREATE TABLE person_email(  "
     "person_id int,  "
     "email varchar(40),  "
     "PRIMARY KEY(person_id, email),  "
     "FOREIGN KEY(person_id) references person(person_id)  "
     "ON DELETE CASCADE) ENGINE=InnoDB ")

tables.append(
     "CREATE TABLE city(  "
     "city_name varchar(40),  "
     "country varchar(40),  "
     "latitude numeric(8,5) NOT NULL,  "
     "longitude numeric(8,5) NOT NULL,  "
     "PRIMARY KEY(city_name, country),  "
     "check(latitude >= 0 and latitude < 360 and  "
     "longitude >= 0 and longitude < 180)) ENGINE=InnoDB ")

tables.append(
     "CREATE TABLE airport(  "
     "airport_name varchar(40),  "
     "city_name varchar(40),  "
     "country varchar(40), "
     "PRIMARY KEY(airport_name, city_name, country), "
     "FOREIGN KEY (city_name, country) references city(city_name, country)  "
     "on delete cascade) ENGINE=InnoDB ")

tables.append(
     "CREATE TABLE store( "
     "store_id int PRIMARY KEY AUTO_INCREMENT, "
     "store_name varchar(40) NOT NULL, "
     "owner varchar(40), "
     "airport_name varchar(40), "
     "city_name varchar(40), "
     "country varchar(40), "
     "FOREIGN KEY (airport_name, city_name, country) references  "
     "airport(airport_name, city_name, country)  "
     "on delete cascade) ENGINE=InnoDB ")

tables.append(
     "CREATE TABLE passenger ( "
     "pass_id int PRIMARY KEY, "
     "expenditure int NOT NULL, "
     "prom_expenditure int NOT NULL, "
     "FOREIGN KEY(pass_id) references person(person_id)  "
     "on delete cascade) ENGINE=InnoDB ")

tables.append(
     "CREATE TABLE staff ( "
     "staff_id int PRIMARY KEY, "
     "salary numeric(12,2) NOT NULL, "
     "FOREIGN KEY(staff_id) references person(person_id)  "
     "on delete cascade) ENGINE=InnoDB ")

tables.append(
     "CREATE TABLE flight_personnel ( "
     "flight_pers_id int PRIMARY KEY, "
     "experience int NOT NULL, "
     "FOREIGN KEY(flight_pers_id) references staff(staff_id)  "
     "on delete cascade) ENGINE=InnoDB ")

tables.append(
     "CREATE TABLE pilot ( "
     "pilot_id int PRIMARY KEY, "
     "rank int NOT NULL, "
     "certificate_type enum('sport', 'recreational', 'private', 'commercial', "
     "'instructor', 'airline transport') NOT NULL, "
     "FOREIGN KEY(pilot_id) references flight_personnel(flight_pers_id)  "
     "on delete cascade) ENGINE=InnoDB ")

tables.append(
     "CREATE TABLE flight_attendant ( "
     "att_id int PRIMARY KEY, "
     "duty varchar(40) NOT NULL, "
     "FOREIGN KEY(att_id) references flight_personnel(flight_pers_id)  "
     "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE ticket_staff ( "
		 "ticket_staff_id int PRIMARY KEY, "
		 "ticket_count int NOT NULL, "
		 "FOREIGN KEY(ticket_staff_id) references staff(staff_id)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE store_staff ( "
		 "store_staff_id int PRIMARY KEY, "
		 "sale_count int NOT NULL, "
		 "store_id int NOT NULL, "
		 "FOREIGN KEY(store_staff_id) references staff(staff_id)  "
                 "on delete cascade, "
		 "FOREIGN KEY(store_id) references store(store_id)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE promotion ( "
		 "pass_id int, "
		 "prom_id int AUTO_INCREMENT, "
		 "amount int NOT NULL, "
		 "PRIMARY KEY(prom_id), "
                 "UNIQUE KEY(amount), "
		 "FOREIGN KEY(pass_id) references passenger(pass_id)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE store_promotion ( "
		 "pass_id int, "
		 "prom_id int, "
		 "product_type enum('alcohol', 'normal') NOT NULL, "
		 "PRIMARY KEY(pass_id, prom_id), "
		 "FOREIGN KEY(pass_id, prom_id) references promotion(pass_id, prom_id)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE food_promotion ( "
		 "pass_id int, "
		 "prom_id int, "
		 "food_type enum('meal', 'drink') NOT NULL, "
		 "PRIMARY KEY(pass_id, prom_id), "
		 "FOREIGN KEY(pass_id, prom_id) references promotion(pass_id, prom_id)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE flight_promotion ( "
		 "pass_id int, "
		 "prom_id int, "
		 "domestic binary NOT NULL, "
		 "PRIMARY KEY(pass_id, prom_id), "
		 "FOREIGN KEY(pass_id, prom_id) references promotion(pass_id, prom_id)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
                 "CREATE TABLE promotion_deadline( "
		 "amount int, "
		 "deadline date, "
		 "PRIMARY KEY(amount, deadline), "
		 "FOREIGN KEY(amount) references promotion(amount)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE plane_model( "
                 "model varchar(20) PRIMARY KEY UNIQUE, "
		 "capacity int, "
                 "plane_range numeric(7,2), "
                 "altitude numeric(5,2)) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE plane( "
		 "plane_id int PRIMARY KEY AUTO_INCREMENT, "
		 "model varchar(20) NOT NULL,"
                 "FOREIGN KEY(model) references plane_model(model) "
                 "on delete cascade)"
                 "ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE flight ( "
		 "flight_id int PRIMARY KEY AUTO_INCREMENT, "
		 "date DATETIME NOT NULL, "
                 "duration numeric(5,2),"
                 "arrival DATETIME,"
		 "plane_id int, "
		 "dep_airport_name varchar(40), "
		 "dep_city_name varchar(40), "
		 "dep_country varchar(40), "
		 "arr_airport_name varchar(40), "
		 "arr_city_name varchar(40), "
		 "arr_country varchar(40), "
                 "econ_price numeric(6,2), "
		 "business_price numeric(6,2), "
		 "landed binary NOT NULL, "
		 "FOREIGN KEY(plane_id) references plane(plane_id)  "
                 "on delete cascade, "
		 "FOREIGN KEY(dep_airport_name, dep_city_name, dep_country) references  "
		 "airport(airport_name, city_name, country)  "
                 "on delete cascade, "
		 "FOREIGN KEY(arr_airport_name, arr_city_name, arr_country) references  "
		 "airport(airport_name, city_name, country)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE seat ( "
		 "flight_id int, "
		 "no int, "
		 "class enum('econ', 'business') NOT NULL, "
		 "PRIMARY KEY (flight_id, no), "
		 "FOREIGN KEY (flight_id) references flight(flight_id)  "
                 "on delete cascade) ENGINE=InnoDB ")
tables.append(
		 "CREATE TABLE menu_option( "
		 "flight_id int, "
                 "option_id int AUTO_INCREMENT, "
		 "option_name varchar(40) NOT NULL, "
                 "price numeric(3,1), "
		 "PRIMARY KEY (option_id), "
		 "FOREIGN KEY (flight_id) references flight(flight_id)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE reservation( "
		 "flight_id int, "
		 "pass_id int, "
		 "deadline date NOT NULL, "
		 "seat_no int, "
		 "PRIMARY KEY(flight_id, pass_id, seat_no), "
		 "FOREIGN KEY(pass_id) references passenger(pass_id)  "
                 "on delete cascade, "
		 "FOREIGN KEY(flight_id, seat_no) references seat(flight_id, no)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE pass_history ( "
		 "flight_id int, "
		 "pass_id int, "
		 "PRIMARY KEY(flight_id, pass_id), "
		 "FOREIGN KEY(flight_id) references flight(flight_id)  "
                 "on delete cascade, "
		 "FOREIGN KEY(pass_id) references passenger(pass_id)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE pers_history( "
		 "flight_id int, "
		 "flight_pers_id int, "
		 "PRIMARY KEY(flight_id, flight_pers_id), "
		 "FOREIGN KEY(flight_id) references flight(flight_id)  "
                 "on delete cascade, "
		 "FOREIGN KEY(flight_pers_id) references flight_personnel(flight_pers_id)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE flight_pilot ( "
		 "flight_id int, "
		 "pilot_id int, "
		 "PRIMARY KEY(flight_id, pilot_id), "
		 "FOREIGN KEY(flight_id) references flight(flight_id)  "
                 "on delete cascade, "
		 "FOREIGN KEY(pilot_id) references pilot(pilot_id)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE flight_att( "
		 "flight_id int, "
		 "att_id int, "
		 "PRIMARY KEY(flight_id, att_id), "
		 "FOREIGN KEY(flight_id) references flight(flight_id)  "
                 "on delete cascade, "
		 "FOREIGN KEY(att_id) references flight_attendant(att_id)  "
                 "on delete cascade) ENGINE=InnoDB ")

tables.append(
		 "CREATE TABLE ticket( "
		 "ticket_id int AUTO_INCREMENT, "
		 "flight_id int, "
		 "pass_id int, "
		 "staff_id int, "
                 "seat_no int, "
		 "luggage int NOT NULL, "
                 "price numeric(6,2), "
		 "PRIMARY KEY(ticket_id), "
#		 "FOREIGN KEY(flight_id, pass_id, seat_no) references reservation(flight_id, pass_id, seat_no)  "
#                 "on delete cascade, "
		 "FOREIGN KEY(staff_id) references ticket_staff(ticket_staff_id)  "
                 "on delete cascade) ENGINE=InnoDB ")

for sql in tables:
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print( "already exists. ")
        else:
            print(err.msg)
    else:
        pass



try:
    cursor.execute( "create view professional_pilot as select * from pilot  "
                        "where rank > 10 and certificate_type = 'airline transport' ")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print( "already exists. ")
    else:
        print(err.msg)

data = []
data.append(
        #passengers 1-11
         "insert into person "
         "(password, person_name, address_no, street, town) "
         "values('omer', 'omer', 789, 'ceviz', 'chinatown'); ")
data.append(

         "insert into person "
         "(password, person_name, address_no, street, town) "
         "values('kaan', 'kaan', 456, 'kestane', 'venezullatown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('irem', 'irem', 123, 'palamut', 'brasiltown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('eren', 'eren', 666, 'cinar', 'hightown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('adam', 'adam', 789, 'ceviz', 'chinatown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('Max', 'max', 456, 'kestane', 'venezullatown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('madam', 'madam', 444, '444sokak', 'bankatown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('franky', 'franky', 666, 'cinar', 'helltown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('gumball watterson', 'gumball', 9999, 'imaginaryStreet', 'elmoretown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('kamina', 'kamina', 9001, 'garstreet', 'kmntown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('gin', 'gin', 23, 'parkstreet', 'kabuki'); ")
data.append(
        #staff 12-15
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('Roy Mustang', 'roy', 23, 'kingstreet', 'kingtown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('Alphonse', 'alphonse', 15, 'islandstreet', 'Resembool'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('Slark Kent', 'slark', 23, 'nightstreet', 'diretown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('Puck Norris', 'puck', 354, 'lightstreet', 'radiantstreet'); ")
data.append(
        #crew 16-25
        #16-20
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('Jackie Lmao', 'jacky', 12321, 'parkstreet', 'elmoretown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('Arteezy Babaev', 'arteezy', 9765, 'parkstreet', 'sellouttown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('Skrillex', 'skrillex', 123333, 'parkstreet', 'arttown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('Michael Jordan', 'jordan', 23, 'parkstreet', 'chicagotown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('Dante', 'dante', 543, 'garstreet', 'helltown'); ")
data.append(
        #pilots 21-25
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('batman', 'batman', 23, 'batstreet', 'batcavetown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('superman', 'superman', 23123, 'JLstreet', 'ktyptown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('hulk', 'hulk', 888, 'carnivalst', 'riostreet'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('emett', 'emett', 1234, 'ordinarystreet', 'ordinarytown'); ")
data.append(
         "insert into person "
         "(password, person_name, address_no, street, town)  "
         "values('Gandalf', 'Gandalf', 123123, 'lightstreet', 'radiantstreet'); ")

data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(1,'55544499'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(2,'1231231'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(3,'22222321'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(4,'50505058'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(5,'33333333'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(6,'89875263'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(7,'12461113'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(8,'82228222'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(9,'8552541'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(10,'3248555528'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(11,'+90879541'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(12,'3452123'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(13,'2346234'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(14,'2346546'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(15,'5684354'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(16,'67854234'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(17,'6787452'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(18,'3234238'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(19,'32443634628'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(20,'3248523423'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(21,'32342328'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(22,'324345438'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(23,'324568'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(24,'32423428'); ")
data.append(
         "insert into person_phone "
         "(person_id, phone)  "
         "values(25,'32456465528'); "
)

data.append(
         "insert into person_email "
         "(person_id, email)  "
         "values(1,'omer@data.com'); ")
data.append(
         "insert into person_email "
         "(person_id, email)  "
         "values(2,'kaan@data.com'); ")
data.append(
         "insert into person_email "
         "(person_id, email)  "
         "values(3,'irem@data.com'); ")
data.append(
         "insert into person_email "
         "(person_id, email)  "
         "values(4,'eren@data.com'); ")
data.append(
         "insert into person_email "
         "(person_id, email)  "
         "values(5,'adam@data.com'); ")
data.append(
         "insert into person_email "
         "(person_id, email)  "
         "values(6,'max@data.com'); ")
data.append(
         "insert into person_email "
         "(person_id, email)  "
         "values(7,'madam@data.com'); ")
data.append(
         "insert into person_email "
         "(person_id, email)  "
         "values(8,'franky@data.com'); ")
data.append(
         "insert into person_email "
         "(person_id, email)  "
         "values(9,'gumball@data.com'); ")
data.append(
         "insert into person_email "
         "(person_id, email)  "
         "values(10,'kamina@data.com'); ")
data.append(
         "insert into person_email "
         "(person_id, email)  "
         "values(11,'gin@data.com'); ")
data.append(
         "insert into person_email "
         "(person_id, email)  "
         "values(12, 'roy@data.com'); ")
data.append(
         "insert into person_email "
         "(person_id, email)  "
         "values(13, 'alphonse@data.com'); ")
data.append(
        "insert into person_email "
         "(person_id, email)  "
         "values(14, 'slark@data.com'); ")
data.append(
        "insert into person_email "
         "(person_id, email)  "
         "values(15, 'puck@data.com'); ")
data.append(
        "insert into person_email "
         "(person_id, email)  "
         "values(16, 'jacky@data.com'); ")
data.append(
        "insert into person_email "
         "(person_id, email)  "
         "values(17, 'arteezy@data.com'); ")
data.append(
        "insert into person_email "
         "(person_id, email)  "
         "values(18, 'skrillex@data.com'); ")
data.append(
        "insert into person_email "
         "(person_id, email)  "
         "values(19, 'jordan@data.com'); ")
data.append(
        "insert into person_email "
         "(person_id, email)  "
         "values(20, 'dante@data.com'); ")
data.append(
        "insert into person_email "
         "(person_id, email)  "
         "values(21, 'batman@data.com'); ")
data.append(
        "insert into person_email "
         "(person_id, email)  "
         "values(22, 'superman@data.com'); ")
data.append(
        "insert into person_email "
         "(person_id, email)  "
         "values(23, 'hulk@data.com'); ")
data.append(
        "insert into person_email "
         "(person_id, email)  "
         "values(24, 'emett@data.com'); ")
data.append(
        "insert into person_email "
         "(person_id, email)  "
         "values(25, 'gandalf@data.com'); "
)

data.append(
         "insert into city "
         "(city_name, country, latitude, longitude)  "
         "values('Cape Town', 'South Africa', -33.92, 18.42) ")
data.append(
         "insert into city "
         "(city_name, country, latitude, longitude)  "
         "values('Ankara', 'Turkey', 39.9334, 32.8597) " )
data.append(
         "insert into city "
         "(city_name, country, latitude, longitude)  "
         "values('Istanbul', 'Turkey', 41.0082, 28.9784) " )
data.append(
         "insert into city "
         "(city_name, country, latitude, longitude)  "
         "values('New York', 'United States', 40.7128, -74.0059) ")
data.append(
         "insert into city "
         "(city_name, country, latitude, longitude)  "
         "values('Tokyo', 'Japan', 35.6895, 139.6917) " )
data.append(
         "insert into city "
         "(city_name, country, latitude, longitude)  "
         "values('Beijing', 'China', 39.9042, 116.4074) " )
data.append(
         "insert into city "
         "(city_name, country, latitude, longitude) "
         "values('London', 'England', 51.5074, 0.1278) " )
data.append(
         "insert into city "
         "(city_name, country, latitude, longitude)  "
         "values('Cairo', 'Egypt', 30.0444, 31.2357) "
)

data.append(
         "insert into airport "
         "(airport_name, city_name, country) "
         "values('Istanbul Ataturk Airport', 'Istanbul', 'Turkey') " )
data.append(
         "insert into airport "
         "(airport_name, city_name, country) "
         "values('Sabiha Gokcen International Airport', 'Istanbul', 'Turkey') ")
data.append(
         "insert into airport "
         "(airport_name, city_name, country)"
         "values('Ankara Esenboga Airport', 'Ankara', 'Turkey') ")
data.append(
         "insert into airport "
         "(airport_name, city_name, country)  "
         "values('John F. Kennedy International Airport', 'New York', 'United States') ")
data.append(
         "insert into airport "
         "(airport_name, city_name, country)  "
         "values('LaGuardia Airport', 'New York', 'United States') ")
data.append(
         "insert into airport "
         "(airport_name, city_name, country)  "
         "values('Cairo International Airport', 'Cairo', 'Egypt') " )
data.append(
         "insert into airport "
         "(airport_name, city_name, country) "
         "values('London City Airport', 'London', 'England') ")
data.append(
         "insert into airport "
         "(airport_name, city_name, country)  "
         "values('Heathrow Airport', 'London', 'England') ")
data.append(
         "insert into airport "
         "(airport_name, city_name, country)  "
         "values('Haneda Airport', 'Tokyo', 'Japan') " )
data.append(
         "insert into airport "
         "(airport_name, city_name, country)  "
         "values('Narita International Airport', 'Tokyo', 'Japan') ")
data.append(
         "insert into airport "
         "(airport_name, city_name, country)  "
         "values('Beijing Capital International Airport', 'Beijing', 'China') " )
data.append(
         "insert into airport "
         "(airport_name, city_name, country)  "
         "values('Beijing Nanyuan Airport', 'Beijing', 'China') " )
data.append(
         "insert into airport "
         "(airport_name, city_name, country)  "
         "values('Beijing Xijiao Airport', 'Beijing', 'China') ")
data.append(
         "insert into airport "
         "(airport_name, city_name, country)  "
         "values('Cape Town International Airport', 'Cape Town', 'South Africa') "
)

data.append(
         "insert into store "
         "(store_name, owner, airport_name, city_name, country)  "
         "values('Toys and Stuff', 'Toy Shop owner dude', 'Cape Town International Airport', 'Cape Town', 'South Africa') ")
data.append(
         "insert into store "
         "(store_name, owner, airport_name, city_name, country)  "
         "values('Smoke and Stuff', 'Snoop Dogg', 'John F. Kennedy International Airport', 'New York', 'United States') ")
data.append(
         "insert into store "
         "(store_name, owner, airport_name, city_name, country)  "
         "values('NotFake Store', 'MM Owner', 'Beijing Nanyuan Airport', 'Beijing', 'China') ")
data.append(
         "insert into store "
         "(store_name, owner, airport_name, city_name, country)  "
         "values('FluffyStuffy', 'FS Owner', 'Narita International Airport', 'Tokyo', 'Japan') ")
data.append(
         "insert into store "
         "(store_name, owner, airport_name, city_name, country)  "
         "values('Lokumcu', 'LokumcuBaba', 'Istanbul Ataturk Airport', 'Istanbul', 'Turkey') ")
data.append(
         "insert into store "
         "(store_name, owner, airport_name, city_name, country)  "
         "values('Kebap Kebap', 'Kebabci', 'Sabiha Gokcen International Airport', 'Istanbul', 'Turkey') ")
data.append(
         "insert into store "
         "(store_name, owner, airport_name, city_name, country)  "
         "values('Soda Limon', 'Sodaci', 'Ankara Esenboga Airport', 'Ankara', 'Turkey') ")
data.append(
         "insert into store "
         "(store_name, owner, airport_name, city_name, country)  "
         "values('Camel Tobacco', 'Camel Rider Smoke', 'Cairo International Airport', 'Cairo', 'Egypt') ")
data.append(
          "insert into store "
         "(store_name, owner, airport_name, city_name, country)  "
         "values('Tea Shop Leafy', 'Sir Arturia Hellsing', 'London City Airport', 'London', 'England') ")
data.append(
          "insert into store "
         "(store_name, owner, airport_name, city_name, country)  "
         "values('Akiba', 'Captain Tsubasa', 'Narita International Airport', 'Tokyo', 'Japan') ")
data.append(
          "insert into store "
         "(store_name, owner, airport_name, city_name, country)  "
         "values('Guns And Such', 'Mr.Freeman', 'John F. Kennedy International Airport', 'New York', 'United States') "
)

data.append(
         "insert into passenger "
         "(pass_id, expenditure, prom_expenditure)  "
         "values(1, 56756, 3345) ")
data.append(
         "insert into passenger "
         "(pass_id, expenditure, prom_expenditure)  "
         "values(2, 12312, 323) ")
data.append(
         "insert into passenger "
         "(pass_id, expenditure, prom_expenditure)  "
         "values(3, 11235, 45454) ")
data.append(
         "insert into passenger "
         "(pass_id, expenditure, prom_expenditure)  "
         "values(4, 66666, 66666) ")
data.append(
         "insert into passenger "
         "(pass_id, expenditure, prom_expenditure)  "
         "values(5, 665, 55) ")
data.append(
         "insert into passenger "
         "(pass_id, expenditure, prom_expenditure)  "
         "values(6, 4213, 666) ")
data.append(
         "insert into passenger "
         "(pass_id, expenditure, prom_expenditure)  "
         "values(7, 77777, 77) ")
data.append(
         "insert into passenger "
         "(pass_id, expenditure, prom_expenditure)  "
         "values(8, 6668, 88) ")
data.append(
         "insert into passenger "
         "(pass_id, expenditure, prom_expenditure)  "
         "values(9, 99999, 99) ")
data.append(
         "insert into passenger "
         "(pass_id, expenditure, prom_expenditure)  "
         "values(10, 101, 10) ")
data.append(
         "insert into passenger "
         "(pass_id, expenditure, prom_expenditure)  "
         "values(11, 1111, 12) "

)

data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(12, 300) ")
data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(13, 445) ")
data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(14, 677) ")
data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(15, 650) "
)
data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(16, 300) ")
data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(17, 445) ")
data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(18, 677) ")
data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(19, 650) "
)
data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(20, 300) ")
data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(21, 445) ")
data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(22, 677) ")
data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(23, 650) "
)
data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(24, 650) "
)
data.append(
         "insert into staff "
         "(staff_id, salary)  "
         "values(25, 650) "
)

data.append(
         "insert into flight_personnel "
         "(flight_pers_id, experience)  "
         "values(12, 2) " )
data.append(
         "insert into flight_personnel "
         "(flight_pers_id, experience)  "
         "values(13, 12) ")
data.append(
         "insert into flight_personnel "
         "(flight_pers_id, experience)  "
         "values(14, 12) ")
data.append(
         "insert into flight_personnel "
         "(flight_pers_id, experience)  "
         "values(15, 11) ")
data.append(
        "insert into flight_personnel "
         "(flight_pers_id, experience)  "
         "values(16, 4) "  )
data.append(
        "insert into flight_personnel "
         "(flight_pers_id, experience)  "
         "values(17, 6) " )
data.append(
        "insert into flight_personnel "
         "(flight_pers_id, experience)  "
         "values(18, 9) "  )
data.append(
        "insert into flight_personnel "
         "(flight_pers_id, experience)  "
         "values(19, 7) " )
data.append(
        "insert into flight_personnel "
         "(flight_pers_id, experience)  "
         "values(20, 6) ")
data.append(
        "insert into flight_personnel "
         "(flight_pers_id, experience)  "
         "values(21, 22) "
)

data.append(
         "insert into pilot "
         "(pilot_id, rank, certificate_type)  "
         "values(12, 2, 'sport') ")
data.append(
         "insert into pilot "
         "(pilot_id, rank, certificate_type)  "
         "values(13, 8, 'recreational') ")
data.append(
         "insert into pilot "
         "(pilot_id, rank, certificate_type)  "
         "values(14, 6, 'instructor') ")
data.append(
         "insert into pilot "
         "(pilot_id, rank, certificate_type)  "
         "values(15, 4, 'airline transport') ")
data.append(
         "insert into pilot "
         "(pilot_id, rank, certificate_type)  "
         "values(16, 10, 'commercial') "

)

data.append(
         "insert into flight_attendant "
         "(att_id, duty)  "
         "values(17, 'host') " )
data.append(
         "insert into flight_attendant "
         "(att_id, duty)  "
         "values(18, 'hostess') ")
data.append(
         "insert into flight_attendant "
         "(att_id, duty)  "
         "values(19, 'hostess') " )
data.append(
         "insert into flight_attendant "
         "(att_id, duty)  "
         "values(20, 'host') ")
data.append(
         "insert into flight_attendant "
         "(att_id, duty)  "
         "values(21, 'hostess') "
)

data.append(
         "insert into ticket_staff"
         "(ticket_staff_id, ticket_count)  "
         "values(22, 54621) ")
data.append(
         "insert into ticket_staff"
         "(ticket_staff_id, ticket_count)  "
         "values(23, 12334) "

)

data.append(
         "insert into store_staff"
         "(store_staff_id, sale_count, store_id)  "
         "values(24, 4474, 1) " )
data.append(
         "insert into store_staff"
         "(store_staff_id, sale_count, store_id)  "
         "values(25, 9865, 2) "
)

data.append(
         "insert into promotion "
         "(pass_id, prom_id, amount)  "
         "values(1, 1, 123) " )
data.append(
         "insert into promotion "
         "(pass_id, prom_id, amount)  "
         "values(2, 2, 12) " )
data.append(
         "insert into promotion "
         "(pass_id, prom_id, amount)  "
         "values(3, 3, 3) ")
data.append(
         "insert into promotion "
         "(pass_id, prom_id, amount)  "
         "values(4, 4, 4444) ")
data.append(
         "insert into promotion "
         "(pass_id, prom_id, amount)  "
         "values(5, 5, 55) ")
data.append(
         "insert into promotion "
         "(pass_id, prom_id, amount)  "
         "values(1, 6, 552) ")
data.append(
         "insert into promotion "
         "(pass_id, prom_id, amount)  "
         "values(2, 7, 535) ")
data.append(
         "insert into promotion "
         "(pass_id, prom_id, amount)  "
         "values(10, 8, 525) "

)

data.append(
         "insert into store_promotion "
         "(pass_id, prom_id, product_type)  "
         "values(1, 6, 'alcohol') ")
data.append(
         "insert into store_promotion "
         "(pass_id, prom_id, product_type)  "
         "values(2, 7, 'normal') " )
data.append(
         "insert into store_promotion "
         "(pass_id, prom_id, product_type)  "
         "values(3, 3, 'normal') "
)

data.append(
         "insert into food_promotion "
         "(pass_id, prom_id, food_type)  "
         "values(4, 4, 'drink') ")
data.append(
         "insert into food_promotion "
         "(pass_id, prom_id, food_type)  "
         "values(5, 5, 'meal') ")
data.append(
         "insert into food_promotion "
         "(pass_id, prom_id, food_type)   "
         "values(10, 8, 'meal') "
)

data.append(
         "insert into flight_promotion "
         "(pass_id, prom_id, domestic)  "
         "values(1, 1, true) ")
data.append(
         "insert into flight_promotion "
         "(pass_id, prom_id, domestic)  "
         "values(2, 2, false) "

)

data.append(
         "insert into promotion_deadline "
         "(amount, deadline)  "
         "values(123, '2018-01-21') ")
data.append(
         "insert into promotion_deadline "
         "(amount, deadline)  "
         "values(12, '2017-07-01') ")
data.append(
         "insert into promotion_deadline "
         "(amount, deadline)  "
         "values(3, '2017-06-01') ")
data.append(
         "insert into promotion_deadline "
         "(amount, deadline)  "
         "values(4444, '2018-04-01') "  )
data.append(
         "insert into promotion_deadline "
         "(amount, deadline)  "
         "values(55, '2017-01-01') " )
data.append(
         "insert into promotion_deadline "
         "(amount, deadline)  "
         "values(552, '2017-05-01') " )
data.append(
         "insert into promotion_deadline "
         "(amount, deadline)  "
         "values(535, '2017-04-01') " )
data.append(
         "insert into promotion_deadline "
         "(amount, deadline)  "
         "values(525, '2017-03-01') " )

data.append(
         "insert into plane_model "
         "(model, capacity, plane_range, altitude)  "
         "values('Concorde', 120, 7250, 18.3) "   )
data.append(
         "insert into plane_model "
         "(model, capacity, plane_range, altitude)  "
         "values('Boeing 777', 450, 9700, 13.1) ")
data.append(
         "insert into plane_model "
         "(model, capacity, plane_range, altitude)  "
         "values('Airbus A380', 853, 15700, 13.1) "
)

data.append(
        # of planes = 7
         "insert into plane "
         "(model)  "
         "values('Boeing 777') ")
data.append(
         "insert into plane "
         "(model)  "
         "values('Concorde') ")
data.append(
         "insert into plane "
         "(model)  "
         "values('Concorde') " )
data.append(
         "insert into plane "
         "(model)  "
         "values('Boeing 777') ")
data.append(
         "insert into plane "
         "(model)  "
         "values('Airbus A380') " )
data.append(
         "insert into plane "
         "(model)  "
         "values('Airbus A380') ")
data.append(
         "insert into plane "
         "(model)  "
         "values('Concorde') "

)
data.append(
         "insert into plane "
         "(model)  "
         "values('Concorde') "

)
data.append(
         "insert into plane "
         "(model)  "
         "values('Concorde') "

)
data.append(
         "insert into plane "
         "(model)  "
         "values('Concorde') "

)

data.append(
         "insert into flight "
         "(date, arrival, plane_id, dep_airport_name, dep_city_name, dep_country, arr_airport_name, arr_city_name, arr_country, duration, econ_price, business_price, landed)  "
         "values('2016-02-01 13:00:00', '2016-02-01 13:00:00',1,'Istanbul Ataturk Airport', 'Istanbul', 'Turkey', 'Ankara Esenboga Airport', 'Ankara', 'Turkey', 0.4, 200, 500, true) ")
data.append(
         "insert into flight "
         "(date, arrival, plane_id, dep_airport_name, dep_city_name, dep_country, arr_airport_name, arr_city_name, arr_country, duration, econ_price, business_price, landed)  "
         "values('2016-05-01 13:00:00', '2016-05-01 13:00:00',1, 'Istanbul Ataturk Airport', 'Istanbul', 'Turkey', 'John F. Kennedy International Airport', 'New York', 'United States', 14, 800, 2000, false) ")
data.append(
         "insert into flight "
         "(date, arrival, plane_id, dep_airport_name, dep_city_name, dep_country, arr_airport_name, arr_city_name, arr_country, duration, econ_price, business_price, landed)  "
         "values('2016-08-05 14:00:00', '2016-08-05 14:00:00',2, 'Sabiha Gokcen International Airport', 'Istanbul', 'Turkey', 'Cape Town International Airport', 'Cape Town', 'South Africa', 9, 1600, 4000, false) ")
data.append(
         "insert into flight "
         "(date, arrival, plane_id, dep_airport_name, dep_city_name, dep_country, arr_airport_name, arr_city_name, arr_country, duration, econ_price, business_price, landed)  "
         "values('2016-08-05 06:00:00', '2016-08-05 14:00:00',3,  'Narita International Airport', 'Tokyo', 'Japan', 'Ankara Esenboga Airport', 'Ankara', 'Turkey', 4, 2400, 6000, false) ")
data.append(
         "insert into flight "
         "(date,arrival, plane_id, dep_airport_name, dep_city_name, dep_country, arr_airport_name, arr_city_name, arr_country, duration, econ_price, business_price, landed)  "
         "values('2016-08-05 14:00:00', '2016-08-05 14:00:00',2,  'Ankara Esenboga Airport', 'Ankara', 'Turkey', 'London City Airport', 'London', 'England', 5, 2400, 6000, false) ")
data.append(
         "insert into flight "
         "(date, arrival,plane_id, dep_airport_name, dep_city_name, dep_country, arr_airport_name, arr_city_name, arr_country, duration, econ_price, business_price, landed)  "
         "values('2016-08-05 14:00:00','2016-08-05 14:00:00',1,  'Ankara Esenboga Airport', 'Ankara', 'Turkey', 'Cape Town International Airport', 'Cape Town', 'South Africa', 9, 2400, 6000, false) ")
data.append(
         "insert into flight "
         "(date, arrival, plane_id, dep_airport_name, dep_city_name, dep_country, arr_airport_name, arr_city_name, arr_country, duration, econ_price, business_price, landed)  "
         "values('2016-08-01 13:00:00','2016-10-01 13:00:00', 2, 'Heathrow Airport', 'London', 'England', 'Sabiha Gokcen International Airport', 'Istanbul', 'Turkey', 5, 1600, 4000, false) ")
data.append(
         "insert into flight "
         "(date, arrival, plane_id, dep_airport_name, dep_city_name, dep_country, arr_airport_name, arr_city_name, arr_country, duration, econ_price, business_price, landed)  "
         "values('2016-09-01 13:00:00','2016-10-01 13:00:00',1,'Sabiha Gokcen International Airport', 'Istanbul', 'Turkey', 'Beijing Nanyuan Airport', 'Beijing', 'China', 8, 1200, 3000, false) ")
data.append(
         "insert into flight "
         "(date, arrival, plane_id, dep_airport_name, dep_city_name, dep_country, arr_airport_name, arr_city_name, arr_country, duration, econ_price, business_price, landed)  "
         "values('2016-10-01 13:00:00', '2016-10-01 13:00:00', 2, 'Beijing Nanyuan Airport', 'Beijing', 'China', 'Haneda Airport', 'Tokyo', 'Japan', 2.5, 1000, 2500, false) ")
data.append(
         "insert into flight "
         "(date, arrival, plane_id, dep_airport_name, dep_city_name, dep_country, arr_airport_name, arr_city_name, arr_country, duration, econ_price, business_price, landed)  "
         "values('2016-03-01 13:00:00', '2016-03-01 13:00:00',1,'Haneda Airport', 'Tokyo', 'Japan', 'Cairo International Airport', 'Cairo', 'Egypt', 16, 1600, 4000, true) "
)


data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(1, 1, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(1, 2, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(1, 3, 'business') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(1, 4, 'business') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(2, 1, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(2, 2, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(2, 3, 'business') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(3, 1, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(3, 2, 'business') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(4, 1, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(4, 2, 'business') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(5, 1, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(5, 2, 'business') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(6, 1, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(6, 2, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(6, 3, 'business') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(7, 1, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(8, 1, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(8, 2, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(8, 3, 'business') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(9, 1, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(9, 2, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(9, 3, 'business') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(10, 1, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(10, 2, 'econ') ")
data.append(
         "insert into seat "
         "(flight_id, no, class)  "
         "values(10, 3, 'business') "

)

data.append(
         "insert into menu_option "
         "(flight_id, option_id, option_name, price)  "
         "values(3, 1, 'Kebap', 32.1) ")
data.append(
         "insert into menu_option "
         "(flight_id, option_id, option_name, price)  "
         "values(3, 2, 'pizza', 42.1) ")
data.append(
         "insert into menu_option "
         "(flight_id, option_id, option_name, price)  "
         "values(4, 3, 'breakfast', 12.1) ")
data.append(
         "insert into menu_option "
         "(flight_id, option_id, option_name, price)  "
         "values(5, 4, 'dailyspec', 54.3) "

)

data.append(
         "insert into reservation "
         "(flight_id, pass_id, deadline, seat_no)  "
         "values(1, 1, '2016-03-01 13:00:00', 1) ")
data.append(
         "insert into reservation "
         "(flight_id, pass_id, deadline, seat_no)  "
         "values(5, 1, '2016-03-01 13:00:00', 1) ")
data.append(
         "insert into reservation "
         "(flight_id, pass_id, deadline, seat_no)  "
         "values(5, 2, '2016-03-01 13:00:00', 2) ")
data.append(
         "insert into reservation "
         "(flight_id, pass_id, deadline, seat_no)  "
         "values(6, 3, '2016-03-01 13:00:00', 1) ")
data.append(
         "insert into reservation "
         "(flight_id, pass_id, deadline, seat_no)  "
         "values(7, 4, '2016-03-01 13:00:00', 1) " )
data.append(
         "insert into reservation "
         "(flight_id, pass_id, deadline, seat_no)  "
         "values(8, 5, '2016-03-01 13:00:00', 1) ")
data.append(
         "insert into reservation "
         "(flight_id, pass_id, deadline, seat_no)  "
         "values(8, 6, '2016-03-01 13:00:00', 2) ")
data.append(
         "insert into reservation "
         "(flight_id, pass_id, deadline, seat_no)  "
         "values(3, 6, '2016-03-01 13:00:00', 2) "
)

data.append(
         "insert into pass_history "
         "(flight_id, pass_id)  "
         "values(1, 3) "  )
data.append(
         "insert into pass_history "
         "(flight_id, pass_id)  "
         "values(1, 5) " )
data.append(
         "insert into pass_history "
         "(flight_id, pass_id)  "
         "values(1, 2) ")
data.append(
         "insert into pass_history "
         "(flight_id, pass_id)  "
         "values(10, 1) ")

data.append(
         "insert into pers_history "
         "(flight_id, flight_pers_id)  "
         "values(10, 20) "
)
data.append(
         "insert into pers_history "
         "(flight_id, flight_pers_id)  "
         "values(1, 16) "
)
data.append(
         "insert into pers_history "
         "(flight_id, flight_pers_id)  "
         "values(1, 17) "
)
data.append(
         "insert into pers_history "
         "(flight_id, flight_pers_id)  "
         "values(1, 18) "
)

data.append(
         "insert into flight_pilot "
         "(flight_id, pilot_id)  "
         "values(1, 12) ")
data.append(
         "insert into flight_pilot "
         "(flight_id, pilot_id)  "
         "values(10, 13) " )
data.append(
         "insert into flight_pilot "
         "(flight_id, pilot_id)  "
         "values(1, 14) "

)

data.append(
         "insert into flight_att "
         "(flight_id, att_id)  "
         "values(2, 17) ")
data.append(
         "insert into flight_att "
         "(flight_id, att_id)  "
         "values(3, 18) ")
data.append(
         "insert into flight_att "
         "(flight_id, att_id)  "
         "values(3, 19) ")
data.append(
         "insert into flight_att "
         "(flight_id, att_id)   "
         "values(4, 20) ")
data.append(
         "insert into flight_att "
         "(flight_id, att_id) "
         "values(5, 19) ")
data.append(
         "insert into flight_att "
         "(flight_id, att_id) "
         "values(5, 17) ")
data.append(
         "insert into flight_att "
         "(flight_id, att_id) "
         "values(6, 18) " )
data.append(
         "insert into flight_att "
         "(flight_id, att_id) "
         "values(6, 19) " )
data.append(
         "insert into flight_att "
         "(flight_id, att_id) "
         "values(7, 20) ")
data.append(
         "insert into flight_att "
         "(flight_id, att_id) "
         "values(8, 19) "        )
data.append(
         "insert into flight_att "
         "(flight_id, att_id) "
         "values(9, 18) "        )
data.append(
         "insert into flight_att "
         "(flight_id, att_id) "
         "values(9, 17) ")

data.append(
         "insert into ticket "
         "(flight_id, pass_id, staff_id, seat_no, luggage, price) "
         "values(1, 1, 22, 1, 1, 40); " )
data.append(
         "insert into ticket "
         "(flight_id, pass_id, staff_id, seat_no, luggage, price) "
         "values(5, 1, 22, 1, 1, 40); " )
data.append(
         "insert into ticket "
         "(flight_id, pass_id, staff_id, seat_no, luggage, price) "
         "values(5, 2, 22, 2, 1, 30); ")
data.append(
         "insert into ticket "
         "(flight_id, pass_id, staff_id, seat_no, luggage, price) "
         "values(6, 3, 22, 1, 1, 20); ")
data.append(
         "insert into ticket "
         "(flight_id, pass_id, staff_id, seat_no, luggage, price) "
         "values(7, 4, 23, 1, 2, 100); ")
data.append(
         "insert into ticket "
         "(flight_id, pass_id, staff_id, seat_no, luggage, price) "
         "values(8, 5, 23, 1, 2, 140); ")
data.append(
         "insert into ticket "
         "(flight_id, pass_id, staff_id, seat_no, luggage, price) "
         "values(8, 6, 23, 2, 3, 50); ")
data.append(
         "insert into ticket "
         "(flight_id, pass_id, staff_id, seat_no, luggage, price) "
         "values(3, 6, 22, 2, 3, 40); ")

i = 0
for sql in data:
    try:
        cursor.execute(sql)
        conn.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print( "already exists. ")
        else:
            print("SATIR: {} ERR: {} SQL: {}".format(i, err, sql))
    i += 1

conn.commit()

trigger = []

trigger.append("create procedure insert_ticket_trigger(new_price numeric(6,2), new_pass_id int, new_flight_id int) "
               "BEGIN insert into pass_history values(new_pass_id, new_flight_id);"
               "update passenger set expenditure = expenditure + new_price where pass_id = new_pass_id; END")

trigger.append("create procedure update_flight_trigger(new_date DATETIME, new_duration numeric(5,2), new_id int, new_landed binary) "
               "BEGIN"
               " delete from flight_att where flight_id = new_id and new_landed = 1;"
               " delete from flight_pilot where flight_id = new_id and new_landed = 1; END")

trigger.append( "create trigger update_flight after update on flight for each row  "
                "call update_flight_trigger(new.date, new.duration, new.flight_id, new.landed) ")

trigger.append( "create trigger luggage_expenditure after update on ticket for each row begin  "
                "if old.luggage > 20 then update passenger set expenditure = expenditure +  "
                "(new.luggage - old.luggage) * 10 where new.luggage > 20 and pass_id = new.pass_id;  "
                "else update passenger set expenditure = expenditure + (new.luggage - 20) * 10  "
                "where new.luggage > 20 and pass_id = new.pass_id; end if; end ")

trigger.append( "create trigger insert_ticket after insert on ticket  "
                "for each row call insert_ticket_trigger(new.price, new.pass_id, new.flight_id)")

trigger.append( "create trigger delete_pass_history after delete on ticket  "
                "for each row delete from pass_history where flight_id = old.flight_id  "
                "and pass_id = old.pass_id ")

trigger.append( "create trigger add_att_history after insert on flight_att for each row  "
                "insert into pers_history values(new.flight_id, new.att_id) ")

trigger.append( "create trigger add_pilot_history after insert on flight_pilot for each row  "
                "insert into pers_history values(new.flight_id, new.pilot_id) ")

trigger.append("create procedure delete_person_trigger(old_person_id int) "
               "BEGIN delete from person_phone where person_id = old_person_id;"
               "delete from person_email where person_id = old_person_id;"
               "delete from passenger where pass_id = old_person_id;"
               "delete from staff where staff_id = old_person_id;"
               "delete from flight_personnel where flight_pers_id = old_person_id;"
               "delete from pilot where pilot_id = old_person_id;"
               "delete from flight_attendant where att_id = old_person_id;"
               "delete from ticket_staff where ticket_staff_id = old_person_id;"
               "delete from store_staff where store_staff_id = old_person_id; END")

trigger.append( "create trigger delete_person after delete on person for each row "
                "call delete_person_trigger(old.person_id)")

for sql in trigger:
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print( "already exists. ")
        else:
            print(err.msg)
conn.commit()

index = []
index.append("CREATE INDEX email_index USING BTREE ON person_email(email)")
index.append("CREATE INDEX source_city_index USING BTREE ON flight(dep_city_name)")
index.append("CREATE INDEX dest_city_index USING BTREE ON flight(arr_city_name)")
index.append("CREATE INDEX plane_range_index USING BTREE ON plane_model(plane_range)")

for sql in index:
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print( "already exists. ")
        else:
            print(err.msg)

cursor.close();
conn.close();
