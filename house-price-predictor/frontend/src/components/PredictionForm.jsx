import { useState } from "react";

const FIELDS = [
  // [name, label, type, min, max, step, defaultVal]
  ["bedrooms",      "Bedrooms",                 "number", 0,   33,      1,    3],
  ["bathrooms",     "Bathrooms",                "number", 0,   8,       0.25, 2],
  ["sqft_living",   "Living Area (sqft)",       "number", 290, 13540,   10,   1800],
  ["sqft_lot",      "Lot Size (sqft)",          "number", 520, 1651359, 100,  7500],
  ["floors",        "Floors",                   "number", 1,   3.5,     0.5,  1],
  ["waterfront",    "Waterfront (0 or 1)",      "number", 0,   1,       1,    0],
  ["view",          "View Quality (0–4)",       "number", 0,   4,       1,    0],
  ["condition",     "Condition (1–5)",          "number", 1,   5,       1,    3],
  ["grade",         "Grade (1–13)",             "number", 1,   13,      1,    7],
  ["sqft_above",    "Above Ground (sqft)",      "number", 290, 9410,    10,   1800],
  ["sqft_basement", "Basement (sqft)",          "number", 0,   4820,    10,   0],
  ["yr_built",      "Year Built",               "number", 1900,2015,    1,    1990],
  ["yr_renovated",  "Year Renovated (0=never)", "number", 0,   2015,    1,    0],
  ["zipcode",       "Zipcode",                  "number", 98001,98199,  1,    98178],
  ["lat",           "Latitude",                 "number", 47.1, 47.8,   0.001,47.5112],
  ["long",          "Longitude",                "number", -122.5,-121.3,0.001,-122.257],
  ["sqft_living15", "Neighbors Avg Living (sqft)", "number", 400, 6210, 10,   1340],
  ["sqft_lot15",    "Neighbors Avg Lot (sqft)",    "number", 651, 871200,100, 5650],
];

const DEFAULT_VALUES = Object.fromEntries(FIELDS.map(([name,,,,,, def]) => [name, def]));

export default function PredictionForm({ onSubmit, isLoading }) {
  const [values, setValues] = useState(DEFAULT_VALUES);
  const [errors, setErrors] = useState({});

  function handleChange(e) {
    const { name, value } = e.target;
    setValues((prev) => ({ ...prev, [name]: value === "" ? "" : Number(value) }));
    setErrors((prev) => ({ ...prev, [name]: undefined }));
  }

  function validate() {
    const errs = {};
    FIELDS.forEach(([name, label, , min, max]) => {
      const v = values[name];
      if (v === "" || v === undefined || v === null) {
        errs[name] = `${label} is required`;
      } else if (min !== undefined && v < min) {
        errs[name] = `Min ${min}`;
      } else if (max !== undefined && v > max) {
        errs[name] = `Max ${max}`;
      }
    });
    return errs;
  }

  function handleSubmit(e) {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return;
    }
    onSubmit(values);
  }

  return (
    <form onSubmit={handleSubmit} className="form-grid" noValidate>
      <div className="fields-grid">
        {FIELDS.map(([name, label, type, min, max, step]) => (
          <div key={name} className="field-group">
            <label htmlFor={name} className="field-label">
              {label}
            </label>
            <input
              id={name}
              name={name}
              type={type}
              min={min}
              max={max}
              step={step}
              value={values[name]}
              onChange={handleChange}
              className={`field-input ${errors[name] ? "field-input--error" : ""}`}
              disabled={isLoading}
            />
            {errors[name] && (
              <span className="field-error">{errors[name]}</span>
            )}
          </div>
        ))}
      </div>

      <div className="form-actions">
        <button
          type="button"
          className="btn btn--ghost"
          onClick={() => { setValues(DEFAULT_VALUES); setErrors({}); }}
          disabled={isLoading}
        >
          Reset
        </button>
        <button type="submit" className="btn btn--primary" disabled={isLoading}>
          {isLoading ? (
            <span className="btn-loading">
              <span className="spinner" /> Predicting…
            </span>
          ) : (
            "Predict Price →"
          )}
        </button>
      </div>
    </form>
  );
}