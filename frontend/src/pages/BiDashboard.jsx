import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';

export default function BiDashboard() {
  const [activeTab, setActiveTab] = useState('profitable'); // 'profitable' | 'genres'
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const endpoint = activeTab === 'profitable' 
          ? '/bi/top-profitable-movies' 
          : '/bi/genre-performance';
        const result = await apiClient(endpoint);
        setData(result || []);
      } catch (err) {
        setError(err.message || 'Failed to load BI data from server.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [activeTab]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-gray-200 pb-5">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            Business Intelligence Dashboard
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Data-driven financial insights and performance metrics extracted directly from SQL analysis.
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="mt-4 sm:mt-0 flex space-x-2 bg-slate-100 p-1 rounded-lg border border-slate-200">
          <button
            onClick={() => setActiveTab('profitable')}
            className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
              activeTab === 'profitable'
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-gray-600 hover:text-slate-900'
            }`}
          >
            Top Profitable
          </button>
          <button
            onClick={() => setActiveTab('genres')}
            className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
              activeTab === 'genres'
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-gray-600 hover:text-slate-900'
            }`}
          >
            Genre Performance
          </button>
        </div>
      </div>

      {/* Connection Error Message */}
      {error && (
        <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded shadow-sm">
          <p className="font-semibold text-sm">Backend Connection Error</p>
          <p className="text-xs mt-1">{error}</p>
          <p className="text-xs text-red-500 mt-2">
            Ensure your FastAPI backend server is running at <code className="bg-red-100 px-1 py-0.5 rounded">http://127.0.0.1:8000</code>.
          </p>
        </div>
      )}

      {/* Loading Indicator */}
      {loading && !error && (
        <div className="flex flex-col items-center justify-center py-16 text-gray-500">
          <div className="w-8 h-8 border-4 border-slate-300 border-t-slate-800 rounded-full animate-spin mb-3"></div>
          <p className="text-sm font-medium">Fetching analytics from SQL engine...</p>
        </div>
      )}

      {/* Data Table */}
      {!loading && !error && (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 bg-gray-50/50 flex justify-between items-center">
            <h2 className="text-base font-semibold text-slate-900">
              {activeTab === 'profitable' ? 'Top Profitable Movies' : 'Genre Analytics Overview'}
            </h2>
            <span className="text-xs font-mono text-gray-500">
              Total records: {data.length}
            </span>
          </div>

          {data.length === 0 ? (
            <div className="p-8 text-center text-gray-500 text-sm">
              No data available for this view.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-gray-600">
                <thead className="bg-slate-100 text-slate-700 uppercase text-xs tracking-wider">
                  <tr>
                    {Object.keys(data[0]).map((key) => (
                      <th key={key} className="px-6 py-3 font-semibold">
                        {key.replace(/_/g, ' ')}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {data.map((row, index) => (
                    <tr key={index} className="hover:bg-gray-50/80 transition-colors">
                      {Object.values(row).map((val, i) => (
                        <td key={i} className="px-6 py-4 whitespace-nowrap font-medium text-slate-800">
                          {typeof val === 'number'
                            ? val.toLocaleString(undefined, { maximumFractionDigits: 2 })
                            : String(val)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}