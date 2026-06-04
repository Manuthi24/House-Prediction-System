const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Send house features to the backend and get a price prediction.
 * @param {Object} features - House feature values matching HouseFeatures schema
 * @returns {Promise<{predicted_price: number, formatted_price: string, confidence_range: Object, model_version: string}>}
 */
export async function predictPrice(features) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(features),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Server error: ${response.status}`);
  }

  return response.json();
}

/**
 * Check backend health and model status.
 * @returns {Promise<Object>}
 */
export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) throw new Error("Backend unreachable");
  return response.json();
}