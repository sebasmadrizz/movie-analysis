import { useState, useEffect } from 'react';
import { getUpcomingMovies, getPosterUrl } from '../api/tmdbClient';
 
export default function MoviePredictor() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
 
  useEffect(() => {
  getUpcomingMovies()
    .then((results) => {
      console.log('Movies received:', results);
      setMovies(results);
    })
    .catch((err) => setError(err.message))
    .finally(() => setLoading(false));
}, []);
 
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
                className="group text-left bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden hover:shadow-md hover:border-slate-300 transition-all"
              >
                <div className="aspect-[2/3] bg-slate-100">
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
    </div>
  );
}
