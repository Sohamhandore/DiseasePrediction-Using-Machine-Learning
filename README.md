<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Disease Prediction System</title>
  <style>
    /* Reset & basic styles */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: Arial, sans-serif;
    }

    body {
      background-color: #f5f7fa;
      color: #333;
      line-height: 1.6;
    }

    /* Banner styles */
    .main-banner {
      position: relative;
      text-align: center;
      color: white;
      margin-bottom: 30px;
      overflow: hidden;
    }

    .main-banner img {
      width: 100%;
      max-height: 400px;
      object-fit: cover;
      filter: brightness(0.6);
      display: block;
    }

    .main-banner h1 {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 3rem;
      font-weight: bold;
      text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.8);
    }

    /* Container */
    .container {
      max-width: 600px;
      background: white;
      margin: auto;
      padding: 20px 30px 40px;
      border-radius: 8px;
      box-shadow: 0 0 15px rgba(0,0,0,0.1);
    }

    /* Form styles */
    form {
      display: flex;
      flex-direction: column;
    }

    label {
      margin: 15px 0 5px;
      font-weight: bold;
    }

    input[type="text"] {
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 1rem;
    }

    button {
      margin-top: 25px;
      padding: 12px;
      font-size: 1.1rem;
      background-color: #007bff;
      border: none;
      color: white;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }

    button:hover {
      background-color: #0056b3;
    }

    /* Result display */
    #result {
      margin-top: 30px;
      padding: 15px;
      background-color: #e9ffe9;
      border: 1px solid #4CAF50;
      border-radius: 5px;
      font-size: 1.2rem;
      color: #2e7d32;
      display: none;
    }

    /* Responsive */
    @media (max-width: 650px) {
      .main-banner h1 {
        font-size: 2rem;
        padding: 0 10px;
      }

      .container {
        margin: 15px;
        padding: 15px 20px 30px;
      }
    }
  </style>
</head>
<body>

  <!-- Main Banner -->
  <header class="main-banner">
    <img 
      src="https://www.medicaldevice-network.com/wp-content/uploads/sites/3/2021/03/AI-disease-prediction-main-image.jpg" 
      alt="AI Disease Prediction Banner"
    />
    <h1>Disease Prediction System</h1>
  </header>

  <div class="container">
    <p>Enter your symptoms below (comma separated), and click Predict to see the likely disease.</p>

    <form id="diseaseForm">
      <label for="symptoms">Symptoms:</label>
      <input
        type="text"
        id="symptoms"
        name="symptoms"
        placeholder="e.g. fever, cough, headache"
        required
      />
      <button type="submit">Predict</button>
    </form>

    <div id="result"></div>
  </div>

  <script>
    // Dummy ML prediction simulation
    // Replace with real API call or ML integration

    const diseaseMap = {
      fever: "Common Cold",
      cough: "Bronchitis",
      headache: "Migraine",
      fatigue: "Anemia",
      rash: "Allergy",
      nausea: "Food Poisoning"
    };

    const form = document.getElementById('diseaseForm');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', function(event) {
      event.preventDefault();

      const symptomsInput = document.getElementById('symptoms').value.toLowerCase();
      const symptoms = symptomsInput.split(',').map(s => s.trim());

      let predictedDiseases = new Set();

      symptoms.forEach(symptom => {
        if (diseaseMap[symptom]) {
          predictedDiseases.add(diseaseMap[symptom]);
        }
      });

      if (predictedDiseases.size === 0) {
        resultDiv.style.display = 'block';
        resultDiv.style.color = '#d32f2f';
        resultDiv.style.backgroundColor = '#ffdddd';
        resultDiv.style.borderColor = '#d32f2f';
        resultDiv.textContent = 'Sorry, no matching disease found for the given symptoms.';
      } else {
        resultDiv.style.display = 'block';
        resultDiv.style.color = '#2e7d32';
        resultDiv.style.backgroundColor = '#e9ffe9';
        resultDiv.style.borderColor = '#4CAF50';
        resultDiv.textContent = 'Likely Disease(s): ' + Array.from(predictedDiseases).join(', ');
      }
    });
  </script>
</body>
</html>
