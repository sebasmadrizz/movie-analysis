import { biReports } from '../config/biReports';
 
function groupByCategory(reports) {
  return reports.reduce((groups, report) => {
    if (!groups[report.category]) {
      groups[report.category] = [];
    }
    groups[report.category].push(report);
    return groups;
  }, {});
}
 
export default function Sidebar({ activeKey, onSelect }) {
  const grouped = groupByCategory(biReports);
 
  return (
    <aside className="w-64 shrink-0 border-r border-gray-200 bg-white">
      <nav className="py-6 px-3 space-y-6">
        {Object.entries(grouped).map(([category, reports]) => (
          <div key={category}>
            <h3 className="px-3 mb-2 text-xs font-semibold uppercase tracking-wider text-gray-400">
              {category}
            </h3>
            <div className="space-y-1">
              {reports.map((report) => (
                <button
                  key={report.key}
                  onClick={() => onSelect(report.key)}
                  className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeKey === report.key
                      ? 'bg-slate-900 text-white'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-slate-900'
                  }`}
                >
                  {report.label}
                </button>
              ))}
            </div>
          </div>
        ))}
      </nav>
    </aside>
  );
}
 
