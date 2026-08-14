/**
 * Custom hook: manages prediction form state and API call.
 */
import { useState, useCallback } from 'react';
import { predictMentalHealth } from '../services/api';
import { validateForm } from '../utils/validators';

const INITIAL_FORM = {
  age: '',
  gender: '',
  occupation: '',
  sleep_hours: '',
  sleep_quality: '',
  social_media_hours: '',
  academic_work_pressure: '',
  physical_activity_days: '',
  stress_level: '',
  anxiety_score: '',
  depression_score: '',
  work_life_balance: '',
  mood_score: '',
  concentration_level: '',
  social_support: '',
};

export function usePrediction() {
  const [formData, setFormData]     = useState(INITIAL_FORM);
  const [errors, setErrors]         = useState({});
  const [result, setResult]         = useState(null);
  const [loading, setLoading]       = useState(false);
  const [apiError, setApiError]     = useState(null);

  const updateField = useCallback((name, value) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear field error on change
    if (errors[name]) {
      setErrors((prev) => { const e = { ...prev }; delete e[name]; return e; });
    }
  }, [errors]);

  const resetForm = useCallback(() => {
    setFormData(INITIAL_FORM);
    setErrors({});
    setResult(null);
    setApiError(null);
  }, []);

  const submit = useCallback(async () => {
    setApiError(null);
    const { isValid, errors: validationErrors } = validateForm(formData);

    if (!isValid) {
      setErrors(validationErrors);
      return false;
    }

    setLoading(true);
    try {
      // Coerce string numbers to actual numbers
      const payload = {};
      Object.entries(formData).forEach(([k, v]) => {
        const num = parseFloat(v);
        payload[k] = isNaN(num) ? v : num;
      });

      const prediction = await predictMentalHealth(payload);
      setResult(prediction);
      return true;
    } catch (err) {
      setApiError(err.message);
      return false;
    } finally {
      setLoading(false);
    }
  }, [formData]);

  return {
    formData,
    errors,
    result,
    loading,
    apiError,
    updateField,
    resetForm,
    submit,
  };
}
