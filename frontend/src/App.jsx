
import { useState, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);
  const fileInputRef = useRef();

  const API = import.meta.env.VITE_API_URL;

  const handleUpload = async () => {
    if (!file) return alert("Please select a file");
    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);
    try {
      const res = await axios.post(`${API}/upload`, formData);
      setResult(res.data);
    } catch (err) {
      alert("Upload failed");
    }
    setLoading(false);
  };

  const fetchAnalytics = async () => {
    setAnalyticsLoading(true);
    try {
      const res = await axios.get(`${API}/analytics`);
      setAnalytics(res.data);
    } catch (err) {
      alert("Failed to load analytics");
    }
    setAnalyticsLoading(false);
  };

  const sd = result?.structured_data;

  return (
    <div className="app">
      <div className="header">
        <h1 className="logo">📄 InvoiceAI</h1>
        <span className="tagline">Extraction Tool</span>
      </div>

      <main className="main">

        {/* Upload */}
        <div className="card">
          <h2 className="card-title">Upload Invoice</h2>
          <div
            className="dropzone"
            onClick={() => fileInputRef.current.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              style={{ display: "none" }}
              onChange={(e) => setFile(e.target.files[0])}
            />
            {file ? (
              <p className="file-selected">✓ {file.name}</p>
            ) : (
              <p className="file-prompt">Click to choose a file <span>(PDF, JPG, PNG)</span></p>
            )}
          </div>
          <button
            className="btn btn-primary"
            onClick={handleUpload}
            disabled={!file || loading}
          >
            {loading ? "Processing..." : "Extract Data"}
          </button>
        </div>

        {/* Result */}
        {result && (
          <div className="card">
            <h2 className="card-title">Extracted Data</h2>
            {sd ? (
              <div>
                <table className="data-table">
                  <tbody>
                    {[
                      ["Vendor", sd.vendor_name],
                      ["Invoice No.", sd.invoice_number],
                      ["Date", sd.invoice_date],
                      ["Amount", sd.total_amount],
                      ["Currency", sd.currency],
                      ["Confidence", result.confidence],
                    ].map(([label, value]) => (
                      <tr key={label}>
                        <td className="table-label">{label}</td>
                        <td className="table-value">{value ?? "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <pre className="json-out">{JSON.stringify(result, null, 2)}</pre>
            )}
          </div>
        )}

        {/* Analytics */}
        <div className="card">
          <h2 className="card-title">Analytics</h2>
          <button
            className="btn btn-secondary"
            onClick={fetchAnalytics}
            disabled={analyticsLoading}
          >
            {analyticsLoading ? "Loading..." : analytics ? "Refresh" : "Load Analytics"}
          </button>
          {analytics && (
            <pre className="json-out" style={{ marginTop: "14px" }}>
              {JSON.stringify(analytics, null, 2)}
            </pre>
          )}
        </div>

      </main>
    </div>
  );
}

export default App;