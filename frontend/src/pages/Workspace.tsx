import Editor, { type OnMount } from '@monaco-editor/react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import {
  api,
  CODE_LANGUAGES,
  friendlyApiError,
  isAuthed,
  patternLabel,
  type AiLevel,
  type CodeLanguage,
  type ProblemDetail,
  type ProblemSummary,
  type RunResponse,
  type RunTestResult,
  type SubmitResponse,
  type TestCase,
} from '../api';
import { defineDsaThemes, registerJavaCompletions } from '../editor/monacoJava';
import { Markdown } from '../components/Markdown';
import { ResizablePanels } from '../components/ResizablePanels';
import { useToast } from '../components/toast';
import {
  DifficultyBadge,
  EmptyState,
  ErrorBox,
  Modal,
  Spinner,
} from '../components/ui';

type LeftTab = 'description' | 'submissions' | 'notes';
type RightTab = 'tests' | 'console';

type Theme = 'dark' | 'light';

interface AiPanel {
  title: string;
  content: string; // markdown
}

const LEVELS: AiLevel[] = ['beginner', 'intermediate', 'advanced'];

const LANG_LABELS: Record<CodeLanguage, string> = {
  java: 'Java',
  python: 'Python',
  cpp: 'C++',
};

const LANG_STORAGE_KEY = (problemId: string, lang: CodeLanguage) =>
  `dsa_code_${problemId}_${lang}`;
const LANG_PREF_KEY = (problemId: string) => `dsa_lang_${problemId}`;

/** Starter code for a language, falling back to the legacy Java `starterCode` for java. */
function starterFor(p: ProblemDetail, lang: CodeLanguage): string {
  return p.starterCodes?.[lang] ?? (lang === 'java' ? p.starterCode : '');
}

/**
 * Load the editor content for a problem+language: per-language draft first,
 * then a one-time migration from the legacy `dsa_code_<problemId>` key,
 * then the language's starter code.
 */
function loadDraft(problem: ProblemDetail, lang: CodeLanguage): string {
  const perKey = LANG_STORAGE_KEY(problem.id, lang);
  const legacyKey = `dsa_code_${problem.id}`;
  try {
    const per = localStorage.getItem(perKey);
    if (per != null) return per;
    const legacy = localStorage.getItem(legacyKey);
    if (legacy != null) {
      // One-time migration: claim the legacy draft for this language.
      localStorage.setItem(perKey, legacy);
      localStorage.removeItem(legacyKey);
      return legacy;
    }
  } catch {
    // storage blocked — non-fatal, fall through to the starter
  }
  return starterFor(problem, lang);
}

function readStoredLanguage(problemId: string): CodeLanguage {
  try {
    const v = localStorage.getItem(LANG_PREF_KEY(problemId));
    if (v === 'java' || v === 'python' || v === 'cpp') return v;
  } catch {
    // storage blocked — non-fatal
  }
  return 'java';
}

function verdictClass(v: string): string {
  const lower = v.toLowerCase();
  if (lower.includes('accepted')) return 'v-accepted';
  if (lower.includes('wrong')) return 'v-wrong';
  if (lower.includes('compilation')) return 'v-compile';
  if (lower.includes('runtime')) return 'v-runtime';
  if (lower.includes('time limit')) return 'v-tle';
  if (lower.includes('memory')) return 'v-mle';
  return '';
}

function AiNotConfiguredNotice() {
  return (
    <div className="ai-notice">
      <div className="ai-notice-title">🤖 AI not configured</div>
      <p>
        The server has no AI API key set. To enable AI features, set{' '}
        <code>OPENAI_API_KEY</code> on the server (optionally{' '}
        <code>OPENAI_BASE_URL</code> / <code>OPENAI_MODEL</code>) and restart
        the backend.
      </p>
    </div>
  );
}

export function WorkspacePage() {
  const { id } = useParams<{ id: string }>();
  const toast = useToast();

  const [problem, setProblem] = useState<ProblemDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  const [code, setCode] = useState('');
  const [lang, setLang] = useState<CodeLanguage>('java');
  const [theme, setTheme] = useState<Theme>(() =>
    localStorage.getItem('dsa_theme') === 'light' ? 'light' : 'dark',
  );
  const [fontSize, setFontSize] = useState<number>(() =>
    Number(localStorage.getItem('dsa_fontsize')) || 14,
  );

  const [leftTab, setLeftTab] = useState<LeftTab>('description');
  const [rightTab, setRightTab] = useState<RightTab>('tests');

  const [customTests, setCustomTests] = useState<TestCase[]>([]);
  const [runResult, setRunResult] = useState<RunResponse | null>(null);
  const [running, setRunning] = useState(false);
  const [submitResult, setSubmitResult] = useState<SubmitResponse | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const [aiPanel, setAiPanel] = useState<AiPanel | null>(null);
  const [aiLoading, setAiLoading] = useState<string | null>(null);
  const [aiError, setAiError] = useState<string | null>(null);
  const [aiNotConfigured, setAiNotConfigured] = useState(false);
  const [hintLevel, setHintLevel] = useState<1 | 2 | 3>(1);
  const [aiLevel, setAiLevel] = useState<AiLevel>(
    () => (localStorage.getItem('dsa_ai_level') as AiLevel) || 'beginner',
  );

  const [note, setNote] = useState('');
  const [savingNote, setSavingNote] = useState(false);
  const [bookmarked, setBookmarked] = useState(false);
  const [submissions, setSubmissions] = useState<Awaited<ReturnType<typeof api.submissions>>>([]);
  const [submissionsLoading, setSubmissionsLoading] = useState(false);

  const [allProblems, setAllProblems] = useState<ProblemSummary[]>([]);
  const [helpOpen, setHelpOpen] = useState(false);

  const editorRef = useRef<Parameters<OnMount>[0] | null>(null);
  const runRef = useRef<() => void>(() => {});

  // ------------------------------------------------------------------ load
  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    setLoading(true);
    setLoadError(null);
    setRunResult(null);
    setSubmitResult(null);
    setAiPanel(null);
    setAiError(null);
    setAiNotConfigured(false);
    setCustomTests([]);
    const initialLang = readStoredLanguage(id);
    setLang(initialLang);
    api
      .problem(id)
      .then((p) => {
        if (cancelled) return;
        setProblem(p);
        setBookmarked(!!p.bookmarked);
        setNote(p.note ?? '');
        setCode(loadDraft(p, initialLang));
        setLoading(false);
      })
      .catch((err) => {
        if (!cancelled) {
          setLoadError(friendlyApiError(err));
          setLoading(false);
        }
      });
    api
      .problems({})
      .then((res) => {
        if (!cancelled) setAllProblems(res.problems);
      })
      .catch(() => {
        // Non-fatal: prev/next/related just won't show.
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  // Persist code draft per problem AND language (debounced).
  useEffect(() => {
    if (!id || !problem) return;
    const t = window.setTimeout(() => {
      try {
        localStorage.setItem(LANG_STORAGE_KEY(id, lang), code);
      } catch {
        // storage full/blocked — non-fatal
      }
    }, 500);
    return () => window.clearTimeout(t);
  }, [code, id, lang, problem]);

  // Persist the selected language per problem.
  useEffect(() => {
    if (!id) return;
    try {
      localStorage.setItem(LANG_PREF_KEY(id), lang);
    } catch {
      // storage blocked — non-fatal
    }
  }, [id, lang]);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem('dsa_theme', theme);
  }, [theme]);

  useEffect(() => {
    localStorage.setItem('dsa_fontsize', String(fontSize));
  }, [fontSize]);

  useEffect(() => {
    localStorage.setItem('dsa_ai_level', aiLevel);
  }, [aiLevel]);

  // ------------------------------------------------------------------ run
  const runCode = useCallback(async () => {
    if (!problem || running) return;
    setRunning(true);
    setRunResult(null);
    setSubmitResult(null);
    setRightTab('tests');
    try {
      const tests: TestCase[] = [
        ...problem.sampleTests.map((t) => ({ input: t.input, expected: t.expected })),
        ...customTests.filter((t) => t.input.trim() !== '' || t.expected.trim() !== ''),
      ];
      const res = await api.run({ problemId: problem.id, mode: 'method', code, tests, language: lang });
      setRunResult(res);
      if (!res.compiled) {
        setRightTab('console');
        toast.push('Compilation failed — see the Console tab.', 'error');
      } else {
        const passed = res.results.filter((r) => r.passed).length;
        toast.push(
          `${passed}/${res.results.length} tests passed.`,
          passed === res.results.length && res.results.length > 0 ? 'success' : 'info',
        );
      }
    } catch (err) {
      toast.push(friendlyApiError(err), 'error');
    } finally {
      setRunning(false);
    }
  }, [problem, running, code, customTests, lang, toast]);
  runRef.current = runCode;

  const submitCode = useCallback(async () => {
    if (!problem || submitting) return;
    setSubmitting(true);
    setSubmitResult(null);
    try {
      const res = await api.submit({ problemId: problem.id, code, language: lang });
      setSubmitResult(res);
      if (res.verdict === 'Accepted') {
        toast.push(`Accepted! ${res.passedCount}/${res.totalCount} hidden tests passed.`, 'success');
      } else {
        toast.push(`Verdict: ${res.verdict}`, 'error');
      }
    } catch (err) {
      toast.push(friendlyApiError(err), 'error');
    } finally {
      setSubmitting(false);
    }
  }, [problem, submitting, code, lang, toast]);

  // ------------------------------------------------------------------ language
  const switchLanguage = useCallback(
    (next: CodeLanguage) => {
      if (!problem || next === lang) return;
      // Save the outgoing draft under its own per-language key before swapping.
      try {
        localStorage.setItem(LANG_STORAGE_KEY(problem.id, lang), code);
      } catch {
        // storage blocked — non-fatal
      }
      setLang(next);
      // Previous run/submit results belong to a different language's code.
      setRunResult(null);
      setSubmitResult(null);
      setCode(loadDraft(problem, next));
    },
    [problem, lang, code],
  );

  const handleMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;
    defineDsaThemes(monaco);
    registerJavaCompletions(monaco);
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
      runRef.current();
    });
  };

  // ------------------------------------------------------------------ AI
  const openAi = useCallback(
    async (title: string, call: () => Promise<{ content: string }>, after?: () => void) => {
      setAiPanel(null);
      setAiError(null);
      setAiNotConfigured(false);
      setAiLoading(title);
      try {
        const res = await call();
        setAiPanel({ title, content: res.content });
        after?.();
      } catch (err) {
        if (err instanceof Error && 'status' in err && (err as { status: number }).status === 503) {
          setAiNotConfigured(true);
          setAiPanel({ title, content: '' });
        } else {
          setAiError(friendlyApiError(err));
        }
      } finally {
        setAiLoading(null);
      }
    },
    [],
  );

  const askUnderstand = () =>
    problem && openAi('Understand This Question', () => api.aiUnderstand(problem.id, aiLevel));
  const askAnalogy = () =>
    problem && openAi('🧠 Explain with an Analogy', () => api.aiAnalogy(problem.id, aiLevel));
  const askHint = () => {
    if (!problem) return;
    const level = hintLevel;
    openAi(`Get a Hint (level ${level}/3)`, () => api.aiHint(problem.id, code, level), () => {
      setHintLevel(((level % 3) + 1) as 1 | 2 | 3);
    });
  };
  const askExplainCode = () =>
    openAi('Explain My Code', () => api.aiExplainCode(problem?.id, code, aiLevel));
  const askComplexity = async () => {
    if (!code.trim()) {
      toast.push('Write some code first, then analyze it.', 'info');
      return;
    }
    setAiPanel(null);
    setAiError(null);
    setAiNotConfigured(false);
    setAiLoading('Analyze Complexity');
    try {
      const res = await api.complexity({ code });
      const md = [
        '## Complexity Analysis',
        '',
        `**Estimated time complexity:** \`${res.time}\``,
        `**Estimated auxiliary space complexity:** \`${res.space}\``,
        `**Confidence:** ${res.confidence} (heuristic estimate, not a proof)`,
        '',
        '### Why',
        res.explanation,
        '',
        res.signals.length > 0 ? '### Signals detected' : '',
        ...res.signals.map((s) => `- ${s}`),
        '',
        `> ⚠️ ${res.caveat}`,
      ].join('\n');
      setAiPanel({ title: 'Analyze Complexity', content: md });
    } catch (err) {
      setAiError(friendlyApiError(err));
    } finally {
      setAiLoading(null);
    }
  };

  // ------------------------------------------------------------------ misc
  const resetCode = () => {
    if (!problem) return;
    if (
      window.confirm(
        `Reset the ${LANG_LABELS[lang]} editor to the starter code? Your current code will be lost.`,
      )
    ) {
      setCode(starterFor(problem, lang));
      try {
        localStorage.removeItem(LANG_STORAGE_KEY(problem.id, lang));
      } catch {
        // storage blocked — non-fatal
      }
      toast.push('Editor reset to starter code.', 'info');
    }
  };

  const toggleBookmark = async () => {
    if (!problem) return;
    if (!isAuthed()) {
      toast.push('Log in to bookmark problems.', 'error');
      return;
    }
    try {
      await api.bookmark(problem.id, !bookmarked);
      setBookmarked(!bookmarked);
      toast.push(!bookmarked ? 'Bookmarked.' : 'Bookmark removed.', 'success');
    } catch (err) {
      toast.push(friendlyApiError(err), 'error');
    }
  };

  const saveNote = async () => {
    if (!problem || savingNote) return;
    if (!isAuthed()) {
      toast.push('Log in to save notes.', 'error');
      return;
    }
    setSavingNote(true);
    try {
      await api.saveNote(problem.id, note);
      toast.push('Note saved.', 'success');
    } catch (err) {
      toast.push(friendlyApiError(err), 'error');
    } finally {
      setSavingNote(false);
    }
  };

  const loadSubmissions = useCallback(async () => {
    if (!id || !isAuthed()) return;
    setSubmissionsLoading(true);
    try {
      setSubmissions(await api.submissions(id));
    } catch {
      setSubmissions([]);
    } finally {
      setSubmissionsLoading(false);
    }
  }, [id]);

  useEffect(() => {
    if (leftTab === 'submissions') loadSubmissions();
  }, [leftTab, loadSubmissions]);

  const { prev, next, related } = useMemo(() => {
    if (!id || allProblems.length === 0) return { prev: null, next: null, related: [] as ProblemSummary[] };
    const idx = allProblems.findIndex((p) => p.id === id);
    if (idx === -1) return { prev: null, next: null, related: [] as ProblemSummary[] };
    const same = allProblems.filter((p) => p.pattern === allProblems[idx].pattern && p.id !== id);
    return {
      prev: idx > 0 ? allProblems[idx - 1] : null,
      next: idx < allProblems.length - 1 ? allProblems[idx + 1] : null,
      related: same.slice(0, 6),
    };
  }, [allProblems, id]);

  if (loading) return <Spinner label="Loading problem…" />;
  if (loadError || !problem)
    return <ErrorBox message={loadError ?? 'Problem not found.'} />;

  const runResultsByIndex = new Map<number, RunTestResult>();
  runResult?.results.forEach((r) => runResultsByIndex.set(r.index, r));

  const javaSignatureText = `class ${problem.signature.className} {\n    public ${problem.signature.returnType} ${problem.signature.methodName}(${problem.signature.params
    .map((p) => `${p.type} ${p.name}`)
    .join(', ')})\n}`;
  const signatureText =
    lang === 'java'
      ? javaSignatureText
      : (problem.methodSignatures?.[lang] ?? javaSignatureText);

  return (
    <div className="workspace">
      <ResizablePanels
        left={
          <div className="panel-body">
            <div className="tabs" role="tablist" aria-label="Problem info tabs">
              {(['description', 'submissions', 'notes'] as LeftTab[]).map((t) => (
                <button
                  key={t}
                  role="tab"
                  aria-selected={leftTab === t}
                  className={`tab ${leftTab === t ? 'active' : ''}`}
                  onClick={() => setLeftTab(t)}
                >
                  {t === 'description' ? 'Description' : t === 'submissions' ? 'Submissions' : 'Notes'}
                </button>
              ))}
            </div>

            {leftTab === 'description' && (
              <div className="desc">
                <div className="desc-header">
                  <h1>{problem.title}</h1>
                  <div className="desc-meta">
                    <DifficultyBadge difficulty={problem.difficulty} />
                    <span className="chip">{patternLabel(problem.pattern)}</span>
                    <button
                      className={`btn btn-sm ${bookmarked ? 'btn-active' : ''}`}
                      onClick={toggleBookmark}
                      aria-pressed={bookmarked}
                      title={bookmarked ? 'Remove bookmark' : 'Bookmark this problem'}
                    >
                      {bookmarked ? '🔖 Bookmarked' : '🔖 Bookmark'}
                    </button>
                  </div>
                </div>

                <div className="desc-section desc-text">{problem.description}</div>

                {problem.examples.map((ex, i) => (
                  <div key={i} className="example">
                    <div className="example-title">Example {i + 1}</div>
                    <pre className="example-block">
                      <strong>Input:</strong> {ex.input}
                      {'\n'}
                      <strong>Output:</strong> {ex.output}
                      {ex.explanation ? `\n${ex.explanation}` : ''}
                    </pre>
                  </div>
                ))}

                <div className="desc-section">
                  <div className="desc-section-title">Constraints</div>
                  <ul className="constraints">
                    {problem.constraints.map((c, i) => (
                      <li key={i}>
                        <code>{c}</code>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="desc-section">
                  <div className="desc-section-title">
                    Method signature{' '}
                    <span className="muted chip chip-sm">{LANG_LABELS[lang]}</span>
                  </div>
                  <pre className="signature-block">{signatureText}</pre>
                </div>

                <div className="desc-section">
                  <div className="desc-section-title">Expected complexity</div>
                  <p>
                    Time: <code>{problem.timeComplexity}</code> · Space:{' '}
                    <code>{problem.spaceComplexity}</code>
                  </p>
                  <div className="tags">
                    {problem.tags.map((t) => (
                      <span key={t} className="chip chip-sm">
                        {t}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="desc-section prev-next">
                  <div>
                    {prev && (
                      <Link className="nav-link" to={`/problem/${prev.id}`}>
                        ← {prev.title}
                      </Link>
                    )}
                  </div>
                  <div>
                    {next && (
                      <Link className="nav-link" to={`/problem/${next.id}`}>
                        {next.title} →
                      </Link>
                    )}
                  </div>
                </div>

                {related.length > 0 && (
                  <div className="desc-section">
                    <div className="desc-section-title">Related problems</div>
                    <ul className="related-list">
                      {related.map((r) => (
                        <li key={r.id}>
                          <Link to={`/problem/${r.id}`}>{r.title}</Link>{' '}
                          <DifficultyBadge difficulty={r.difficulty} />
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {leftTab === 'submissions' && (
              <div className="desc">
                {!isAuthed() && (
                  <EmptyState message="Log in to see your submission history for this problem." />
                )}
                {isAuthed() && submissionsLoading && <Spinner label="Loading submissions…" />}
                {isAuthed() && !submissionsLoading && submissions.length === 0 && (
                  <EmptyState message="No submissions yet. Run or submit your code to start." />
                )}
                {isAuthed() && !submissionsLoading && submissions.length > 0 && (
                  <ol className="submission-list">
                    {submissions.map((s, i) => (
                      <li key={String(s.id ?? i)} className="submission-row">
                        <span className={`verdict-badge ${verdictClass(String(s.verdict ?? ''))}`}>
                          {String(s.verdict ?? '—')}
                        </span>
                        <span className="muted">
                          {s.passedCount != null && s.totalCount != null
                            ? `${s.passedCount}/${s.totalCount}`
                            : ''}
                        </span>
                        <span className="muted">
                          {String(s.createdAt ?? s.submittedAt ?? '')}
                        </span>
                      </li>
                    ))}
                  </ol>
                )}
              </div>
            )}

            {leftTab === 'notes' && (
              <div className="desc notes-tab">
                <div className="desc-section-title">Your notes</div>
                <textarea
                  className="input notes-area"
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                  placeholder="Mistakes, insights, revision reminders…"
                  aria-label="Problem notes"
                />
                <button className="btn" onClick={saveNote} disabled={savingNote}>
                  {savingNote ? 'Saving…' : 'Save note'}
                </button>
                {!isAuthed() && (
                  <p className="muted">Log in to persist notes on the server.</p>
                )}
              </div>
            )}
          </div>
        }
        center={
          <div className="editor-wrap">
            <div className="ai-toolbar" aria-label="AI learning assistant">
              <button className="btn btn-sm" onClick={askUnderstand} disabled={!!aiLoading}>
                Understand This Question
              </button>
              <button className="btn btn-sm" onClick={askAnalogy} disabled={!!aiLoading}>
                🧠 Explain with an Analogy
              </button>
              <button className="btn btn-sm" onClick={askHint} disabled={!!aiLoading}>
                Get a Hint (level {hintLevel}/3)
              </button>
              <button className="btn btn-sm" onClick={askExplainCode} disabled={!!aiLoading}>
                Explain My Code
              </button>
              <button className="btn btn-sm" onClick={askComplexity} disabled={!!aiLoading}>
                Analyze Complexity
              </button>
              <label className="ai-level">
                Level
                <select
                  className="input input-sm"
                  value={aiLevel}
                  onChange={(e) => setAiLevel(e.target.value as AiLevel)}
                  aria-label="AI explanation level"
                >
                  {LEVELS.map((l) => (
                    <option key={l} value={l}>
                      {l}
                    </option>
                  ))}
                </select>
              </label>
              <button
                className="btn btn-sm btn-icon"
                onClick={() => setHelpOpen(true)}
                aria-label="Show keyboard shortcuts"
                title="Keyboard shortcuts"
              >
                ?
              </button>
            </div>

            <div className="editor-toolbar" aria-label="Editor controls">
              <div className="editor-toolbar-left">
                <div className="lang-picker" role="group" aria-label="Programming language">
                  {CODE_LANGUAGES.map((l) => (
                    <button
                      key={l}
                      type="button"
                      className={`lang-btn ${lang === l ? 'active' : ''}`}
                      aria-pressed={lang === l}
                      onClick={() => switchLanguage(l)}
                    >
                      {LANG_LABELS[l]}
                    </button>
                  ))}
                </div>
                <button
                  className="btn btn-sm btn-icon"
                  onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                  aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
                  title="Toggle dark/light theme"
                >
                  {theme === 'dark' ? '☀️' : '🌙'}
                </button>
                <button
                  className="btn btn-sm btn-icon"
                  onClick={() => setFontSize((f) => Math.max(10, f - 1))}
                  aria-label="Decrease font size"
                >
                  A−
                </button>
                <span className="font-size-label" aria-live="polite">
                  {fontSize}px
                </span>
                <button
                  className="btn btn-sm btn-icon"
                  onClick={() => setFontSize((f) => Math.min(24, f + 1))}
                  aria-label="Increase font size"
                >
                  A+
                </button>
                <button className="btn btn-sm" onClick={resetCode}>
                  Reset code
                </button>
              </div>
              <div className="editor-toolbar-right">
                <span className="muted shortcut-hint">Ctrl/⌘ + Enter to run</span>
              </div>
            </div>

            <div className="editor-main">
              <Editor
                height="100%"
                language={lang}
                theme={theme === 'dark' ? 'dsa-dark' : 'dsa-light'}
                value={code}
                onChange={(v) => setCode(v ?? '')}
                onMount={handleMount}
                options={{
                  fontSize,
                  fontFamily:
                    "'JetBrains Mono', ui-monospace, 'Cascadia Code', Consolas, monospace",
                  minimap: { enabled: false },
                  automaticLayout: true,
                  scrollBeyondLastLine: false,
                  renderLineHighlight: 'all',
                  bracketPairColorization: { enabled: true },
                  padding: { top: 8 },
                  suggest: {
                    showKeywords: true,
                    showSnippets: true,
                  },
                }}
                loading={<Spinner label="Loading editor…" />}
              />
              {(aiPanel || aiLoading || aiError) && (
                <aside className="ai-drawer" aria-label="AI assistant output">
                  <div className="ai-drawer-header">
                    <strong>{aiLoading ?? aiPanel?.title ?? 'AI Assistant'}</strong>
                    <button
                      className="btn btn-sm btn-icon"
                      onClick={() => {
                        setAiPanel(null);
                        setAiError(null);
                        setAiNotConfigured(false);
                      }}
                      aria-label="Close AI panel"
                    >
                      ✕
                    </button>
                  </div>
                  <div className="ai-drawer-body">
                    {aiLoading && <Spinner label="Thinking…" />}
                    {aiError && <div className="error-box">{aiError}</div>}
                    {aiNotConfigured && <AiNotConfiguredNotice />}
                    {aiPanel && !aiNotConfigured && <Markdown text={aiPanel.content} />}
                  </div>
                </aside>
              )}
            </div>
          </div>
        }
        right={
          <div className="panel-body">
            <div className="tabs" role="tablist" aria-label="Test tabs">
              {(['tests', 'console'] as RightTab[]).map((t) => (
                <button
                  key={t}
                  role="tab"
                  aria-selected={rightTab === t}
                  className={`tab ${rightTab === t ? 'active' : ''}`}
                  onClick={() => setRightTab(t)}
                >
                  {t === 'tests' ? 'Test Cases' : 'Console'}
                </button>
              ))}
            </div>

            {rightTab === 'tests' && (
              <div className="tests-tab">
                <div className="run-actions">
                  <button
                    className="btn btn-primary"
                    onClick={runCode}
                    disabled={running || submitting}
                  >
                    {running ? 'Running…' : '▶ Run'}
                  </button>
                  <button
                    className="btn btn-submit"
                    onClick={submitCode}
                    disabled={running || submitting}
                  >
                    {submitting ? 'Submitting…' : 'Submit'}
                  </button>
                </div>

                {submitResult && (
                  <div className={`verdict-banner ${verdictClass(submitResult.verdict)}`}>
                    <div className="verdict-title">
                      {submitResult.verdict} — {submitResult.passedCount}/{submitResult.totalCount} hidden tests
                      passed
                    </div>
                    {!submitResult.compiled && submitResult.compileOutput && (
                      <pre className="verdict-detail">{submitResult.compileOutput}</pre>
                    )}
                    {submitResult.failedTest && (
                      <div className="verdict-detail">
                        <div>
                          <strong>Input:</strong>
                          <pre>{submitResult.failedTest.input}</pre>
                        </div>
                        <div>
                          <strong>Expected:</strong>
                          <pre>{submitResult.failedTest.expected}</pre>
                        </div>
                        <div>
                          <strong>Actual:</strong>
                          <pre>{submitResult.failedTest.actual || '(empty)'}</pre>
                        </div>
                        {submitResult.failedTest.error && (
                          <div>
                            <strong>Error:</strong>
                            <pre>{submitResult.failedTest.error}</pre>
                          </div>
                        )}
                      </div>
                    )}
                    {submitResult.timeMs > 0 && (
                      <div className="muted">Total time: {submitResult.timeMs}ms</div>
                    )}
                  </div>
                )}

                <div className="desc-section-title">Sample tests</div>
                {problem.sampleTests.map((t, i) => {
                  const r = runResultsByIndex.get(i);
                  return (
                    <div key={i} className={`test-row ${r ? (r.passed ? 'pass' : 'fail') : ''}`}>
                      <div className="test-row-header">
                        <strong>Case {i + 1}</strong>
                        {r && (
                          <span className={`verdict-badge ${verdictClass(r.verdict)}`}>
                            {r.passed ? '✓ Passed' : `✗ ${r.verdict}`}
                          </span>
                        )}
                      </div>
                      <div>
                        <span className="muted">Input:</span>
                        <pre>{t.input}</pre>
                      </div>
                      <div>
                        <span className="muted">Expected:</span>
                        <pre>{t.expected}</pre>
                      </div>
                      {r && (
                        <div className="run-details">
                          <div>
                            <span className="muted">Actual:</span>
                            <pre>{r.actual || '(empty)'}</pre>
                          </div>
                          <div className="muted">⏱ {r.timeMs}ms</div>
                          {r.error && (
                            <div>
                              <span className="muted">Error:</span>
                              <pre className="error-output">{r.error}</pre>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}

                <div className="desc-section-title custom-tests-title">
                  Custom tests
                  <button
                    className="btn btn-sm"
                    onClick={() => setCustomTests((prev) => [...prev, { input: '', expected: '' }])}
                  >
                    + Add test
                  </button>
                </div>
                {customTests.length === 0 && (
                  <p className="muted">Add your own stdin / expected-output pairs to try edge cases.</p>
                )}
                {customTests.map((t, i) => {
                  const globalIdx = problem.sampleTests.length + i;
                  const r = runResultsByIndex.get(globalIdx);
                  return (
                    <div key={i} className={`test-row ${r ? (r.passed ? 'pass' : 'fail') : ''}`}>
                      <div className="test-row-header">
                        <strong>Custom {i + 1}</strong>
                        <button
                          className="btn btn-sm btn-icon"
                          onClick={() =>
                            setCustomTests((prev) => prev.filter((_, j) => j !== i))
                          }
                          aria-label={`Remove custom test ${i + 1}`}
                        >
                          ✕
                        </button>
                      </div>
                      <label className="muted">
                        stdin
                        <textarea
                          className="input test-input"
                          value={t.input}
                          onChange={(e) =>
                            setCustomTests((prev) =>
                              prev.map((ct, j) => (j === i ? { ...ct, input: e.target.value } : ct)),
                            )
                          }
                          rows={3}
                          placeholder={'[2,7,11,15]\n9'}
                          aria-label={`Custom test ${i + 1} input`}
                        />
                      </label>
                      <label className="muted">
                        expected output
                        <input
                          className="input"
                          value={t.expected}
                          onChange={(e) =>
                            setCustomTests((prev) =>
                              prev.map((ct, j) =>
                                j === i ? { ...ct, expected: e.target.value } : ct,
                              ),
                            )
                          }
                          placeholder="[0, 1]"
                          aria-label={`Custom test ${i + 1} expected output`}
                        />
                      </label>
                      {r && (
                        <div className="run-details">
                          <span className={`verdict-badge ${verdictClass(r.verdict)}`}>
                            {r.passed ? '✓ Passed' : `✗ ${r.verdict}`}
                          </span>
                          <div>
                            <span className="muted">Actual:</span>
                            <pre>{r.actual || '(empty)'}</pre>
                          </div>
                          <div className="muted">⏱ {r.timeMs}ms</div>
                          {r.error && (
                            <div>
                              <span className="muted">Error:</span>
                              <pre className="error-output">{r.error}</pre>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}

            {rightTab === 'console' && (
              <div className="console-tab">
                {running && <Spinner label="Compiling and running…" />}
                {!running && !runResult && <EmptyState message="Run your code to see console output here." />}
                {runResult && !runResult.compiled && (
                  <div>
                    <div className="desc-section-title">Compilation output</div>
                    <pre className="error-output console-pre">
                      {runResult.compileOutput || '(no output)'}
                    </pre>
                  </div>
                )}
                {runResult?.note && (
                  <div>
                    <div className="desc-section-title">Note</div>
                    <pre className="console-pre">{runResult.note}</pre>
                  </div>
                )}
                {runResult?.compiled && (
                  <div>
                    <div className="desc-section-title">Per-test errors</div>
                    {runResult.results.filter((r) => r.error).length === 0 && (
                      <p className="muted">No stderr / runtime errors reported.</p>
                    )}
                    {runResult.results
                      .filter((r) => r.error)
                      .map((r) => (
                        <div key={r.index} className="test-row fail">
                          <div className="test-row-header">
                            <strong>Test {r.index + 1}</strong>
                            <span className={`verdict-badge ${verdictClass(r.verdict)}`}>
                              {r.verdict}
                            </span>
                          </div>
                          <pre className="error-output">{r.error}</pre>
                        </div>
                      ))}
                  </div>
                )}
              </div>
            )}
          </div>
        }
      />

      {helpOpen && (
        <Modal title="Keyboard shortcuts" onClose={() => setHelpOpen(false)}>
          <table className="shortcuts-table">
            <tbody>
              <tr>
                <td>
                  <kbd>Ctrl</kbd> / <kbd>⌘</kbd> + <kbd>Enter</kbd>
                </td>
                <td>Run code against sample + custom tests</td>
              </tr>
              <tr>
                <td>
                  <kbd>F1</kbd>
                </td>
                <td>Monaco command palette (inside the editor)</td>
              </tr>
              <tr>
                <td>
                  <kbd>Esc</kbd>
                </td>
                <td>Close dialogs</td>
              </tr>
            </tbody>
          </table>
          <p className="muted">
            Code drafts are stored in this browser per problem and language. Submit when authed
            to record official submissions.
          </p>
        </Modal>
      )}
    </div>
  );
}
