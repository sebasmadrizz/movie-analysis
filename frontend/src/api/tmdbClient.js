const TMDB_BASE_URL = 'https://api.themoviedb.org/3';
const TMDB_TOKEN = import.meta.env.VITE_TMDB_TOKEN;
 
async function tmdbFetch(path) {
  const response = await fetch(`${TMDB_BASE_URL}${path}`, {
    headers: {
      Authorization: `Bearer ${TMDB_TOKEN}`,
      accept: 'application/json',
    },
  });
 
  if (!response.ok) {
    throw new Error(`TMDB request failed: ${response.status}`);
  }
 
  return response.json();
}
 
export async function getUpcomingMovies(page = 1) {
  const data = await tmdbFetch(`/movie/upcoming?language=en-US&page=${page}`);
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - 60);
  const cutoffStr = cutoff.toISOString().split('T')[0];
  return data.results.filter((movie) => movie.release_date >= cutoffStr);
}
export async function getMovieDetails(movieId) {
  return tmdbFetch(`/movie/${movieId}?append_to_response=credits&language=en-US`);
}

export function getPosterUrl(posterPath, size = 'w342') {
  if (!posterPath) return null;
  return `https://image.tmdb.org/t/p/${size}${posterPath}`;
}
 
export function mapTmdbMovieToPredictionRequest(movieDetails) {
  const director = movieDetails.credits.crew.find((person) => person.job === 'Director');
  const topCast = [...movieDetails.credits.cast]
    .sort((a, b) => a.order - b.order)
    .slice(0, 3);
  const studio = movieDetails.production_companies[0];

  return {
    budget: movieDetails.budget,
    runtime: movieDetails.runtime,
    genres: movieDetails.genres.map((g) => g.name),
    release_date: movieDetails.release_date,
    director_id: director ? director.id : null,
    cast_ids: topCast.map((c) => c.id),
    studio_id: studio ? studio.id : null,
    is_sequel: 0,
    original_language_code: movieDetails.original_language,
  };
}