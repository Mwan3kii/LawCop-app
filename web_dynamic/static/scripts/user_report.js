document.addEventListener('DOMContentLoaded', () => {
    fetch('/my_reports')
        .then(response => response.json())
        .then(data => {
            const reportsList = document.getElementById('reportsList');
            data.reports.forEach(report => {
                const reportItem = document.createElement('div');
                reportItem.className = 'report-item';
                reportItem.innerHTML = `
                    <p class="report-type">${report.type}</p>
                    <p class="report-date">${report.date}</p>
                    <div class="manage-buttons">
                        <button class="view-details-button" onclick="viewDetails(${report.id})">View Details</button>
                        <button class="edit-button" onclick="editReport(${report.id})">Edit</button>
                        <button class="delete-button" onclick="deleteReport(${report.id})">Delete</button>
                    </div>
                `;
                reportsList.appendChild(reportItem);
            });
        });
});

function viewDetails(reportId) {
    fetch(`/get_report_details?id=${id}`)
        .then(response => response.json())
        .then(data => {
            const sidePanel = document.getElementById('side-panel');
            const detailsContent = document.getElementById('details-content');
            detailsContent.innerHTML = `
                <h2>${data.type}</h2>
                <p>Date: ${data.date}</p>
                <p>${data.description}</p>
            `;
            sidePanel.style.display = 'block';
        });
}

function editReport(id) {
    // Code to edit the report
}

function deleteReport(id) {
    fetch(`/delete_report?id=${id}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.location.reload();
        }
    });
}

function closePanel() {
    document.getElementById('side-panel').style.display = 'none';
}