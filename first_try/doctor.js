document.getElementById('doctorForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/upload_reports', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const tableBody = document.querySelector('#patientTable tbody');
            tableBody.innerHTML = ''; // Clear existing rows

            data.forEach(report => {
                const row = document.createElement('tr');

                const fileNameCell = document.createElement('td');
                fileNameCell.textContent = report.filename;
                row.appendChild(fileNameCell);

                const criticalityCell = document.createElement('td');
                criticalityCell.textContent = report.criticality;
                row.appendChild(criticalityCell);

                tableBody.appendChild(row);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing the reports.');
    });
});
