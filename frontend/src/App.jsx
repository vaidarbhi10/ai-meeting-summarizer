import { Routes, Route } from "react-router-dom";
import Upload from "./pages/Upload";
import Results from "./pages/Results";
import "./App.css";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Upload />} />
      <Route path="/results" element={<Results />} />
    </Routes>
  );
}

export default App;
