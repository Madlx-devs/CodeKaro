import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api, friendlyApiError, isAuthed } from '../api';
import { useToast } from '../components/toast';

export function LoginPage() {
  const navigate = useNavigate();
  const toast = useToast();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (isAuthed()) {
    navigate('/dashboard', { replace: true });
    return null;
  }

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password) {
      setError('Enter a username and password.');
      return;
    }
    setBusy(true);
    setError(null);
    try {
      if (mode === 'login') {
        await api.login(username.trim(), password);
        toast.push(`Welcome back, ${username.trim()}!`, 'success');
      } else {
        await api.register(username.trim(), password);
        toast.push(`Account created — welcome, ${username.trim()}!`, 'success');
      }
      navigate('/dashboard');
    } catch (err) {
      setError(friendlyApiError(err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="page login-page">
      <div className="login-card">
        <h1>{mode === 'login' ? 'Log in' : 'Create account'}</h1>
        <p className="muted">
          {mode === 'login'
            ? 'Your solutions, notes and streaks are saved to your account.'
            : 'Pick a username and password to track progress across sessions.'}
        </p>
        <div className="tabs" role="tablist" aria-label="Auth mode">
          {(['login', 'register'] as const).map((m) => (
            <button
              key={m}
              role="tab"
              aria-selected={mode === m}
              className={`tab ${mode === m ? 'active' : ''}`}
              onClick={() => {
                setMode(m);
                setError(null);
              }}
            >
              {m === 'login' ? 'Log in' : 'Register'}
            </button>
          ))}
        </div>
        <form onSubmit={submit} className="login-form">
          <label>
            Username
            <input
              className="input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
              aria-label="Username"
            />
          </label>
          <label>
            Password
            <input
              className="input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
              aria-label="Password"
            />
          </label>
          {error && (
            <div className="error-box" role="alert">
              {error}
            </div>
          )}
          <button className="btn btn-primary" type="submit" disabled={busy}>
            {busy ? 'Please wait…' : mode === 'login' ? 'Log in' : 'Create account'}
          </button>
        </form>
        <p className="muted">
          You can browse and solve problems without an account; logging in saves
          submissions, notes and streaks.
        </p>
      </div>
    </div>
  );
}
