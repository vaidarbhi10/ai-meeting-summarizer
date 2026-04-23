import "./Loader.css";

export default function Loader() {
  return (
    <div className="loader-container">
      <div className="loader-spinner"></div>
      <div className="loader-text">
        <h3>⏳ Processing your meeting audio...</h3>
        <p>This may take a few minutes depending on the audio length</p>
      </div>
    </div>
  );
}