import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Overview from './pages/Overview';
import BiDashboard from './pages/BiDashboard';
import MoviePredictor from './pages/MoviePredictor';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Overview />} />
          <Route path="bi" element={<BiDashboard />} />
          <Route path="predict" element={<MoviePredictor />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}