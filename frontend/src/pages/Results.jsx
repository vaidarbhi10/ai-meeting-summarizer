import { useLocation, useNavigate } from "react-router-dom";
import "./Results.css";

function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const results = location.state?.results;

  if (!results) {
    return (
      <div className="app">
        <div className="container">
          <div className="no-results">
            <h2>No results available</h2>
            <button onClick={() => navigate("/")} className="back-btn">
              ← Back to Upload
            </button>
          </div>
        </div>
      </div>
    );
  }

  const { summary, keywords, actionItems, speakers, downloadUrl } = results;

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1 className="title">📊 Meeting Analysis Results</h1>
          <button onClick={() => navigate("/")} className="back-btn">
            ← Upload Another Meeting
          </button>
        </header>

        <section className="results-section">
          <div className="columns">
            <div className="column summary-column">
              <h2 className="section-title">📋 Meeting Summary</h2>
              <p className="summary-text">{summary}</p>
            </div>

            <div className="column keywords-column">
              <h2 className="section-title">🏷️ Keywords</h2>
              {keywords.length > 0 ? (
                <div className="badge-list">
                  {keywords.map((keyword, index) => (
                    <span key={index} className="badge">
                      {keyword}
                    </span>
                  ))}
                </div>
              ) : (
                <p>No keywords available.</p>
              )}
            </div>

            <div className="column action-column">
              <h2 className="section-title">✅ Action Items</h2>
              {actionItems.length > 0 ? (
                <ul className="actions-list">
                  {actionItems.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              ) : (
                <p>No action items available.</p>
              )}
            </div>

            <div className="column">
              <h2 className="section-title">📄 Download</h2>
              {downloadUrl ? (
                <a href={downloadUrl} download="meeting-summary.pdf" className="download-link">
                  📄 Download Meeting Summary PDF
                </a>
              ) : (
                <p>PDF will be available after processing.</p>
              )}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Results;
