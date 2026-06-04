export default function ResultCard({ result, onReset }) {
  if (!result) return null;

  const { formatted_price, confidence_range, model_version } = result;

  return (
    <div className="result-card">
      <div className="result-header">
        <span className="result-eyebrow">Estimated Market Value</span>
        <h2 className="result-price">{formatted_price}</h2>
      </div>

      <div className="result-range">
        <div className="range-bar-wrapper">
          <span className="range-label">Low</span>
          <div className="range-bar">
            <div className="range-fill" />
          </div>
          <span className="range-label">High</span>
        </div>
        <div className="range-values">
          <span className="range-value">{confidence_range.low}</span>
          <span className="range-caption">±12% confidence range</span>
          <span className="range-value">{confidence_range.high}</span>
        </div>
      </div>

      <div className="result-meta">
        <span className="meta-badge">King County, WA</span>
        <span className="meta-badge">Model v{model_version}</span>
        <span className="meta-badge">Gradient Boosting</span>
      </div>

      <button className="btn btn--outline result-btn" onClick={onReset}>
        ← Try Another House
      </button>
    </div>
  );
}