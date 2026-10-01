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
  return data.results;
}
 
export async function getMovieDetails(movieId) {
  return tmdbFetch(`/movie/${movieId}?append_to_response=credits&language=en-US`);
}
 
