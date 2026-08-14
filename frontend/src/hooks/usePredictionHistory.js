/**
 * Custom hook: manages prediction history in localStorage.
 */
import { useState, useCallback, useEffect } from 'react';

const STORAGE_KEY = 'mhp_prediction_history';
const MAX_HISTORY = 10;

export function usePredictionHistory() {
  const [history, setHistory] = useState([]);

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) setHistory(JSON.parse(stored));
    } catch {
      setHistory([]);
    }
  }, []);

  const saveToHistory = useCallback((result, formData) => {
    const entry = {
      id:        Date.now(),
      timestamp: new Date().toISOString(),
      result,
      formData,
    };

    setHistory((prev) => {
      const updated = [entry, ...prev].slice(0, MAX_HISTORY);
      try { localStorage.setItem(STORAGE_KEY, JSON.stringify(updated)); } catch {}
      return updated;
    });
  }, []);

  const deleteEntry = useCallback((id) => {
    setHistory((prev) => {
      const updated = prev.filter((e) => e.id !== id);
      try { localStorage.setItem(STORAGE_KEY, JSON.stringify(updated)); } catch {}
      return updated;
    });
  }, []);

  const clearHistory = useCallback(() => {
    setHistory([]);
    try { localStorage.removeItem(STORAGE_KEY); } catch {}
  }, []);

  return { history, saveToHistory, deleteEntry, clearHistory };
}
