document.addEventListener('DOMContentLoaded', () => {
    fetch('/get_alerts')
        .then(response => response.json())
        .then(data => {
            const alertsList = document.querySelector('alertsList');
            data.forEach(alert => {
                const alertItem = document.createElement('div');
                alertItem.classList.add('alert-item');
                alertItem.setAttribute('onclick', `showDetails(${alert.id})`);
                alertItem.innerHTML = `
                    <p class="crime-type">${alert.type}</p>
                    <p class="alert-date">${alert.date}</p>
                    <button class="view-details-button">View Details</button>
                `;
                alertsList.appendChild(alertItem);
            });
        });
});

function showDetails(alertId) {
    // Example data, in a real application, fetch data from server or database
    fetch(`/get_alert_details?id=${alertId}`)
        .then(response => response.json())
        .then(alert => {
            const detailsContent = document.getElementById('details-content');
            detailsContent.innerHTML = `
                <p><strong>Type:</strong> ${alert.type}</p>
                <p><strong>Date:</strong> ${alert.date}</p>
                <p><strong>Description:</strong> ${alert.description}</p>
            `;
            document.getElementById('side-panel').style.display = 'block';
        });
}

function closePanel() {
    document.getElementById('side-panel').style.display = 'none';
}
function loadPage(page) {
    if (page === 'create-alert') {
        window.location.href = '/c_alerts.html';
    } else if (page === 'my-reports') {
        window.location.href = '/my_reports.html';
    }
}