export const biReports = [
  { key: 'profitable', label: 'Top Profitable', endpoint: '/bi/top-profitable-movies', category: 'Movies' },
  { key: 'roi', label: 'Top ROI', endpoint: '/bi/top-roi-movies', category: 'Movies' },
  { key: 'flops', label: 'Financial Flops', endpoint: '/bi/top-financial-flops', category: 'Movies' },
  { key: 'directors', label: 'Top Directors', endpoint: '/bi/top-directors', category: 'People' },
  { key: 'actors', label: 'Top Lead Actors', endpoint: '/bi/top-lead-actors', category: 'People' },
  { key: 'worst-directors', label: 'Worst Directors', endpoint: '/bi/worst-performing-directors', category: 'People' },
  { key: 'lowest-roi-actors', label: 'Lowest ROI Actors', endpoint: '/bi/lowest-roi-lead-actors', category: 'People' },
  { key: 'duos', label: 'Director-Actor Duos', endpoint: '/bi/director-actor-duos', category: 'People' },
  { key: 'studios', label: 'Production Companies', endpoint: '/bi/production-company-performance', category: 'Studios' },
  { key: 'genres', label: 'Genre Performance', endpoint: '/bi/genre-performance', category: 'Genre' },
  { key: 'critical', label: 'Critical vs Commercial', endpoint: '/bi/critical-vs-commercial-matrix', category: 'Genre' },
];
