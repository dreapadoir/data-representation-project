# data-representation-project
# David Higgins - G00411302
# Boeing Quarantine Dashboard

## Overview
This project is a web-based application that allows users to visualize and track quarantine data for various fictional buildings at the Boeing manufacturing facility in Seattle. This README provides an overview of the project, its features, and how to set it up and run it. The Python code in this project was implemented using Python 3 on the Anaconda distribution. Javascript was used to create the map functionality. MySQL Server 8.0 and MySQL Workbench 8.0 were used to build and maintain the two SQL tables in the quarantine database (table quar used to manage the lots and table operator used to manage operators). The requirements.txt file holds all the necessary packages required to run this project.

## Features
- Interactive Map: Displays a map with markers representing different buildings.
- Building Information: Clicking on a marker shows detailed information about the building, including the number of lots and the quantity of parts in quarantine.
- Data Retrieval: The application retrieves building data from a server using AJAX calls.
- Mapping Library: Utilizes the Leaflet mapping library to create an interactive map interface.
- Server-Side: Includes server-side code to handle data retrieval and API endpoints.

## Installation and Setup
To run the Quarantine Dashboard locally, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have Python installed. The project includes a Flask-based server.
3. Install the required Python packages by running:

pip install -r requirements.txt

4. Start the Flask server by running:

python app.py

5. Open a web browser and navigate to the local server URL (e.g., `http://127.0.0.1:5000`).

## Usage
- The map will display markers for different buildings.
- Click on a marker to view information about the building, including lots in quarantine and quantity of parts in quarantine.
- Login credentials are username and password
- The quarantine database can be searched on the search page and will return the current state and details of the lot
- The operator is identified by badge number in the data entry functions but for display purposes, a second SQL table is searched to return a dictionary matching the badge number and name. This allows the operator's name to be displayed when viewing details of each lot.
- The current local temperature in Seattle is displayed in the banner. This is data pulled from the OpenMeteo API (https://open-meteo.com/).
- New lots can be added to quarantine using the button on the index.html page and subsequent form on signin.html.
- Lots currently in quarantine can be signed out using the red buttons at the right of the data table on index.html
- The lot number in the main data table on the index.html page is a hyperlink that will bring the user to a form where they can update or delete a lot.
- At the top of the index.html page are a set of metrics showing current inventory levels and recents signs in and out.

## Project Structure
The project is structured as follows:
- `app.py`: The main Flask application.
- `quarantineDAO.py`: Data Access Object for retrieving building data.
- `static/`: Contains static assets (e.g., JavaScript, CSS).
- `templates/`: Contains HTML templates for the application pages.
- `quarantine.sql`: SQL databases containing quar and operator tables.

## Dependencies
- Flask: Python web framework for the server.
- Leaflet: JavaScript library for interactive maps.




