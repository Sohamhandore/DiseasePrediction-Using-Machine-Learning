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

    // Mock prediction (replace with actual API call)
    const mockPrediction = Math.random() > 0.5;
    setPredictionResult(mockPrediction);
  };

  const renderPredictionResult = () => {
    if (predictionResult === null) return null;

    const diseaseMessages = {
      liver: "liver disease",
      heart: "heart disease",
      kidney: "kidney disease",
    };

    const message = diseaseMessages[selectedDisease];

    return (
      <div
        className={`prediction-result ${
          predictionResult ? "positive" : "negative"
        }`}
      >
        {predictionResult
          ? `The person may have ${message}. Please consult a doctor.`
          : `The person is likely not to have ${message}.`}
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
