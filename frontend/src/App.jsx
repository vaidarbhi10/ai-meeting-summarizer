import { useState } from "react";
import API from "./api/api";
import Loader from "./components/Loader";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [pdfUrl, setPdfUrl] = useState("");

  const handleUpload = async () => {
    if (!file) {
      alert("Please select an audio file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setPdfUrl("");

      const res = await API.post("/upload", formData, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      setPdfUrl(url);
    } catch (err) {
      console.log(err);
      alert("Upload failed. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🎙️ AI Meeting Summarizer</h1>

      <input
        type="file"
        accept="audio/*"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={handleUpload} className="btn">
        Upload & Generate PDF
      </button>

      {loading && <Loader />}

      {pdfUrl && (
        <div style={{ marginTop: "20px" }}>
          <a href={pdfUrl} download="meeting-summary.pdf">
            📄 Download PDF
          </a>
        </div>
      )}
    </div>
  );
}

export default App;