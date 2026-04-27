import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/api";
import Loader from "../components/Loader";
import "./Upload.css";

function Upload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const cleanText = (text) => {
    return String(text).replace(/\*+/g, "").trim();
  };

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
      setError("");

      const res = await API.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const data = res.data;
      const summary = cleanText(data.summary || "");
      const cleanedKeywords = Array.isArray(data.keywords)
        ? data.keywords.map(cleanText)
        : String(data.keywords).split(/[\n,]+/).map((item) => cleanText(item)).filter(Boolean);
      const cleanedActions = Array.isArray(data.action_items)
        ? data.action_items.map(cleanText)
        : String(data.action_items).split(/[\n]+/).map((item) => cleanText(item)).filter(Boolean);
      const speakers = Array.isArray(data.speakers) ? data.speakers : [];
      const baseUrl = API.defaults.baseURL || "";
      const downloadUrl = data.pdf_download_url ? `${baseUrl}${data.pdf_download_url}` : "";

      const resultsData = {
        summary,
        keywords: cleanedKeywords,
        actionItems: cleanedActions,
        speakers,
        downloadUrl,
      };

      navigate("/results", { state: { results: resultsData } });
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
            <div className="file-name">Selected: {file.name}</div>
          )}

          <button
            onClick={handleUpload}
            className="upload-btn"
            disabled={loading || !file}
          >
            {loading ? "🔄 Processing..." : "🚀 Upload & Analyze Meeting"}
          </button>
        </section>

        {loading && (
          <section className="loading-section">
            <Loader />
          </section>
        )}

        {error && (
          <div className="error-message">⚠️ {error}</div>
        )}
      </div>
    </div>
  );
}

export default Upload;
