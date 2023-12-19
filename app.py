from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from quarantineDAO import QuarantineDAO  # this is the data access object that was created to interact with the database
from datetime import datetime, timedelta # timedelta is required to accomodate weekends in ount_lots_signed_out_last_2_days() - line 33
import requests


# initialize Flask application, bcrypt for password hashing, and HTTP auth
app = Flask(__name__)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()

# dictionary with login credentials
users = {
    'username': bcrypt.generate_password_hash('password').decode('utf-8')
}

dao = QuarantineDAO()

# authentication function
@auth.verify_password
def verify_password(username, password):
    if username in users and bcrypt.check_password_hash(users.get(username), password):
        return username

    
def count_lots_signed_out_last_2_days(records):
    today = datetime.now().date()
    weekday = today.weekday()

    # Include Friday if today is Monday
    if weekday == 0:
        start_date = today - timedelta(days=3)
    else:
        start_date = today - timedelta(days=1)

    count = 0
    for record in records:
        if record['dateout']:
            date_out = record['dateout']
            if start_date <= date_out <= today:
                count += 1
    return count

def calculate_average_days_for_status1(records):
    total_days = 0
    count = 0
    for record in records:
        if record['datein'] and record['status'] == 1:
            date_in = record['datein']
            # Calculate the difference only for lots with status 1
            delta = datetime.now().date() - date_in
            total_days += delta.days
            count += 1
    return total_days / count if count > 0 else 0

def count_new_lots_signed_in(records):
    today = datetime.now().date()
    weekday = today.weekday()

    if weekday == 0:
        start_date = today - timedelta(days=3)
    else:
        start_date = today - timedelta(days=1)

    count = 0
    for record in records:
        if record['datein']:
            date_in = record['datein']
            if date_in >= start_date:
                count += 1
    return count

def count_lots_over_7_days_for_status1(records, days=7):
    count = 0
    for record in records:
        if record['datein'] and record['status'] == 1:
            delta = datetime.now().date() - record['datein']
            if delta.days > days:
                count += 1
    return count

def count_lots_signed_in(records):
    today = datetime.now().date()
    weekday = today.weekday()  # Get the current day of the week (0 = Monday, 6 = Sunday)

    # Calculate the start date based on the current day of the week
    if weekday == 0:  # If today is Monday, include Friday, Saturday, Sunday, and today
        start_date = today - timedelta(days=3)
    else:  # Include yesterday and today
        start_date = today - timedelta(days=1)

    count = 0
    for record in records:
        if record['datein']:
            date_in = record['datein']
            if date_in >= start_date:
                count += 1
    return count

def calculate_average_days(records):
    total_days = 0
    count = 0
    for record in records:
        if record['datein']:
            date_in = record['datein']
            delta = datetime.now().date() - date_in
            total_days += delta.days
            count += 1
    return total_days / count if count > 0 else 0


def count_lots_over_days(records, days=7):
    count = 0
    for record in records:
        if record['datein']:
            # Directly calculate the difference as 'datein' is already a date object
            delta = datetime.now().date() - record['datein']
            if delta.days > days:
                count += 1
    return count


# Route for the main page, requires authentication
@app.route('/')
@auth.login_required

def index():
    try:
        records = dao.getAll()
        number_of_lots = len([record for record in records if record['status'] == 1])

        average_days_in_quarantine = calculate_average_days_for_status1(records)
        new_lots_signed_in = count_new_lots_signed_in(records)
        lots_over_7_days = count_lots_over_7_days_for_status1(records, 7)
        total_parts_in_quarantine = sum(record['qty'] for record in records if record['status'] == 1)
        lots_signed_out_last_2_days = count_lots_signed_out_last_2_days(records)

        return render_template('index.html', records=records, number_of_lots=number_of_lots,
                               average_days_in_quarantine=average_days_in_quarantine,
                               new_lots_signed_in=new_lots_signed_in,
                               lots_over_7_days=lots_over_7_days,
                               total_parts_in_quarantine=total_parts_in_quarantine,
                               lots_signed_out_last_2_days=lots_signed_out_last_2_days)
    except Exception as e:
        print("An error occurred:", e)
        return render_template('index.html', records=[], number_of_lots=0,
                               average_days_in_quarantine=0, new_lots_signed_in=0,
                               lots_over_7_days=0)




@app.route('/signin', methods=['GET', 'POST'])
def sign_in_lot():
    if request.method == 'POST':
        # Extract data from form
        lot = request.form['lot']
        part = request.form['part']
        qty = request.form['qty']
        datein = request.form['datein']
        reason = request.form['reason']
        badge = request.form['badge']

        # Convert datein to a datetime object
        datein = datetime.strptime(datein, '%Y-%m-%d').date()

        # Create a new record in the database
        new_id = dao.create((lot, part, qty, datein, reason, badge, None, None, True, None))
        return redirect(url_for('index'))  # Redirect to the index page after form submission
    return render_template('signin.html')

@app.route('/edit/<int:lot>', methods=['GET', 'POST'])
def edit_record(lot):
    if request.method == 'POST':
        # Extract data from form and update the record
        updated_values = {
            'lot': lot,
            'part': request.form['part'],
            'qty': request.form['qty'],
            'datein': request.form['datein'],
            'reason': request.form['reason'],
            'badge': request.form['badge']
            
        }
        dao.update(updated_values)
        return redirect(url_for('index'))
    else:
        # For a GET request, find the record by lot and render the edit page
        record = dao.findByID(lot)
        return render_template('edit.html', record=record)


# Route to delete a record
@app.route('/delete/<int:lot>', methods=['POST'])
def delete_record(lot):
    dao.delete(lot)
    return redirect(url_for('index'))

@app.route('/signout/<int:lot>', methods=['GET', 'POST'])
def sign_out_lot(lot):
    if request.method == 'POST':
        try:
            # Extract data from the form
            badgeout = request.form['badgeout']
            dateout = request.form['dateout']
            signoutcomment = request.form['signoutcomment']

            # Update the sign-out details in the database using the new method
            dao.update_signout(lot, badgeout, dateout, signoutcomment)

            # Redirect to the index page after successful sign-out
            return redirect(url_for('index'))
        except Exception as e:
            # Handle any errors or exceptions here
            print("An error occurred:", e)

    # For a GET request, find the record by lot and render the signout page
    record = dao.findByID(lot)
    return render_template('signout.html', record=record)

@app.route('/search', methods=['GET', 'POST'])
def search_records():
    if request.method == 'POST':
        search_query = request.form.get('search_query')

        search_results = dao.search_records(search_query)

        return render_template('search.html', search_results=search_results)

    return render_template('search.html', search_results=[])


@app.route('/view_record/<int:lot>', methods=['GET'])
def view_record(lot):
    try:
        record = dao.findByID(lot)
        operator_data = dao.get_operator_data()  # Fetch operator data
        return render_template('record_details.html', record=record, operator_data=operator_data)
    except Exception as e:
        print("An error occurred:", e)
        return render_template('record_details.html', record={}, operator_data={})



@app.route('/api/buildings')
def get_buildings():
    # Query the database using the DAO to get the sum of quantities and count of lots for each building
    buildings_data = dao.get_building_data()  

    # Map the buildings to their static lat/lon values
    static_locations = {
        'B1': {'lat': 47.929246, 'lon': -122.275260},
        'B3': {'lat': 47.929156, 'lon': -122.269902},
        'B6': {'lat': 47.925021, 'lon': -122.272193}
    }

    # Combine the data from the DAO with the static location data
    buildings = []
    for building in buildings_data:
        building_info = static_locations.get(building['name'], {})
        building_info.update({
            'name': building['name'],
            'lots': building['lot_count'],
            'parts': building['total_qty']
        })
        buildings.append(building_info)

    return jsonify(buildings)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if verify_password(username, password):
        return redirect(url_for('protected'))
    else:
        return 'Login failed. Please try again.'

# route to pull in current weather in Seattle to display as a basic widget in page banner    
@app.route('/get_weather_data')
def get_weather_data():
    latitude = 47.6062  # latitude of Boeing factory in Seattle
    longitude = -122.3321  # longitude of Boeing factory
    endpoint = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': True
    }
    
    try:
        response = requests.get(endpoint, params=params, verify=False)
        response.raise_for_status()
        weather_data = response.json()
        current_temperature = weather_data['current_weather']['temperature']
        return jsonify({'current_temperature': current_temperature})
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return jsonify({'error': 'Error fetching weather data'}), 500
    except Exception as err:
        print(f'Other error occurred: {err}')
        return jsonify({'error': 'An unexpected error occurred'}), 500




if __name__ == '__main__':
    app.run(debug=True)
