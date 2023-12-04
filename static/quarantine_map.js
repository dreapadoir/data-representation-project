// Initialize the map
var map = L.map('map').setView([47.928141, -122.273287], 15);

// Add the tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Function to add markers to the map
function addMarkers(buildings) {
    for (var i = 0; i < buildings.length; i++) {
        var building = buildings[i];
        var marker = L.marker([building.lat, building.lon]).addTo(map);
        marker.bindPopup(`
            <strong>${building.name}</strong><br>
            Lots in Quarantine: ${building.lots}<br>
            Quantity of Parts in Quarantine: ${building.parts}
        `);
    }
}

// AJAX call to get building data from the server
fetch('/api/buildings')
    .then(response => response.json())
    .then(data => addMarkers(data))
    .catch(error => console.error('Error:', error));
