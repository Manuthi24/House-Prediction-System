import { useState } from "react";
import PredictionForm from "./components/PredictionForm";
import ResultCard from "./components/ResultCard";
import { predictPrice } from "./api/predict";
import "./index.css";

export default function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(features) {
    setIsLoading(true);
    setError(null);
    try {
      const data = await predictPrice(features);
      setResult(data);
    } catch (err) {
      setError(err.message || "Prediction failed. Is the backend running?");
    } finally {
      setIsLoading(false);
    }
  }

  function handleReset() {
    setResult(null);
    setError(null);
  }

  return (
    <div className="app">
      {/* Background decoration */}
      <div className="bg-grid" aria-hidden="true" />
      <div className="bg-glow bg-glow--1" aria-hidden="true" />
      <div className="bg-glow bg-glow--2" aria-hidden="true" />

      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">⌂</span>
            <span className="logo-text">HomeVal</span>
          </div>
          <p className="header-sub">King County House Price Predictor · Seattle Metro</p>
        </div>
      </header>

      <main className="main">
        {!result ? (
          <section className="card form-card">
            <div className="card-header">
              <h1 className="card-title">Estimate Your Home's Value</h1>
              <p className="card-desc">
                Fill in the property details below. Our Gradient Boosting model — trained on
                21,000+ King County sales — will predict the market price instantly.
              </p>
            </div>

            {error && (
              <div className="error-banner" role="alert">
                <span className="error-icon">⚠</span>
                <span>{error}</span>
              </div>
            )}

            <PredictionForm onSubmit={handleSubmit} isLoading={isLoading} />
          </section>
        ) : (
          <section className="card result-wrapper">
            <ResultCard result={result} onReset={handleReset} />
          </section>
        )}
      </main>

      <footer className="footer">
        <p>
          Built with FastAPI + scikit-learn · Trained on{" "}
          <a
            href="https://www.kaggle.com/datasets/harlfoxem/housesalesprediction"
            target="_blank"
            rel="noopener noreferrer"
          >
            KC House Data
          </a>
        </p>
      </footer>
    </div>
  );
}