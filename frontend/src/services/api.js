/**
 * Axios API service — centralised HTTP client.
 * All backend communication goes through this module.
 */
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

// ── Response interceptor ──────────────────────────────────────
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.error ||
      error.response?.data?.message ||
      error.message ||
      'An unexpected error occurred.';
    return Promise.reject(new Error(message));
  }
);

// ── API Methods ───────────────────────────────────────────────

/**
 * Run a mental health prediction.
 * @param {Object} formData - 15-field prediction payload
 * @returns {Promise<Object>} prediction result
 */
export const predictMentalHealth = async (formData) => {
  const response = await apiClient.post('/api/predict', formData);
  return response.data.data;
};

/**
 * Get trained model evaluation metrics.
 * @returns {Promise<Object>} metrics for all 3 models
 */
export const getModelInfo = async () => {
  const response = await apiClient.get('/api/model-info');
  return response.data.data;
};

/**
 * Get wellness recommendations for a condition/severity.
 * @param {string} condition
 * @param {string} severity
 * @returns {Promise<Object>}
 */
export const getRecommendations = async (condition, severity) => {
  const response = await apiClient.get('/api/recommendations', {
    params: { condition, severity },
  });
  return response.data.data;
};

export default apiClient;
