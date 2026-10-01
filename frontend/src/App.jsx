import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import BiDashboard from './pages/BiDashboard';
import MoviePredictor from './pages/MoviePredictor';

function Overview() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight text-slate-900">Project Overview</h1>
      <p className="text-gray-600 leading-relaxed">
        A personal portfolio project that turns a raw dataset of 5,000 movies into a full analytics platform — from SQL-based business intelligence to a revenue prediction model served through a REST API.
      </p>
    </div>
  );
}


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