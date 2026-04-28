document.addEventListener('DOMContentLoaded', () => {
    const mapElement = document.getElementById('receiver-listings-map');
    const dataElement = document.getElementById('receiver-listings-map-data');

    if (!mapElement || !dataElement || typeof L === 'undefined') {
        return;
    }

    const listings = JSON.parse(dataElement.textContent);
    if (!listings.length) {
        return;
    }

    const firstListing = listings[0];
    const map = L.map(mapElement).setView([firstListing.latitude, firstListing.longitude], 12);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        referrerPolicy: 'strict-origin-when-cross-origin',
        attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors',
    }).addTo(map);

    const bounds = [];

    listings.forEach((listing) => {
        const marker = L.marker([listing.latitude, listing.longitude]).addTo(map);
        const popupHtml = `
            <div class="map-popup">
                <h3>${listing.title}</h3>
                <p>${listing.description}</p>
                <p><strong>Quantity:</strong> ${listing.quantity}</p>
                <p><strong>Pickup:</strong> ${listing.pickup_location}</p>
                <p><strong>Donor:</strong> ${listing.donor}</p>
                <p><strong>Status:</strong> ${listing.status}</p>
                <p><a href="${listing.request_url}">Open request page</a></p>
            </div>
        `;
        marker.bindPopup(popupHtml);
        bounds.push([listing.latitude, listing.longitude]);
    });

    if (bounds.length > 1) {
        map.fitBounds(bounds, { padding: [30, 30] });
    }
});
