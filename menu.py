def c_dic(link, icon, title):
    return {
        'link': link,
        'icon': icon,
        'title': title
    }

profile = c_dic('/profile', 'fa-user', 'Profile')

passenger = [
    c_dic('/passenger/flights', 'fa-plane', 'Flights'),
    c_dic('/passenger/flight_history', 'fa-history', 'Flight History'),
    c_dic('/passenger/reservations', 'fa-barcode', 'Reservations'),
    c_dic('/passenger/promotions', 'fa-gift', 'Promotions'),
    c_dic('/passenger/store', 'wb-shopping-cart', 'Store'),
    profile
]

pilot = [
    c_dic('/attendant/current', 'fa-plane', 'Current Flights'),
    c_dic('/attendant/flight_history', 'fa-history', 'Flight History'),
    profile
]

attendant = [
    c_dic('/attendant/current', 'fa-plane', 'Current Flights'),
    c_dic('/attendant/flight_history', 'fa-history', 'Flight History'),
    c_dic('/attendant/food_promotion', 'fa-gift', 'Food Promotion'),
    profile
]

ticket_staff = [
    c_dic('/ticket_staff/sale', 'fa-plane', 'Ticket Sale'),
    c_dic('/ticket_staff/flight_promotions', 'fa-gift', 'Flight Promotions'),
    c_dic('/ticket_staff/history', 'fa-history', 'Ticket History'),
    profile
]

store_staff = [
    c_dic('/store_staff/flight_promotions', 'fa-gift', 'Store Promotions'),
    profile
]

admin = [
    c_dic('/admin/delay', 'wb-sort-asc', 'Delay'),
    c_dic('/admin/flight', 'fa-refresh', 'Flight'),
    c_dic('/admin/plane', 'fa-plane', 'Plane'),
    c_dic('/admin/menu', 'wb-menu', 'Menu'),
    c_dic('/admin/crew', 'wb-users', 'Crew'),
    c_dic('/admin/account', 'wb-settings', 'Assign Accounts'),
    c_dic('/admin/scheduled', 'wb-graph-up', 'Scheduled Flights'),
    profile
]

def get_menu():
    return {
        'passenger': passenger,
        'attendant': attendant,
        'pilot': pilot,
        'ticket_staff': ticket_staff,
        'store_staff': store_staff,
        'admin': admin
    }
