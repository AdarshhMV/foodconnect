document.addEventListener('DOMContentLoaded', () => {
    const mapElement = document.getElementById('listing-location-map');
    const latitudeInput = document.getElementById('id_latitude');
    const longitudeInput = document.getElementById('id_longitude');
    const coordinateDisplay = document.getElementById('selected-coordinates');

    if (!mapElement || !latitudeInput || !longitudeInput || typeof L === 'undefined') {
        return;
    }

    const defaultLat = 20.5937;
    const defaultLng = 78.9629;
    const hasSavedCoordinates = latitudeInput.value && longitudeInput.value;
    const initialLat = hasSavedCoordinates ? Number(latitudeInput.value) : defaultLat;
    const initialLng = hasSavedCoordinates ? Number(longitudeInput.value) : defaultLng;

    const map = L.map(mapElement).setView([initialLat, initialLng], hasSavedCoordinates ? 14 : 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map);

    let marker = null;

    const updateCoordinateDisplay = (lat, lng) => {
        coordinateDisplay.innerHTML = `<span><i class="bi bi-geo-alt-fill"></i> Selected: ${lat.toFixed(6)}, ${lng.toFixed(6)}</span>`;
    };

    const setMarker = (lat, lng) => {
        latitudeInput.value = lat.toFixed(6);
        longitudeInput.value = lng.toFixed(6);
        updateCoordinateDisplay(lat, lng);

        if (marker) {
            marker.setLatLng([lat, lng]);
            return;
        }

        marker = L.marker([lat, lng]).addTo(map);
    };

    if (hasSavedCoordinates) {
        setMarker(initialLat, initialLng);
    }

    map.on('click', (event) => {
        const { lat, lng } = event.latlng;
        setMarker(lat, lng);
    });
});
