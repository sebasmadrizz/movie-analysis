import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '../api/client';

export function useBiData(endpoint) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    if (!endpoint) return;
    try {
      setLoading(true);
      setError(null);
      const result = await apiClient(endpoint);
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}