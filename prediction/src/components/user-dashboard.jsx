import React, { useState, useRef } from "react";
import "../assets/styles/user-dashboard.css";

const UserDashboard = () => {
  const [file, setFile] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);
  const [selectedDisease, setSelectedDisease] = useState("liver");
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setPredictionResult(null);
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

    console.log('File being sent:', file);
    console.log('FormData contents:');
    for (let [key, value] of formData.entries()) {
      console.log(key, value);
    }

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        setPredictionResult(data);
      } else {
        alert(data.error || 'An error occurred while processing the PDF');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while processing the PDF');
    }

    setFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const renderPredictionResult = () => {
    if (!predictionResult) return null;

    return (
      <div className="card result-card">
        <h3>Prediction Result for {selectedDisease.charAt(0).toUpperCase() + selectedDisease.slice(1)} Disease</h3>
        <p><strong>Risk Level:</strong> <span className={predictionResult.risk_level.toLowerCase().replace(' ', '-')}>{predictionResult.risk_level}</span></p>
        <p>{predictionResult.message}</p>
        
        {predictionResult.patient_info && Object.keys(predictionResult.patient_info).length > 0 && (
          <div className="patient-info">
            <h4>Patient Information:</h4>
            <pre>
              {Object.entries(predictionResult.patient_info).map(([key, value]) => (
                `${key}: ${value}\n`
              )).join('')}
            </pre>
          </div>
        )}
        
        {predictionResult.table_data && predictionResult.table_data.length > 0 ? (
          <div className="prediction-table-container">
            <h4>Test Results</h4>
            <table className="prediction-table">
              <thead>
                <tr>
                  <th>Parameter</th>
                  <th>Tested Value</th>
                  <th>Unit</th>
                  <th>Normal Range</th>
                </tr>
              </thead>
              <tbody>
                {predictionResult.table_data.map((row, index) => (
                  <tr key={index}>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                    <td>{row[2]}</td>
                    <td>{row[3]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p>No test results found in the uploaded PDF.</p>
        )}
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
                <label htmlFor="pdfUpload" className="file-upload-label">
                  Select PDF file
                  <input
                    type="file"
                    id="pdfUpload"
                    accept=".pdf"
                    onChange={handleFileChange}
                    ref={fileInputRef}
                    className="file-input"
                  />
                </label>
                {file && (
                  <span className="files-selected">
                    1 file selected
                  </span>
                )}
              </div>
              <button type="submit" className="btn-primary">Analyze Report</button>
            </form>
          </div>
          {renderPredictionResult()}
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;