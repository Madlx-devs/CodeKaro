/**
 * Typed API client for the DSA Practice Platform backend.
 * Every shape below mirrors the REST API section of CONTRACT.md exactly.
 */

const API_BASE = '/api';
const TOKEN_KEY = 'dsa_token';

// ---------------------------------------------------------------------------
// Auth token helpers
// ---------------------------------------------------------------------------

export function getToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

export function isAuthed(): boolean {
  return getToken() !== null;
}

// ---------------------------------------------------------------------------
// Error type
// ---------------------------------------------------------------------------

export class ApiError extends Error {
  status: number;
  body?: unknown;

  constructor(status: number, message: string, body?: unknown) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.body = body;
  }

  /** True when the backend has no AI API key configured (friendly 503). */
  get isAiNotConfigured(): boolean {
    return this.status === 503;
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> | undefined),
  };
  const token = getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(API_BASE + path, { ...options, headers });
  if (!res.ok) {
    let body: unknown;
    try {
      body = await res.json();
    } catch {
      body = undefined;
    }
    const msg =
      (body as { error?: string } | undefined)?.error ||
      (res.status === 429
        ? 'Rate limit exceeded — too many run/submit requests. Wait a minute and try again.'
        : res.status === 401
          ? 'Login required for this action.'
          : `Request failed (${res.status})`);
    throw new ApiError(res.status, msg, body);
  }
  return (await res.json()) as T;
}

// ---------------------------------------------------------------------------
// Types (CONTRACT.md: Question JSON schema + REST API)
// ---------------------------------------------------------------------------

export type Difficulty = 'Easy' | 'Medium' | 'Hard';
export type Verdict =
  | 'Accepted'
  | 'Wrong Answer'
  | 'Compilation Error'
  | 'Runtime Error'
  | 'Time Limit Exceeded'
  | 'Memory Limit Exceeded';
export type AiLevel = 'beginner' | 'intermediate' | 'advanced';
export type CodeLanguage = 'java' | 'python' | 'cpp';
export const CODE_LANGUAGES: CodeLanguage[] = ['java', 'python', 'cpp'];

export interface ProblemSummary {
  id: string;
  title: string;
  pattern: string;
  difficulty: Difficulty;
  tags: string[];
  solved: boolean;
  attempted: boolean;
  bookmarked: boolean;
}

export interface ProblemsResponse {
  problems: ProblemSummary[];
}

export interface Example {
  input: string;
  output: string;
  explanation?: string;
}

export interface Param {
  name: string;
  type: string;
}

export interface Signature {
  className: string;
  methodName: string;
  returnType: string;
  params: Param[];
}

export interface TestCase {
  input: string;
  expected: string;
}

export interface ProblemDetail {
  id: string;
  title: string;
  pattern: string;
  difficulty: Difficulty;
  description: string;
  examples: Example[];
  constraints: string[];
  signature: Signature;
  starterCode: string;
  /** Per-language starter code. `java` may fall back to the legacy `starterCode` field. */
  starterCodes?: Record<CodeLanguage, string>;
  /** Display-only method signatures for the non-Java languages. */
  methodSignatures?: { python: string; cpp: string };
  sampleTests: TestCase[];
  tags: string[];
  timeComplexity: string;
  spaceComplexity: string;
  hints: string[];
  solved?: boolean;
  attempted?: boolean;
  bookmarked?: boolean;
  note?: string;
}

export interface RunTestResult {
  index: number;
  input: string;
  expected: string;
  actual: string;
  passed: boolean;
  error: string;
  timeMs: number;
  verdict: Verdict;
}

export interface RunResponse {
  compiled: boolean;
  compileOutput: string;
  results: RunTestResult[];
  note: string;
}

export interface FailedTest {
  input: string;
  expected: string;
  actual: string;
  error: string;
}

export interface SubmitResponse {
  compiled: boolean;
  compileOutput: string;
  verdict: Verdict;
  passedCount: number;
  totalCount: number;
  failedTest?: FailedTest;
  timeMs: number;
}

export interface ComplexityResponse {
  time: string;
  space: string;
  confidence: string;
  signals: string[];
  explanation: string;
  caveat: string;
}

export interface AiResponse {
  content: string;
}

export interface ProgressPattern {
  solved: number;
  total: number;
}

export interface ProgressResponse {
  solved: number;
  attempted: number;
  streakDays: number;
  byPattern: Record<string, ProgressPattern>;
  byDifficulty: Record<string, unknown>;
  recentSubmissions: Array<Record<string, unknown>>;
}

export interface SubmissionRecord {
  id?: number | string;
  problemId?: string;
  problemTitle?: string;
  verdict?: string;
  passedCount?: number;
  totalCount?: number;
  timeMs?: number;
  createdAt?: string;
  submittedAt?: string;
  code?: string;
}

export interface ProblemsQuery {
  pattern?: string;
  difficulty?: Difficulty | '';
  search?: string;
  status?: 'solved' | 'attempted' | 'unsolved' | 'bookmarked' | '';
  sort?: string;
}

function toQuery(q: ProblemsQuery): string {
  const params = new URLSearchParams();
  if (q.pattern) params.set('pattern', q.pattern);
  if (q.difficulty) params.set('difficulty', q.difficulty);
  if (q.search) params.set('search', q.search);
  if (q.status) params.set('status', q.status);
  if (q.sort) params.set('sort', q.sort);
  const s = params.toString();
  return s ? `?${s}` : '';
}

// ---------------------------------------------------------------------------
// Client
// ---------------------------------------------------------------------------

export const api = {
  problems(q: ProblemsQuery = {}): Promise<ProblemsResponse> {
    return request<ProblemsResponse>(`/problems${toQuery(q)}`);
  },

  problem(id: string): Promise<ProblemDetail> {
    return request<ProblemDetail>(`/problems/${encodeURIComponent(id)}`);
  },

  run(body: {
    problemId?: string;
    mode: 'method' | 'program';
    code: string;
    tests: TestCase[];
    language?: CodeLanguage;
  }): Promise<RunResponse> {
    return request<RunResponse>('/run', {
      method: 'POST',
      body: JSON.stringify(body),
    });
  },

  submit(body: {
    problemId: string;
    code: string;
    language?: CodeLanguage;
  }): Promise<SubmitResponse> {
    return request<SubmitResponse>('/submit', {
      method: 'POST',
      body: JSON.stringify(body),
    });
  },

  complexity(body: { code: string }): Promise<ComplexityResponse> {
    return request<ComplexityResponse>('/complexity', {
      method: 'POST',
      body: JSON.stringify(body),
    });
  },

  aiUnderstand(problemId: string, level?: AiLevel): Promise<AiResponse> {
    return request<AiResponse>('/ai/understand', {
      method: 'POST',
      body: JSON.stringify({ problemId, level }),
    });
  },

  aiAnalogy(problemId: string, level?: AiLevel): Promise<AiResponse> {
    return request<AiResponse>('/ai/analogy', {
      method: 'POST',
      body: JSON.stringify({ problemId, level }),
    });
  },

  aiHint(problemId: string, code?: string, hintLevel?: 1 | 2 | 3): Promise<AiResponse> {
    return request<AiResponse>('/ai/hint', {
      method: 'POST',
      body: JSON.stringify({ problemId, code, hintLevel }),
    });
  },

  aiExplainCode(problemId: string | undefined, code: string, level?: AiLevel): Promise<AiResponse> {
    return request<AiResponse>('/ai/explain-code', {
      method: 'POST',
      body: JSON.stringify({ problemId, code, level }),
    });
  },

  aiDryRun(problemId: string | undefined, code: string, input?: string): Promise<AiResponse> {
    return request<AiResponse>('/ai/dry-run', {
      method: 'POST',
      body: JSON.stringify({ problemId, code, input }),
    });
  },

  async register(username: string, password: string): Promise<string> {
    const res = await request<{ token: string }>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    setToken(res.token);
    return res.token;
  },

  async login(username: string, password: string): Promise<string> {
    const res = await request<{ token: string }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    setToken(res.token);
    return res.token;
  },

  logout(): void {
    clearToken();
  },

  progress(): Promise<ProgressResponse> {
    return request<ProgressResponse>('/me/progress');
  },

  bookmark(id: string, bookmarked: boolean): Promise<unknown> {
    return request(`/problems/${encodeURIComponent(id)}/bookmark`, {
      method: 'POST',
      body: JSON.stringify({ bookmarked }),
    });
  },

  saveNote(id: string, note: string): Promise<unknown> {
    return request(`/problems/${encodeURIComponent(id)}/note`, {
      method: 'POST',
      body: JSON.stringify({ note }),
    });
  },

  submissions(problemId?: string): Promise<SubmissionRecord[]> {
    const q = problemId ? `?problemId=${encodeURIComponent(problemId)}` : '';
    return request<SubmissionRecord[]>(`/submissions${q}`);
  },
};

// ---------------------------------------------------------------------------
// Shared constants
// ---------------------------------------------------------------------------

export const PATTERNS = [
  'hashing',
  'two-pointers',
  'sliding-window',
  'prefix-sums',
  'binary-search',
  'sorting-intervals',
  'stacks',
  'linked-lists',
  'trees',
  'heaps',
  'backtracking',
  'greedy',
  'graph-traversal',
  'topo-unionfind-mst',
  'dynamic-programming',
  'bit-manipulation',
  'tries',
  'matrix-simulation',
] as const;

const PATTERN_LABELS: Record<string, string> = {
  hashing: 'Hashing',
  'two-pointers': 'Two Pointers',
  'sliding-window': 'Sliding Window',
  'prefix-sums': 'Prefix Sums',
  'binary-search': 'Binary Search',
  'sorting-intervals': 'Sorting / Intervals',
  stacks: 'Stacks',
  'linked-lists': 'Linked Lists',
  trees: 'Trees',
  heaps: 'Heaps',
  backtracking: 'Backtracking',
  greedy: 'Greedy',
  'graph-traversal': 'Graph Traversal',
  'topo-unionfind-mst': 'Topo Sort / Union-Find / MST',
  'dynamic-programming': 'Dynamic Programming',
  'bit-manipulation': 'Bit Manipulation',
  tries: 'Tries',
  'matrix-simulation': 'Matrix / Simulation',
};

export function patternLabel(pattern: string): string {
  return PATTERN_LABELS[pattern] ?? pattern;
}

export const DIFFICULTIES: Difficulty[] = ['Easy', 'Medium', 'Hard'];

export function friendlyApiError(err: unknown): string {
  if (err instanceof ApiError) return err.message;
  if (err instanceof Error) return err.message;
  return 'Something went wrong.';
}
