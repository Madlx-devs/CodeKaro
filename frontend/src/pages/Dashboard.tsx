import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  api,
  friendlyApiError,
  isAuthed,
  PATTERNS,
  patternLabel,
  type ProblemsResponse,
} from '../api';
import { useToast } from '../components/toast';
import { EmptyState, ErrorBox, Spinner } from '../components/ui';

interface DifficultyStat {
  label: string;
  solved: number;
  total: number;
}

function difficultyStats(byDifficulty: Record<string, unknown>): DifficultyStat[] {
  const out: DifficultyStat[] = [];
  for (const [label, v] of Object.entries(byDifficulty)) {
    if (typeof v === 'number') {
      out.push({ label, solved: v, total: v });
    } else if (v && typeof v === 'object') {
      const o = v as Record<string, unknown>;
      const solved = typeof o.solved === 'number' ? o.solved : 0;
      const total = typeof o.total === 'number' ? o.total : solved;
      out.push({ label, solved, total });
    }
  }
  return out;
}

function submissionField(s: Record<string, unknown>, ...keys: string[]): string {
  for (const k of keys) {
    const v = s[k];
    if (v != null && v !== '') return String(v);
  }
  return '';
}

export function DashboardPage() {
  const navigate = useNavigate();
  const toast = useToast();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<Awaited<ReturnType<typeof api.progress>> | null>(null);
  const [problemIndex, setProblemIndex] = useState<ProblemsResponse | null>(null);

  useEffect(() => {
    if (!isAuthed()) {
      navigate('/login', { replace: true });
      return;
    }
    let cancelled = false;
    setLoading(true);
    Promise.all([api.progress(), api.problems({})])
      .then(([p, probs]) => {
        if (cancelled) return;
        setProgress(p);
        setProblemIndex(probs);
        setLoading(false);
      })
      .catch((err) => {
        if (!cancelled) {
          setError(friendlyApiError(err));
          setLoading(false);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [navigate]);

  const revisionQueue = useMemo(() => {
    if (!problemIndex) return [];
    const attemptedUnsolved = problemIndex.problems.filter((p) => p.attempted && !p.solved);
    const bookmarked = problemIndex.problems.filter((p) => p.bookmarked && !p.solved);
    const seen = new Set<string>();
    const out: typeof problemIndex.problems = [];
    for (const p of [...attemptedUnsolved, ...bookmarked]) {
      if (!seen.has(p.id)) {
        seen.add(p.id);
        out.push(p);
      }
    }
    return out.slice(0, 20);
  }, [problemIndex]);

  if (!isAuthed()) return null;
  if (loading) return <Spinner label="Loading dashboard…" />;
  if (error || !progress)
    return <ErrorBox message={error ?? 'Could not load dashboard.'} />;

  const totalSolved = progress.solved;
  const totalProblems = PATTERNS.reduce(
    (acc, pt) => acc + (progress.byPattern[pt]?.total ?? 0),
    0,
  );
  const diffStats = difficultyStats(progress.byDifficulty ?? {});

  return (
    <div className="page dashboard-page">
      <h1>Dashboard</h1>

      <div className="stat-cards">
        <div className="stat-card">
          <div className="stat-value">{totalSolved}</div>
          <div className="stat-label">Solved</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{progress.attempted}</div>
          <div className="stat-label">Attempted</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{progress.streakDays}🔥</div>
          <div className="stat-label">Day streak</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            {totalProblems > 0 ? Math.round((totalSolved / totalProblems) * 100) : 0}%
          </div>
          <div className="stat-label">Completion</div>
        </div>
      </div>

      <section aria-label="Pattern progress">
        <h2>Pattern-wise progress</h2>
        <div className="progress-bars">
          {PATTERNS.map((pt) => {
            const s = progress.byPattern[pt] ?? { solved: 0, total: 0 };
            const pct = s.total > 0 ? (s.solved / s.total) * 100 : 0;
            return (
              <div key={pt} className="progress-row">
                <span className="progress-name">{patternLabel(pt)}</span>
                <span className="progress-bar">
                  <span className="progress-fill" style={{ width: `${pct}%` }} />
                </span>
                <span className="progress-count">
                  {s.solved}/{s.total}
                </span>
              </div>
            );
          })}
        </div>
      </section>

      <section aria-label="Difficulty breakdown">
        <h2>Difficulty breakdown</h2>
        {diffStats.length === 0 ? (
          <EmptyState message="No difficulty data yet." />
        ) : (
          <div className="progress-bars">
            {diffStats.map((d) => {
              const pct = d.total > 0 ? (d.solved / d.total) * 100 : 0;
              return (
                <div key={d.label} className="progress-row">
                  <span className="progress-name">{d.label}</span>
                  <span className="progress-bar">
                    <span
                      className={`progress-fill diff-fill-${d.label.toLowerCase()}`}
                      style={{ width: `${pct}%` }}
                    />
                  </span>
                  <span className="progress-count">
                    {d.solved}/{d.total}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </section>

      <section aria-label="Revision queue">
        <h2>Revision queue</h2>
        <p className="muted">Attempted but unsolved, plus your bookmarks — spaced-repetition fuel.</p>
        {revisionQueue.length === 0 ? (
          <EmptyState message="Queue is empty. Attempt a problem or bookmark one to start a revision queue." />
        ) : (
          <ol className="revision-list">
            {revisionQueue.map((p) => (
              <li key={p.id}>
                <Link to={`/problem/${p.id}`}>{p.title}</Link>
                <span className="muted"> · {patternLabel(p.pattern)}</span>
                {p.bookmarked && <span title="Bookmarked"> 🔖</span>}
              </li>
            ))}
          </ol>
        )}
      </section>

      <section aria-label="Recent submissions">
        <h2>Recent submissions</h2>
        {progress.recentSubmissions.length === 0 ? (
          <EmptyState message="No submissions yet." />
        ) : (
          <ol className="recent-list">
            {progress.recentSubmissions.slice(0, 10).map((s, i) => (
              <li key={i}>
                <span>{submissionField(s, 'problemTitle', 'problemId', 'problem', 'title')}</span>{' '}
                <span className="muted">
                  {submissionField(s, 'verdict')} {submissionField(s, 'createdAt', 'submittedAt')}
                </span>
              </li>
            ))}
          </ol>
        )}
      </section>

      <button
        className="btn"
        onClick={() => {
          api.logout();
          toast.push('Logged out.', 'info');
          navigate('/login');
        }}
      >
        Log out
      </button>
    </div>
  );
}
