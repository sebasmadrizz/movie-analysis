import React from 'react';
import { useBiData } from '../hooks/useBiData';

export default function Dashboard() {
  const { data: movies, loading, error } = useBiData('/bi/top-profitable-movies?limit=10');

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '1000px', margin: '0 auto' }}>
      <h1>Movie Analysis Platform</h1>
      <p>Business Intelligence - Top Profitable Movies</p>

      {loading && <p>Cargando datos de BI...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {!loading && !error && (
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
          <thead>
            <tr style={{ backgroundColor: '#f2f2f2', textAlign: 'left' }}>
              <th style={{ padding: '10px', border: '1px solid #ddd' }}>Película</th>
              <th style={{ padding: '10px', border: '1px solid #ddd' }}>Presupuesto</th>
              <th style={{ padding: '10px', border: '1px solid #ddd' }}>Ingresos</th>
              <th style={{ padding: '10px', border: '1px solid #ddd' }}>Beneficio Neto</th>
            </tr>
          </thead>
          <tbody>
            {movies.map((movie, index) => (
              <tr key={index}>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>{movie.title || movie.original_title || 'N/D'}</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>${Number(movie.budget || 0).toLocaleString()}</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>${Number(movie.revenue || 0).toLocaleString()}</td>
                <td style={{ padding: '10px', border: '1px solid #ddd', color: 'green', fontWeight: 'bold' }}>
                  ${Number(movie.net_profit || 0).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}