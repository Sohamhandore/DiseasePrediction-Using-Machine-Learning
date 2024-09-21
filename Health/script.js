document.getElementById('healthForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('bloodTestReport', document.getElementById('bloodTestReport').files[0]);
    formData.append('bloodPressure', document.getElementById('bloodPressure').value);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = `<h2>Prediction Results:</h2><p>${JSON.stringify(data)}</p>`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
