import { useState, useEffect } from 'react';
import {
  getUpcomingMovies,
  getMovieDetails,
  getPosterUrl,
  mapTmdbMovieToPredictionRequest,
  validatePredictionRequest,
} from '../api/tmdbClient';
import { predictRevenue } from '../api/client';
import PredictionModal from '../components/PredictionModal';

export default function MoviePredictor() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [selectedMovie, setSelectedMovie] = useState(null);
  const [requestData, setRequestData] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [panelLoading, setPanelLoading] = useState(false);
  const [panelError, setPanelError] = useState(null);
  const [credits, setCredits] = useState(null);
  const [missingFields, setMissingFields] = useState(null);

  useEffect(() => {
    getUpcomingMovies()
      .then((results) => setMovies(results))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const handleSelectMovie = async (movie) => {
    setSelectedMovie(movie);
    setPanelLoading(true);
    setPanelError(null);
    setRequestData(null);
    setPrediction(null);
    setCredits(null);
    setMissingFields(null);

    try {
      const details = await getMovieDetails(movie.id);
      const request = mapTmdbMovieToPredictionRequest(details);
      const missing = validatePredictionRequest(request);
      if (missing) {
        setMissingFields(missing);
        return;
      }
      setRequestData(request);

      const director = details.credits.crew.find((p) => p.job === 'Director');
      const topCast = [...details.credits.cast].sort((a, b) => a.order - b.order).slice(0, 3);
      const studio = details.production_companies[0];
      setCredits({
        directorName: director?.name ?? 'Unknown',
        castNames: topCast.map((c) => c.name),
        studioName: studio?.name ?? 'Unknown',
      });

      const result = await predictRevenue(request);
      setPrediction(result);
    } catch (err) {
      setPanelError(err.message);
    } finally {
      setPanelLoading(false);
    }
  };

  const handleCloseModal = () => {
    setSelectedMovie(null);
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-5">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Revenue Predictor
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Pick an upcoming movie to predict its box office revenue using our model.
        </p>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded shadow-sm">
          <p className="font-semibold text-sm">TMDB Connection Error</p>
          <p className="text-xs mt-1">{error}</p>
        </div>
      )}

      {loading && !error && (
        <div className="flex flex-col items-center justify-center py-16 text-gray-500">
          <div className="w-8 h-8 border-4 border-slate-300 border-t-slate-800 rounded-full animate-spin mb-3"></div>
          <p className="text-sm font-medium">Fetching upcoming movies...</p>
        </div>
      )}

      {!loading && !error && (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {movies.map((movie) => {
            const posterUrl = getPosterUrl(movie.poster_path);
            return (
              <button
                key={movie.id}
                onClick={() => handleSelectMovie(movie)}
                className="group text-left bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden hover:shadow-md hover:border-slate-300 transition-all"
              >
                <div className="aspect-[2/3] bg-slate-100 relative">
                  {posterUrl ? (
                    <img
                      src={posterUrl}
                      alt={movie.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-xs text-gray-400 p-2 text-center">
                      No poster available
                    </div>
                  )}
                  <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-colors flex items-center justify-center">
                    <span className="text-white text-sm font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
                      Predict Revenue →
                    </span>
                  </div>
                </div>
                <div className="p-3">
                  <p className="text-sm font-semibold text-slate-900 line-clamp-2">
                    {movie.title}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">{movie.release_date}</p>
                </div>
              </button>
            );
          })}
        </div>
      )}

      <PredictionModal
        movie={selectedMovie}
        posterUrl={selectedMovie ? getPosterUrl(selectedMovie.poster_path) : null}
        requestData={requestData}
        credits={credits}
        prediction={prediction}
        loading={panelLoading}
        error={panelError}
        onClose={handleCloseModal}
        missingFields={missingFields}
      />
    </div>
  );
}
