import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/api";
import { toggleDarkMode } from "../utils/theme";
import "./Upload.css";

function Upload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  // Clean text helper
  const cleanText = (text) => {
    return String(text).replace(/\*+/g, "").trim();
  };

  const handleUpload = async () => {
    if (!file) {
      setError("⚠️ Please select a file first");
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

      const keywords = Array.isArray(data.keywords)
        ? data.keywords.map(cleanText)
        : String(data.keywords || "")
            .split(/[,]+/)
            .map((k) => cleanText(k))
            .filter(Boolean);

      const actionItems = Array.isArray(data.action_items)
        ? data.action_items.map(cleanText)
        : String(data.action_items || "")
            .split(/\n+/)
            .map((a) => cleanText(a))
            .filter(Boolean);

      const transcript = data.transcript || "";
      const downloadUrl = data.pdf_download_url || "";

      const resultsData = {
        summary,
        keywords,
        actionItems,
        transcript,
        downloadUrl,
      };

      localStorage.setItem("results", JSON.stringify(resultsData));
      navigate("/results");

    } catch (err) {
      console.error(err);
      setError("❌ Upload failed. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-center">
      <div className="main-card">

        {/* HEADER */}
        <div className="top-bar">
          <h1 className="title">
            🎙️ <span>AI Meeting Summarizer</span>
          </h1>

          <button className="dark-btn" onClick={toggleDarkMode}>
            🌙
          </button>
        </div>

        {/* FILE UPLOAD */}
        <div className="upload-box">
          <input
            type="file"
            accept="audio/*"
            onChange={(e) => {
              setFile(e.target.files[0]);
              setError("");
            }}
            hidden
            id="fileInput"
          />

          {!file ? (
            <label htmlFor="fileInput" className="upload-label">
              <div className="icon">📄</div>
              <h2>Choose File</h2>
              <p>Click to upload audio</p>
            </label>
          ) : (
            <div className="file-preview">
              <div className="file-left">
                <span className="file-icon">🎵</span>
                <div>
                  <h3>{file.name}</h3>
                  <p>File selected</p>
                </div>
              </div>

              <label htmlFor="fileInput" className="change-btn">
                Change
              </label>
            </div>
          )}
        </div>

        {/* BUTTON */}
        <button
          className="upload-btn"
          onClick={handleUpload}
          disabled={loading}
        >
          {loading ? "⏳ Processing..." : "🚀 Upload & Analyze"}
        </button>

        {/* ERROR */}
        {error && <p className="error-text">{error}</p>}

      </div>
    </div>
  );
}

export default Upload;