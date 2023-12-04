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


# Route to edit a record
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_record(id):
    # Handle record editing
    return render_template('edit.html')

# Route to delete a record
@app.route('/delete/<int:id>')
def delete_record(id):
    dao = dao.QuarantineDAO()
    dao.delete(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
