document.getElementById('reporForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const county = document.getElementById('county').value;
    const location = document.getElementById('location').value;
    const crimeType = document.getElementById('crime').value;
    const datetime = document.getElementById('datetime').value;
    const description = document.getElementById('description').value;
    const anonymous = document.getElementById('anonymous').checked;

    const reportData = {
        county,
        location,
        crimeType,
        datetime,
        description,
    };
    try {
        const response = await fetch('/api/reports', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(reportData),
        });

        if (response.ok) {
            alert('Report submitted successfully');
            window.location.href = '/alert.html';
        } else {
            const errorData = await response.json();
            alert('Error: ' + errorData.message);
        }
    } catch (error) {
        console.error('Error submitting report:', error);
        alert('Error submitting report. Please try again later.');
    }
});