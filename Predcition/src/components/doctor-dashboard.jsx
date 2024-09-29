import React, { useState, useRef } from "react";
import "../assets/styles/doctor-dashboard.css";

const DoctorDashboard = () => {
  const [files, setFiles] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [selectedDisease, setSelectedDisease] = useState("liver");
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const newFiles = Array.from(e.target.files);
    setFiles(prevFiles => {
      const updatedFiles = [...prevFiles];
      newFiles.forEach(file => {
        if (!updatedFiles.some(f => f.name === file.name)) {
          updatedFiles.push(file);
        }
      });
      return updatedFiles;
    });
    // Clear predictions when new files are uploaded
    setPredictions([]);
  };

  const handleRemoveFile = (index) => {
    setFiles(prevFiles => prevFiles.filter((_, i) => i !== index));
    // Clear predictions when a file is removed
    setPredictions([]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (files.length === 0) {
      alert("Please upload at least one PDF file");
      return;
    }

    // Mock predictions (replace with actual API calls)
    const mockPredictions = files.map((file) => ({
      fileName: file.name,
      prediction: Math.random() > 0.5,
    }));
    setPredictions(mockPredictions);

    // Clear the selected files
    setFiles([]);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const renderPredictionTable = () => {
    if (predictions.length === 0) return null;

    return (
      <div className="prediction-table-container">
        <table className="prediction-table">
          <thead>
            <tr>
              <th>File Name</th>
              <th>Prediction</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map((pred, index) => (
              <tr key={index}>
                <td>{pred.fileName}</td>
                <td className={pred.prediction ? "positive" : "negative"}>
                  {pred.prediction
                    ? `May have ${selectedDisease} disease`
                    : `Likely not to have ${selectedDisease} disease`}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const renderFileList = () => {
    if (files.length === 0) return null;

    return (
      <div className="uploaded-files">
        <h4>Uploaded Files ({files.length})</h4>
        <ul>
          {files.map((file, index) => (
            <li key={index}>
              <span className="file-name">{file.name}</span>
              <button onClick={() => handleRemoveFile(index)} className="remove-file" aria-label="Remove file">
                &times;
              </button>
            </li>
          ))}
        </ul>
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
            <h3>Upload Multiple Blood Reports</h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="pdfUpload" className="file-upload-label">
                  Select PDF files
                  <input
                    type="file"
                    id="pdfUpload"
                    accept=".pdf"
                    onChange={handleFileChange}
                    multiple
                    ref={fileInputRef}
                    className="file-input"
                  />
                </label>
                {files.length > 0 && (
                  <span className="files-selected">
                    {files.length} file(s) selected
                  </span>
                )}
              </div>
              {renderFileList()}
              <button type="submit" className="btn-primary">Analyze Reports</button>
            </form>
          </div>
          {predictions.length > 0 && (
            <div className="card result-card">
              <h3>Prediction Results</h3>
              {renderPredictionTable()}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DoctorDashboard;
