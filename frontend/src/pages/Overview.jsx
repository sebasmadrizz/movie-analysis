import { Link } from 'react-router-dom';

const REPO_URL = 'https://github.com/sebasmadrizz/movie-analysis';

const stats = [
  { value: '11', label: 'BI reports' },
  { value: '3,498', label: 'Movies in training set' },
  { value: '0.50', label: 'R² on test set' },
  { value: '5', label: 'SQL pipeline stages' },
];

const features = [
  {
    title: 'Business Intelligence',
    description:
      'Eleven SQL-driven reports on profitability, ROI, genres, directors, actors, studios and flops. Heavy aggregation happens once in PostgreSQL views, not on every request.',
    to: '/bi',
    linkLabel: 'Explore the reports →',
  },
  {
    title: 'Feature Engineering in SQL',
    description:
      'Leakage-safe window functions, genre-relative budget normalization and explicit cold-start handling turn a skewed, noisy dataset into learnable signal before Python touches it.',
    href: `${REPO_URL}/tree/main/sql`,
    linkLabel: 'See the SQL on GitHub →',
  },
  {
    title: 'Revenue Predictor',
    description:
      'Pick an upcoming movie pulled live from TMDB. Its director, cast and studio are resolved against the historical dataset and fed to the model, with flags when there is no track record.',
    to: '/predict',
    linkLabel: 'Try the predictor →',
  },
];

const pipeline = [
  { name: 'Ingest', detail: 'Kaggle CSVs loaded into staging tables' },
  { name: 'Transform', detail: 'JSON parsed into an analytics schema' },
  { name: 'Analyze', detail: 'Eleven BI views in SQL' },
  { name: 'Feature store', detail: 'Leakage-safe ML features' },
  { name: 'Train', detail: 'Tuned gradient boosting model' },
  { name: 'Serve', detail: 'FastAPI backend, React frontend' },
];

const stack = [
  'PostgreSQL',
  'Docker',
  'Python',
  'scikit-learn',
  'FastAPI',
  'React',
  'Vite',
  'Tailwind CSS',
  'TMDB API',
];

const focusRing =
  'focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2';

// All three hero buttons share this style so none looks "already selected"
const ctaButton = `inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-white text-slate-900 text-sm font-medium border border-gray-300 shadow-sm hover:bg-slate-900 hover:text-white hover:border-slate-900 transition-colors ${focusRing}`;

function StrokeIcon({ children }) {
  return (
    <svg
      className="w-4 h-4"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {children}
    </svg>
  );
}

function GitHubIcon() {
  return (
    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
    </svg>
  );
}

export default function Overview() {
  return (
    <div className="space-y-16">
      {/* Hero */}
      <section className="pt-4 space-y-6">
        <span className="inline-block text-xs font-medium px-3 py-1 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
          Portfolio project
        </span>
        <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-slate-900 max-w-3xl">
          From raw movie data to a revenue prediction platform
        </h1>
        <p className="text-lg text-gray-600 leading-relaxed max-w-2xl">
          A dataset of 5,000 movies turned into a full analytics stack: SQL-based business
          intelligence, a feature store built in PostgreSQL, and a revenue model served through a
          REST API.
        </p>
        <div className="flex flex-wrap items-center gap-3 pt-2">
          <Link to="/bi" className={ctaButton}>
            <StrokeIcon>
              <path d="M3 3v18h18" />
              <path d="M7 16v-5" />
              <path d="M12 16V8" />
              <path d="M17 16v-9" />
            </StrokeIcon>
            Explore Business Intelligence
          </Link>
          <Link to="/predict" className={ctaButton}>
            <StrokeIcon>
              <polyline points="22 7 13.5 15.5 8.5 10.5 2 17" />
              <polyline points="16 7 22 7 22 13" />
            </StrokeIcon>
            Try the Revenue Predictor
          </Link>
          <a href={REPO_URL} target="_blank" rel="noopener noreferrer" className={ctaButton}>
            <GitHubIcon />
            View on GitHub
          </a>
        </div>
      </section>

      {/* Stats */}
      <section className="space-y-3">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat) => (
            <div
              key={stat.label}
              className="bg-white rounded-xl border border-gray-200 shadow-sm p-5"
            >
              <p className="text-3xl font-bold text-slate-900">{stat.value}</p>
              <p className="mt-1 text-xs font-medium text-gray-500 uppercase tracking-wide">
                {stat.label}
              </p>
            </div>
          ))}
        </div>
        <p className="text-xs text-gray-500">
          The training set keeps only movies with a budget and revenue above $10,000 and a known
          release date.
        </p>
      </section>

      {/* What's inside */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold tracking-tight text-slate-900">What&apos;s inside</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="bg-white rounded-xl border border-gray-200 shadow-sm p-6 flex flex-col"
            >
              <h3 className="text-base font-semibold text-slate-900">{feature.title}</h3>
              <p className="mt-2 text-sm text-gray-600 leading-relaxed flex-1">
                {feature.description}
              </p>
              {feature.to ? (
                <Link
                  to={feature.to}
                  className={`mt-4 text-sm font-medium text-slate-900 hover:underline rounded ${focusRing}`}
                >
                  {feature.linkLabel}
                </Link>
              ) : (
                <a
                  href={feature.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`mt-4 text-sm font-medium text-slate-900 hover:underline rounded ${focusRing}`}
                >
                  {feature.linkLabel}
                </a>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Pipeline */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold tracking-tight text-slate-900">How it works</h2>
        <ol className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {pipeline.map((step, index) => (
            <li key={step.name} className="bg-white rounded-lg border border-gray-200 p-4">
              <span className="text-xs font-mono text-gray-400">
                {String(index + 1).padStart(2, '0')}
              </span>
              <p className="mt-1 text-sm font-semibold text-slate-900">{step.name}</p>
              <p className="mt-1 text-xs text-gray-500 leading-relaxed">{step.detail}</p>
            </li>
          ))}
        </ol>
        <p className="text-sm text-gray-600 max-w-2xl leading-relaxed">
          Every stage is a standalone script paired with its own SQL file and its own tests. The
          API is layered (router → service → repository), so each layer has one job and the SQL
          stays in one place.
        </p>
      </section>

      {/* Stack */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold tracking-tight text-slate-900">Built with</h2>
        <ul className="flex flex-wrap gap-2">
          {stack.map((tech) => (
            <li
              key={tech}
              className="px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-sm border border-slate-200"
            >
              {tech}
            </li>
          ))}
        </ul>
        <p className="text-xs text-gray-500">
          The model is a baseline (R² ≈ 0.50 on the test set) and is still being improved.
        </p>
      </section>
    </div>
  );
}