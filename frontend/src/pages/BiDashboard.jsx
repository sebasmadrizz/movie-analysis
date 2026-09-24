import { useState, useMemo } from 'react';
import { useBiData } from '../hooks/useBiData';
import { biReports } from '../config/biReports';
import Sidebar from '../components/Sidebar';
import DataTable from '../components/DataTable';
 
function formatStatValue(val) {
  if (typeof val !== 'number') return val;
  if (Math.abs(val) >= 1000) {
    return val.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  }
  return val.toFixed(2);
}
 
function computeStats(data) {
  if (!data || data.length === 0) return [];
 

  const numericKeys = Object.keys(data[0]).filter(
    (key) => typeof data[0][key] === 'number'
  );
  
 
  // Pick up to 3 numeric columns to summarize (skip ids)
  const relevantKeys = numericKeys.filter((k) => !k.toLowerCase().includes('_id')).slice(0, 3);
 
  return relevantKeys.map((key) => {
    const values = data.map((row) => row[key]).filter((v) => typeof v === 'number');
    const avg = values.reduce((sum, v) => sum + v, 0) / values.length;
    return {
      label: key.replace(/_/g, ' '),
      value: formatStatValue(avg),
      sublabel: 'average',
    };
  });
}
 const LIMIT_OPTIONS = [5, 10, 25, 50];
export default function BiDashboard() {
  const [activeKey, setActiveKey] = useState(biReports[0].key);
  const [limit, setLimit] = useState(10);
  const activeReport = biReports.find((r) => r.key === activeKey);
  const endpointWithLimit = `${activeReport.endpoint}?limit=${limit}`;
  const { data, loading, error } = useBiData(endpointWithLimit);
 
  const stats = useMemo(() => computeStats(data), [data]);
 
  return (
    <div className="flex -mx-4 sm:-mx-6 lg:-mx-8 -my-8 min-h-[calc(100vh-8.5rem)]">
      <Sidebar activeKey={activeKey} onSelect={setActiveKey} />
 
      <div className="flex-1 px-6 py-8 space-y-6 overflow-x-hidden">
        {/* Header */}
        <div className="border-b border-gray-200 pb-5">
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            {activeReport.label}
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Business intelligence data pulled directly from a pre-aggregated SQL view.
          </p>
        </div>
        {/* Limit Filter */}
        <div className="flex items-center gap-2">
          <label htmlFor="limit-select" className="text-sm text-gray-500">
            Show
          </label>
          <select
            id="limit-select"
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
            className="border border-gray-300 rounded-md text-sm px-3 py-1.5 bg-white text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900"
          >
            {LIMIT_OPTIONS.map((opt) => (
              <option key={opt} value={opt}>
                {opt} rows
              </option>
            ))}
          </select>
        </div>


 
        {/* Connection Error */}
        {error && (
          <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded shadow-sm">
            <p className="font-semibold text-sm">Backend Connection Error</p>
            <p className="text-xs mt-1">{error}</p>
            <p className="text-xs text-red-500 mt-2">
              Ensure your FastAPI backend server is running at{' '}
              <code className="bg-red-100 px-1 py-0.5 rounded">http://127.0.0.1:8000</code>.
            </p>
          </div>
        )}
 
        {/* Loading */}
        {loading && !error && (
          <div className="flex flex-col items-center justify-center py-16 text-gray-500">
            <div className="w-8 h-8 border-4 border-slate-300 border-t-slate-800 rounded-full animate-spin mb-3"></div>
            <p className="text-sm font-medium">Fetching analytics from SQL engine...</p>
          </div>
        )}
 
        {/* Stat Cards */}
        {!loading && !error && stats.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
              <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Total Records</p>
              <p className="mt-2 text-2xl font-bold text-slate-900">{data.length}</p>
            </div>
            {stats.map((stat) => (
              <div key={stat.label} className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
                <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                  {stat.sublabel} {stat.label}
                </p>
                <p className="mt-2 text-2xl font-bold text-slate-900">{stat.value}</p>
              </div>
            ))}
          </div>
        )}
 
        {/* Table */}
        {!loading && !error && (
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200 bg-gray-50/50 flex justify-between items-center">
              <h2 className="text-base font-semibold text-slate-900">{activeReport.label}</h2>
              <span className="text-xs font-mono text-gray-500">
                Total records: {data.length}
              </span>
            </div>
            <DataTable data={data} />
          </div>
        )}
      </div>
    </div>
  );
}

