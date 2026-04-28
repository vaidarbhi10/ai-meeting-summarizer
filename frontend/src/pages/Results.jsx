import { useNavigate } from "react-router-dom";
import "./Results.css";

function Results() {
  const navigate = useNavigate();

  const results = JSON.parse(localStorage.getItem("results") || "null");

  if (!results) {
    return (
      <div className="app">
        <div className="container">
          <h2>No results available</h2>
          <button className="back-btn" onClick={() => navigate("/")}>
            ← Back
          </button>
        </div>
      </div>
    );
  }

  let {
    summary = "",
    keywords = [],
    actionItems = [],
    transcript = "",
    downloadUrl = "",
  } = results;

  // ensure arrays
  if (!Array.isArray(keywords)) {
    keywords = keywords.split(",").map((k) => k.trim()).filter(Boolean);
  }

  if (!Array.isArray(actionItems)) {
    actionItems = actionItems.split("\n").filter(Boolean);
  }

  return (
    <div className="app">
      <div className="container">

        <div className="header">
          <h1 className="title">📊 Meeting Results</h1>
          <button className="back-btn" onClick={() => navigate("/")}>
            ← Back
          </button>
        </div>

        <div className="results-section">

          {/* TRANSCRIPT */}
          <div className="column">
            <h2>📝 Transcript</h2>
            <p className="text">{transcript}</p>
          </div>

          {/* SUMMARY */}
          <div className="column">
            <h2>📋 Summary</h2>
            <p className="text">{summary}</p>
          </div>

          {/* KEYWORDS */}
          <div className="column">
            <h2>🏷️ Keywords</h2>
            <div className="badge-list">
              {keywords.map((k, i) => (
                <span key={i} className="badge">
                  {k}
                </span>
              ))}
            </div>
          </div>

          {/* ACTION ITEMS */}
          <div className="column">
            <h2>✅ Action Items</h2>
            <ol className="actions-list">
              {actionItems.map((a, i) => (
                <li key={i}>{a}</li>
              ))}
            </ol>
          </div>

          {/* DOWNLOAD */}
          <div className="column">
            <h2>📄 Download</h2>
            {downloadUrl ? (
              <a
                href={downloadUrl}
                target="_blank"
                rel="noreferrer"
                className="download-link"
              >
                Download PDF
              </a>
            ) : (
              <p>No PDF available</p>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}

export default Results;