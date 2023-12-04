from flask import Flask, render_template, request, redirect, url_for
from quarantineDAO import QuarantineDAO  # Ensure this matches the name of your DAO file

app = Flask(__name__)
dao = QuarantineDAO()
# Route to view records

@app.route('/')
def index():
    try:
        records = dao.getAll()
        number_of_lots = len(records) if records else 0
        # For average_days_in_quarantine, you'll need to calculate the average
        # based on the 'datein' field of each record and today's date.
        
        return render_template('index.html', records=records, number_of_lots=number_of_lots)
    except Exception as e:
        print("An error occurred:", e)
        return render_template('index.html', records=[], number_of_lots=0)



# Route to add a record
@app.route('/add', methods=['POST'])
def add_record():
    # Extract data from form and call DAO to add record
    return redirect(url_for('index'))

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
