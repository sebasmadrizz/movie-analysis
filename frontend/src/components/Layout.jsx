import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';

export default function Layout() {
  const location = useLocation();

  const navLinks = [
    { name: 'Overview', path: '/' },
    { name: 'Business Intelligence', path: '/bi' },
    { name: 'ML Predictor', path: '/predict' },
  ];

  return (
    <div className="min-h-screen bg-customBg text-customTextH flex flex-col font-sans">
      {/* Top Navbar */}
      <header className="bg-slate-900 text-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="text-xl font-bold tracking-wide text-customAccent">
              Movie Analytics
            </span>
            <span className="text-xs bg-slate-800 text-gray-300 px-2 py-1 rounded border border-slate-700">
              Portfolio Project
            </span>
          </div>
          <nav className="flex space-x-1 sm:space-x-4">
            {navLinks.map((link) => {
              const isActive = location.pathname === link.path;
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-customAccentBg text-customAccent border border-customAccentBorder'
                      : 'text-gray-300 hover:bg-slate-800 hover:text-white'
                  }`}
                >
                  {link.name}
                </Link>
              );
            })}
          </nav>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Aquí se inyectarán las páginas (Overview, BI, Predictor) */}
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-customBorder py-4 text-center text-xs text-customText">
        Movie Analysis Platform — Built with FastAPI, PostgreSQL, and React.
      </footer>
    </div>
  );
}