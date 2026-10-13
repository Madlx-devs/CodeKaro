import { useEffect, useState } from 'react';
import { HashRouter, Link, NavLink, Route, Routes, useNavigate } from 'react-router-dom';
import { clearToken, isAuthed } from './api';
import { ToastProvider, useToast } from './components/toast';
import { DashboardPage } from './pages/Dashboard';
import { LoginPage } from './pages/Login';
import { ProblemsPage } from './pages/Problems';
import { WorkspacePage } from './pages/Workspace';

function Nav() {
  const [authed, setAuthed] = useState(isAuthed());
  const navigate = useNavigate();
  const toast = useToast();

  // Re-check auth state on every navigation.
  useEffect(() => {
    setAuthed(isAuthed());
  });

  return (
    <header className="nav">
      <Link to="/" className="nav-brand" aria-label="DSA Practice Platform home">
        <span className="nav-mark" aria-hidden="true">&lt;/&gt;</span>
        DSA Platform
      </Link>
      <nav className="nav-links" aria-label="Primary">
        <NavLink to="/" end className={({ isActive }) => (isActive ? 'active' : '')}>
          Problems
        </NavLink>
        <NavLink to="/dashboard" className={({ isActive }) => (isActive ? 'active' : '')}>
          Dashboard
        </NavLink>
      </nav>
      <div className="nav-right">
        {authed ? (
          <button
            className="btn btn-sm"
            onClick={() => {
              clearToken();
              setAuthed(false);
              toast.push('Logged out.', 'info');
              navigate('/');
            }}
          >
            Log out
          </button>
        ) : (
          <Link to="/login" className="btn btn-sm">
            Log in
          </Link>
        )}
      </div>
    </header>
  );
}

function NotFound() {
  return (
    <div className="page">
      <h1>Page not found</h1>
      <p className="muted">
        <Link to="/">Back to problems</Link>
      </p>
    </div>
  );
}

export function App() {
  useEffect(() => {
    if (!document.documentElement.dataset.theme) {
      document.documentElement.dataset.theme = localStorage.getItem('dsa_theme') || 'dark';
    }
  }, []);

  return (
    <HashRouter>
      <ToastProvider>
        <div className="app">
          <Nav />
          <main className="main">
            <Routes>
              <Route path="/" element={<ProblemsPage />} />
              <Route path="/problem/:id" element={<WorkspacePage />} />
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
          <footer className="footer muted">
            Solve real Java, run real tests. Shortcuts: Ctrl/⌘+Enter runs your code.
          </footer>
        </div>
      </ToastProvider>
    </HashRouter>
  );
}
