import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  api,
  DIFFICULTIES,
  friendlyApiError,
  PATTERNS,
  patternLabel,
  type Difficulty,
  type ProblemsQuery,
  type ProblemSummary,
} from '../api';
import { DifficultyBadge, EmptyState, ErrorBox, Spinner } from '../components/ui';

type SortKey = 'default' | 'title' | 'difficulty' | 'status';

const DIFFICULTY_ORDER: Record<string, number> = { Easy: 0, Medium: 1, Hard: 2 };

function StatusIndicators({ p }: { p: ProblemSummary }) {
  return (
    <span className="status-indicators" aria-label="status">
      {p.solved && <span className="pill pill-solved" title="Solved">✓</span>}
      {!p.solved && p.attempted && (
        <span className="pill pill-attempted" title="Attempted">•</span>
      )}
      {p.bookmarked && <span className="pill pill-bookmark" title="Bookmarked">🔖</span>}
    </span>
  );
}

export function ProblemsPage() {
  const [problems, setProblems] = useState<ProblemSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [pattern, setPattern] = useState('');
  const [difficulty, setDifficulty] = useState<Difficulty | ''>('');
  const [status, setStatus] = useState<ProblemsQuery['status']>('');
  const [sort, setSort] = useState<SortKey>('default');

  // Debounce the search box so we don't hammer the API on every keystroke.
  useEffect(() => {
    const t = window.setTimeout(() => setDebouncedSearch(search), 350);
    return () => window.clearTimeout(t);
  }, [search]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    api
      .problems({
        pattern: pattern || undefined,
        difficulty: difficulty || undefined,
        search: debouncedSearch || undefined,
        status: status || undefined,
      })
      .then((res) => {
        if (!cancelled) {
          setProblems(res.problems);
          setLoading(false);
        }
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
  }, [pattern, difficulty, debouncedSearch, status]);

  const sorted = useMemo(() => {
    const arr = [...problems];
    switch (sort) {
      case 'title':
        arr.sort((a, b) => a.title.localeCompare(b.title));
        break;
      case 'difficulty':
        arr.sort(
          (a, b) => DIFFICULTY_ORDER[a.difficulty] - DIFFICULTY_ORDER[b.difficulty],
        );
        break;
      case 'status':
        arr.sort(
          (a, b) => Number(b.solved) - Number(a.solved) || Number(b.attempted) - Number(a.attempted),
        );
        break;
      default:
        break;
    }
    return arr;
  }, [problems, sort]);

  const patternSummary = useMemo(() => {
    if (!pattern && !difficulty && !debouncedSearch && !status) {
      const byPattern: Record<string, { solved: number; total: number }> = {};
      for (const p of problems) {
        const entry = byPattern[p.pattern] ?? { solved: 0, total: 0 };
        entry.total += 1;
        if (p.solved) entry.solved += 1;
        byPattern[p.pattern] = entry;
      }
      return PATTERNS.map((pt) => {
        const entry = byPattern[pt] ?? { solved: 0, total: 0 };
        return { pattern: pt, solved: entry.solved, total: entry.total };
      });
    }
    return null;
  }, [problems, pattern, difficulty, debouncedSearch, status]);

  const solvedCount = problems.filter((p) => p.solved).length;

  return (
    <div className="page problems-page">
      <div className="problems-header">
        <div>
          <h1>Problems</h1>
          <p className="muted">
            {problems.length} shown
            {problems.length > 0 && ` · ${solvedCount} solved in this view`}
          </p>
        </div>
      </div>

      <div className="filters" role="search">
        <input
          className="input search-input"
          type="search"
          placeholder="Search problems…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          aria-label="Search problems"
        />
        <select
          className="input"
          value={pattern}
          onChange={(e) => setPattern(e.target.value)}
          aria-label="Filter by pattern"
        >
          <option value="">All patterns</option>
          {PATTERNS.map((pt) => (
            <option key={pt} value={pt}>
              {patternLabel(pt)}
            </option>
          ))}
        </select>
        <select
          className="input"
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value as Difficulty | '')}
          aria-label="Filter by difficulty"
        >
          <option value="">All difficulties</option>
          {DIFFICULTIES.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
        <select
          className="input"
          value={status}
          onChange={(e) => setStatus(e.target.value as ProblemsQuery['status'])}
          aria-label="Filter by status"
        >
          <option value="">Any status</option>
          <option value="solved">Solved</option>
          <option value="attempted">Attempted</option>
          <option value="unsolved">Unsolved</option>
          <option value="bookmarked">Bookmarked</option>
        </select>
        <select
          className="input"
          value={sort}
          onChange={(e) => setSort(e.target.value as SortKey)}
          aria-label="Sort problems"
        >
          <option value="default">Sort: default</option>
          <option value="title">Sort: title</option>
          <option value="difficulty">Sort: difficulty</option>
          <option value="status">Sort: status</option>
        </select>
      </div>

      {patternSummary && (
        <div className="pattern-summary" aria-label="Per-pattern progress">
          {patternSummary.map(({ pattern: pt, solved, total }) => (
            <Link
              key={pt}
              className="pattern-chip"
              to={`/?pattern=${pt}`}
              onClick={(e) => {
                e.preventDefault();
                setPattern(pt);
              }}
              title={`${patternLabel(pt)}: ${solved}/${total} solved`}
            >
              <span className="pattern-chip-name">{patternLabel(pt)}</span>
              <span className="pattern-chip-bar">
                <span
                  className="pattern-chip-fill"
                  style={{ width: total ? `${(solved / total) * 100}%` : '0%' }}
                />
              </span>
              <span className="pattern-chip-count">
                {solved}/{total}
              </span>
            </Link>
          ))}
        </div>
      )}

      {loading && <Spinner label="Loading problems…" />}
      {error && <ErrorBox message={error} onRetry={() => setPattern(pattern)} />}
      {!loading && !error && problems.length === 0 && (
        <EmptyState message="No problems match these filters. Try clearing them." />
      )}

      {!loading && !error && sorted.length > 0 && (
        <ol className="problem-list">
          {sorted.map((p) => (
            <li key={p.id} className="problem-row">
              <Link to={`/problem/${p.id}`} className="problem-link">
                <StatusIndicators p={p} />
                <span className="problem-title">{p.title}</span>
                <DifficultyBadge difficulty={p.difficulty} />
                <span className="problem-pattern muted">{patternLabel(p.pattern)}</span>
                <span className="problem-tags muted">{p.tags.join(', ')}</span>
              </Link>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
