import { useState } from "react";
import API from "./api/api";
import Loader from "./components/Loader";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [pdfUrl, setPdfUrl] = useState("");
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setError("");
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select an audio file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setPdfUrl("");
      setError("");

      const res = await API.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      setPdfUrl(url);
    } catch (err) {
      console.error(err);

      if (err.response) {
        const serverMessage = err.response.data?.error || err.response.data || err.response.statusText;
        setError(`Upload failed: ${serverMessage}`);
      } else if (err.request) {
        setError("Upload failed: no response from backend. Please verify the backend is running.");
      } else {
        setError(`Upload failed: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1 className="title">🎙️ AI Meeting Summarizer</h1>
          <p className="subtitle">
            Upload your meeting audio and get an instant summary with keywords and action items
          </p>
        </header>

        <section className="upload-section">
          <label htmlFor="file-input" className="file-input-label">
            📁 Choose Audio File
          </label>
          <input
            id="file-input"
            type="file"
            accept="audio/*"
            onChange={handleFileChange}
            className="file-input"
          />

          {file && (
            <div className="file-name">
              Selected: {file.name}
            </div>
          )}

          <button
            onClick={handleUpload}
            className="upload-btn"
            disabled={loading || !file}
          >
            {loading ? "🔄 Processing..." : "🚀 Upload & Generate Summary"}
          </button>
        </section>

        {loading && (
          <section className="loading-section">
            <Loader />
          </section>
        )}

        {pdfUrl && (
          <section className="download-section">
            <a href={pdfUrl} download="meeting-summary.pdf" className="download-link">
              📄 Download Meeting Summary PDF
            </a>
          </section>
        )}

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;