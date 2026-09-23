function formatValue(key, val) {
  if (val === null || val === undefined) return '—';
 
  if (typeof val !== 'number') return String(val);
 
  const lowerKey = key.toLowerCase();
 
  // ROI-style ratios → shown as multiplier (e.g. 3.50x)
  if (lowerKey.includes('roi')) {
    return `${val.toFixed(2)}x`;
  }
 
  // Percentage fields
  if (lowerKey.includes('pct') || lowerKey.includes('percent')) {
    return `${val.toFixed(2)}%`;
  }
 
  // Money fields → currency format
  const moneyKeywords = ['budget', 'revenue', 'profit', 'loss', 'box_office', 'spent'];
  if (moneyKeywords.some((kw) => lowerKey.includes(kw))) {
    return val.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  }
 
  // Plain numbers (counts, years, etc.)
  return val.toLocaleString(undefined, { maximumFractionDigits: 2 });
}
 
function getValueColor(key, val) {
  if (typeof val !== 'number') return '';
  const lowerKey = key.toLowerCase();
  const isFinancial = ['profit', 'loss', 'roi', 'net_profit', 'net_loss'].some((kw) => lowerKey.includes(kw));
  if (!isFinancial) return '';
  if (val > 0 && !lowerKey.includes('loss')) return 'text-emerald-600';
  if (val < 0 || lowerKey.includes('loss')) return 'text-red-600';
  return '';
}
 
export default function DataTable({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500 text-sm">
        No data available for this view.
      </div>
    );
  }
 
  return (
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
              {Object.entries(row).map(([key, val]) => (
                <td
                  key={key}
                  className={`px-6 py-4 whitespace-nowrap font-medium ${
                    getValueColor(key, val) || 'text-slate-800'
                  }`}
                >
                  {formatValue(key, val)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
