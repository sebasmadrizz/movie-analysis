import { useState, useEffect } from 'react';
import { getUpcomingMovies } from '../api/tmdbClient';

export default function MoviePredictor() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getUpcomingMovies()
      .then((results) => setMovies(results))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading upcoming movies...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Upcoming Movies</h1>
      <ul className="space-y-2">
        {movies.map((movie) => (
          <li key={movie.id} className="border-b pb-2">
            <strong>{movie.title}</strong> — {movie.release_date}
          </li>
        ))}
      </ul>
    </div>
  );
}