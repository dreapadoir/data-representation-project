from flask import Flask, render_template, request, redirect, url_for
import quarantineDAO  # Ensure this matches the name of your DAO file

app = Flask(__name__)

# Route to view records
@app.route('/')
def index():
    dao = quarantineDAO.QuarantineDAO()
    records = dao.getAll()
    return render_template('index.html', records=records)

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
    dao = quarantineDAO.QuarantineDAO()
    dao.delete(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
