import { useState } from "react";
import API from "../api/api";

export default function UploadBox() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select an audio file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file); // MUST match backend

    try {
      setLoading(true);

      const res = await API.post("/upload", formData, {
        responseType: "blob",
      });

      // ✅ FIX: Ensure proper PDF type
      const blob = new Blob([res.data], {
        type: "application/pdf",
      });

      const url = window.URL.createObjectURL(blob);

      // ✅ AUTO DOWNLOAD (BEST UX)
      const link = document.createElement("a");
      link.href = url;
      link.download = "meeting-summary.pdf";
      document.body.appendChild(link);
      link.click();

      // cleanup
      link.remove();
      window.URL.revokeObjectURL(url);

    } catch (error) {
      console.log("Upload Error:", error);
      alert("Upload failed. Check backend or CORS.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1>🎙️ AI Meeting Summarizer</h1>

      <input
        type="file"
        accept="audio/*"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button style={styles.button} onClick={handleUpload}>
        {loading ? "Processing..." : "Upload & Generate PDF"}
      </button>

      {loading && <p>⏳ Processing audio... Please wait</p>}
    </div>
  );
}

const styles = {
  container: {
    textAlign: "center",
    marginTop: "80px",
    fontFamily: "Arial",
  },
  button: {
    padding: "10px 20px",
    marginTop: "10px",
    cursor: "pointer",
    backgroundColor: "#000",
    color: "#fff",
    border: "none",
    borderRadius: "6px",
  },
};