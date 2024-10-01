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

    try {
      const response = await fetch('http://localhost:5000/process_pdf', {
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

    const allResults = [
      ...(predictionResult.abnormal_results || []),
      ...(predictionResult.normal_results || [])
    ];

    return (
      <div className="card result-card">
        <h3>Prediction Result for {selectedDisease.charAt(0).toUpperCase() + selectedDisease.slice(1)} Disease</h3>
        <p><strong>Risk Level:</strong> <span className={predictionResult.risk_level.toLowerCase().replace(' ', '-')}>{predictionResult.risk_level}</span></p>
        <p>{predictionResult.message}</p>
        
        {allResults.length > 0 && (
          <div className="prediction-table-container">
            <h4>Relevant Test Results</h4>
            <table className="prediction-table">
              <thead>
                <tr>
                  <th>Test</th>
                  <th>Value</th>
                  <th>Normal Range</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {allResults.map((result, index) => (
                  <tr key={index} className={predictionResult.abnormal_results.some(r => r.test === result.test) ? 'abnormal' : 'normal'}>
                    <td>{result.test}</td>
                    <td>{result.value}</td>
                    <td>Up to {result.threshold}</td>
                    <td>{result.value > result.threshold ? 'Abnormal' : 'Normal'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        
        {predictionResult.test_results && Object.keys(predictionResult.test_results).length > 0 && (
          <div className="all-results-table-container">
            <h4>All Extracted Test Results</h4>
            <table className="all-results-table">
              <thead>
                <tr>
                  <th>Test</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(predictionResult.test_results).map(([test, value], index) => (
                  <tr key={index}>
                    <td>{test}</td>
                    <td>{value}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
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