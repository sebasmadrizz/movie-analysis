function DebutBadge({ isDebut, label }) {
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
        isDebut ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700'
      }`}
    >
      {label}: {isDebut ? 'No historical data' : 'Has track record'}
    </span>
  );
}
 
function formatCurrency(val) {
  if (!val && val !== 0) return '—';
  return val.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
}
 
export default function PredictionModal({
  movie,
  posterUrl,
  requestData,
  credits,
  prediction,
  loading,
  error,
  onClose,
}) {
  if (!movie) return null;
 
  return (
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start gap-4 p-6 border-b border-gray-200">
          {posterUrl && (
            <img
              src={posterUrl}
              alt={movie.title}
              className="w-20 rounded-md shrink-0 shadow-sm"
            />
          )}
          <div className="flex-1 min-w-0">
            <h2 className="text-xl font-bold text-slate-900">{movie.title}</h2>
            <p className="text-sm text-gray-500 mt-1">{movie.release_date}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl leading-none"
            aria-label="Close"
          >
            &times;
          </button>
        </div>
 
        {/* Body */}
        <div className="p-6 space-y-5">
          {loading && (
            <div className="flex items-center gap-3 text-gray-500 text-sm py-8 justify-center">
              <div className="w-5 h-5 border-2 border-slate-300 border-t-slate-800 rounded-full animate-spin"></div>
              Fetching details and running prediction...
            </div>
          )}
 
          {error && <p className="text-sm text-red-600">Error: {error}</p>}
 
          {requestData && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
              <div>
                <p className="text-xs text-gray-500 uppercase">Budget</p>
                <p className="font-semibold text-slate-900">{formatCurrency(requestData.budget)}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase">Runtime</p>
                <p className="font-semibold text-slate-900">{requestData.runtime} min</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase">Genres</p>
                <p className="font-semibold text-slate-900">{requestData.genres.join(', ')}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase">Release Date</p>
                <p className="font-semibold text-slate-900">{requestData.release_date}</p>
              </div>
            </div>
          )}
 
          {credits && prediction && (
            <div className="border-t border-gray-200 pt-5 space-y-2 text-sm">
              <p>
                <span className="text-gray-500">Director:</span>{' '}
                <span className="font-medium text-slate-900">{credits.directorName}</span>
              </p>
              <p>
                <span className="text-gray-500">Cast:</span>{' '}
                <span className="font-medium text-slate-900">{credits.castNames.join(', ')}</span>
              </p>
              <p>
                <span className="text-gray-500">Studio:</span>{' '}
                <span className="font-medium text-slate-900">{credits.studioName}</span>
              </p>
              <div className="flex flex-wrap gap-2 pt-2">
                <DebutBadge isDebut={prediction.director_is_debut} label="Director" />
                <DebutBadge isDebut={prediction.cast_is_debut} label="Cast" />
                <DebutBadge isDebut={prediction.studio_is_debut} label="Studio" />
              </div>
            </div>
          )}
 
          {prediction && (
            <div className="border-t border-gray-200 pt-5">
              <p className="text-xs text-gray-500 uppercase">Predicted Revenue</p>
              <p className="text-3xl font-bold text-emerald-600">
                {formatCurrency(prediction.predicted_revenue)}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
