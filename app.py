from flask import Flask, render_template, request, redirect, url_for
from quarantineDAO import QuarantineDAO  # Ensure this matches the name of your DAO file
from datetime import datetime


app = Flask(__name__)
dao = QuarantineDAO()


def calculate_average_days(records):
    total_days = 0
    count = 0
    for record in records:
        if record['datein']:  # Assuming 'datein' is already a date object
            # No need to parse it, just calculate the difference
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



# @app.route('/')
# def index():
#     try:
#         records = dao.getAll()
#         number_of_lots = len(records) if records else 0
#         # For average_days_in_quarantine, you'll need to calculate the average
#         # based on the 'datein' field of each record and today's date.
        
#         return render_template('index.html', records=records, number_of_lots=number_of_lots)
#     except Exception as e:
#         print("An error occurred:", e)
#         return render_template('index.html', records=[], number_of_lots=0)


@app.route('/')
def index():
    try:
        records = dao.getAll()
        number_of_lots = len(records) if records else 0
        average_days_in_quarantine = calculate_average_days(records)
        lots_over_7_days = count_lots_over_days(records, 7)  # Using the helper function
        return render_template('index.html', records=records, number_of_lots=number_of_lots,
                               average_days_in_quarantine=average_days_in_quarantine,
                               lots_over_7_days=lots_over_7_days)  # Pass the count to the template
    except Exception as e:
        print("An error occurred:", e)
        # Pass default values if an error occurs
        return render_template('index.html', records=[], number_of_lots=0,
                               average_days_in_quarantine=0, lots_over_7_days=0)


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
            # Add other fields as necessary
        }
        dao.update(updated_values)
        return redirect(url_for('index'))
    else:
        # For a GET request, find the record by lot and render the edit page
        record = dao.findByID(lot)
        return render_template('edit.html', record=record)


# Route to delete a record
@app.route('/delete/<int:id>')
def delete_record(id):
    dao = dao.QuarantineDAO()
    dao.delete(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
