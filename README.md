# data-representation-project
# Quarantine Map Project

## Overview
The Quarantine Map Project is a web-based application that allows users to visualize and track quarantine data for various buildings. This README provides an overview of the project, its features, and how to set it up and run it.

## Features
- Interactive Map: Displays a map with markers representing different buildings.
- Building Information: Clicking on a marker shows detailed information about the building, including the number of lots and the quantity of parts in quarantine.
- Data Retrieval: The application retrieves building data from a server using AJAX calls.
- Mapping Library: Utilizes the Leaflet mapping library to create an interactive map interface.
- Server-Side: Includes server-side code to handle data retrieval and API endpoints.

## Installation and Setup
To run the Quarantine Map Project locally, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have Python installed. The project includes a Flask-based server.
3. Install the required Python packages by running:

pip install -r requirements.txt

4. Start the Flask server by running:

python app.py

5. Open a web browser and navigate to the local server URL (e.g., `http://localhost:5000`).

## Usage
- The map will display markers for different buildings.
- Click on a marker to view information about the building, including lots in quarantine and quantity of parts in quarantine.
- Login credentials are username and password

## Project Structure
The project is structured as follows:
- `app.py`: The main Flask application.
- `quarantineDAO.py`: Data Access Object for retrieving building data.
- `static/`: Contains static assets (e.g., JavaScript, CSS).
- `templates/`: Contains HTML templates for the application pages.

## Dependencies
- Flask: Python web framework for the server.
- Leaflet: JavaScript library for interactive maps.

## Contributing
Contributions to the project are welcome. Please follow the standard open-source guidelines for contributions.

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
If you have any questions or need assistance, feel free to contact [Your Name](mailto:your.email@example.com).

