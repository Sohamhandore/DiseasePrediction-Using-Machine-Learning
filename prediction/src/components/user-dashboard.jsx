import React, { useState } from "react";
import "../assets/styles/user-dashboard.css";

const DiseasePrediction = () => {
  const [file, setFile] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);
  const [selectedDisease, setSelectedDisease] = useState("liver");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please upload a PDF file");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('disease_type', selectedDisease);

    try {
      const response = await fetch('http://localhost:5000/process_pdf', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        setPredictionResult(data.prediction);
      } else {
        alert(data.error || 'An error occurred while processing the PDF');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while processing the PDF');
    }
  };

  const renderPredictionResult = () => {
    if (predictionResult === null) return null;

    return (
      <div className={`prediction-result ${predictionResult.toLowerCase().replace(' ', '-')}`}>
        {`The person has a ${predictionResult} of ${selectedDisease} disease.`}
        {predictionResult !== "Normal" && " Please consult a doctor."}
      </div>
    );
  };

  return (
    <div className="disease-prediction-dashboard">
      <nav className="disease-nav">
        <h2>Disease Prediction</h2>
        <ul>
          {["liver", "heart", "kidney"].map((disease) => (
            <li key={disease}>
              <button
                className={selectedDisease === disease ? "active" : ""}
                onClick={() => setSelectedDisease(disease)}
              >
                {disease.charAt(0).toUpperCase() + disease.slice(1)} Disease
              </button>
            </li>
          ))}
        </ul>
      </nav>
      <div className="main-content">
        <div className="prediction-content">
          <h1>
            {selectedDisease.charAt(0).toUpperCase() + selectedDisease.slice(1)}{" "}
            Disease Prediction
          </h1>
          <div className="card">
            <h3>Upload Blood Report</h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="pdfUpload">Select PDF file:</label>
                <input
                  type="file"
                  id="pdfUpload"
                  accept=".pdf"
                  onChange={handleFileChange}
                  required
                />
              </div>
              <button type="submit" className="btn-primary">Analyze Report</button>
            </form>
          </div>
          {predictionResult !== null && (
            <div className="card result-card">
              <h3>Prediction Result</h3>
              {renderPredictionResult()}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DiseasePrediction;
