# DSA Practice Platform — Build Contract (v1)

Single source of truth for all builders. Follow it exactly; if something here conflicts
with an earlier message, this file wins.

## Repo layout (~/workspace/dsa-platform/)

- `backend/` — Java 17 + Spring Boot 3.4 REST API (existing starter: keep `ExecutionController`'s
  Docker sandbox logic, extend it). Serves the API and, for the all-in-one jar, the frontend
  from `src/main/resources/static/`.
- `frontend/` — React + TypeScript + Vite + Monaco Editor (`@monaco-editor/react`).
  `npm run build` outputs to `frontend/dist/`, which is copied into
  `backend/src/main/resources/static/` for the single-jar deployment.
- `questions/` — the question bank: one JSON file per pattern, `questions/<pattern>.json`,
  each a JSON array of exactly 20 question objects (schema below). Backend loads them from
  `backend/src/main/resources/questions/*.json` at startup (build step copies them there).

## Patterns (18) — file names

`hashing`, `two-pointers`, `sliding-window`, `prefix-sums`, `binary-search`,
`sorting-intervals`, `stacks`, `linked-lists`, `trees`, `heaps`, `backtracking`,
`greedy`, `graph-traversal`, `topo-unionfind-mst`, `dynamic-programming`,
`bit-manipulation`, `tries`, `matrix-simulation`.

## Question JSON schema

Every question object MUST have exactly these fields:

```json
{
  "id": "two-sum",
  "title": "Two Sum",
  "pattern": "hashing",
  "difficulty": "Easy",
  "description": "Given an array of integers nums and an integer target, return indices of the two numbers that add up to target. ...",
  "examples": [
    {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "nums[0] + nums[1] == 9."}
  ],
  "constraints": ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "Exactly one valid answer exists."],
  "signature": {
    "className": "Solution",
    "methodName": "twoSum",
    "returnType": "int[]",
    "params": [{"name": "nums", "type": "int[]"}, {"name": "target", "type": "int"}]
  },
  "starterCode": "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        \n    }\n}",
  "sampleTests": [{"input": "[2,7,11,15]\n9", "expected": "[0, 1]"}],
  "hiddenTests": [{"input": "[3,2,4]\n6", "expected": "[1, 2]"}],
  "tags": ["array", "hash-table"],
  "timeComplexity": "O(n)",
  "spaceComplexity": "O(n)",
  "hints": ["Try a brute-force pair check first to feel the problem.", "Can you trade space for time with a map from value to index?"]
}
```

Rules:
- `id`: kebab-case, globally unique. `difficulty`: one of `Easy`, `Medium`, `Hard`.
- Per pattern: 8 Easy, 8 Medium, 4 Hard. Mix classic + fresh variants; no duplicates across the bank.
- `signature` types are restricted to the harness-supported set:
  `int`, `long`, `double`, `boolean`, `char`, `String`,
  `int[]`, `long[]`, `double[]`, `boolean[]`, `char[]`, `String[]`,
  `int[][]`, `char[][]`, `ListNode`, `TreeNode`,
  `List<Integer>`, `List<String>`, `List<List<Integer>>`, `void`.
  Return type may additionally be `ListNode` / `TreeNode`.
- `sampleTests` / `hiddenTests`: `input` is the EXACT stdin the harness feeds (see I/O format).
  `expected` is the EXACT canonical serialized output (see serialization). 2–3 samples, 5–10 hidden.
- Every hidden test must be verified by hand (or by running a reference solution) — a wrong
  expected value is the worst possible bug in this bank.

## Harness I/O format (method mode)

The backend wraps the user's `Solution` class with a generated `Main` that:

1. Reads ALL of stdin, splits into lines (trailing empty lines dropped).
2. Parses line *i* as parameter *i* using the question's signature types:
   - scalars: `int`/`long`/`double`/`boolean` parse naturally; `char` is a single char; `String` is the raw line (may contain spaces).
   - 1-D arrays: JSON-ish `[1, 2, 3]` or `[1,2,3]` (elements comma-separated, brackets required). `String[]` elements may be quoted: `["a", "b"]`.
   - `int[][]` / `char[][]`: `[[1, 2], [3, 4]]`.
   - `ListNode`: `[1, 2, 3]` → 1→2→3. `TreeNode`: level-order `[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4]`.
   - `List<Integer>` / `List<String>` / `List<List<Integer>>`: same bracket syntax as arrays.
3. Calls `new Solution().method(args...)`, serializes the return value, prints it (no extra text).

Canonical serialization (`expected` values must match this exactly):
- scalars → `String.valueOf` (`double` via `Double.toString`).
- `String` → raw string. `char[]` → `[a, b, c]`.
- arrays → `[1, 2, 3]` (comma + space). 2-D → `[[1, 2], [3, 4]]`.
- `ListNode` → `[1, 2, 3]`. `TreeNode` → level-order with `null`, trailing nulls trimmed: `[3, 5, 1, null, 2]`.
- `List<List<Integer>>` → `[[1, 2], [3]]`. `void` → empty output.
- Comparison trims trailing whitespace and normalizes `\r\n` → `\n`.

Program mode (unchanged from starter): complete program with `class Main` + `main`, raw stdin/stdout.

## REST API (backend implements; frontend consumes)

Base path `/api`. JSON everywhere.

- `GET /api/problems?pattern=&difficulty=&search=&status=&sort=` → `{problems: [{id,title,pattern,difficulty,tags,solved,attempted,bookmarked}]}` (auth optional; status fields false when anonymous). `status`: `solved|attempted|unsolved|bookmarked`.
- `GET /api/problems/{id}` → full question WITHOUT `hiddenTests`. 404 if unknown.
- `POST /api/run` `{problemId?, mode: "method"|"program", code, tests: [{input, expected}]}` → `{compiled, compileOutput, results: [{index, input, expected, actual, passed, error, timeMs, verdict}], note}`. `verdict` per test: `Accepted|Wrong Answer|Runtime Error|Time Limit Exceeded|Memory Limit Exceeded`. Never runs hidden tests.
- `POST /api/submit` `{problemId, code}` → runs hiddenTests server-side → `{compiled, compileOutput, verdict, passedCount, totalCount, failedTest?: {input, expected, actual, error}, timeMs}`. Records submission when authed. `verdict`: `Accepted|Wrong Answer|Compilation Error|Runtime Error|Time Limit Exceeded|Memory Limit Exceeded`.
- `POST /api/complexity` `{code}` → `{time, space, confidence, signals[], explanation, caveat}` (heuristic, labeled as such).
- `POST /api/ai/understand` `{problemId, level?: "beginner"|"intermediate"|"advanced"}` → `{content}`
- `POST /api/ai/analogy` `{problemId, level?}` → `{content}` (the 🧠 Explain with an Analogy feature)
- `POST /api/ai/hint` `{problemId, code?, hintLevel?: 1|2|3}` → `{content}` (progressive; never full solution)
- `POST /api/ai/explain-code` `{problemId?, code, level?}` → `{content}`
- `POST /api/ai/dry-run` `{problemId?, code, input?}` → `{content}`
- All `/api/ai/*` return **503 `{error: "AI not configured"}`** when no API key is set. Keys live only in
  server env (`OPENAI_API_KEY`, optional `OPENAI_BASE_URL`, `OPENAI_MODEL`); never sent to the client.
- Auth: `POST /api/auth/register {username, password}` → `{token}`; `POST /api/auth/login` → `{token}`.
  Authed requests send `Authorization: Bearer <token>`.
- `GET /api/me/progress` → `{solved, attempted, streakDays, byPattern: {pattern: {solved, total}}, byDifficulty: {...}, recentSubmissions: [...]}`.
- `POST /api/problems/{id}/bookmark {bookmarked: bool}`, `POST /api/problems/{id}/note {note}`.
- `GET /api/submissions?problemId=` → submission history (authed).

Execution semantics (backend):
- Docker sandbox is the production runner (`--network none`, memory/cpu/pids limits, read-only,
  `no-new-privileges`, `cap-drop ALL`, per-test fresh container, 3s timeout, 128m/64m heap).
- Dev fallback `JAVA_RUNNER_MODE=local` runs `javac`/`java` on the host ONLY when
  `ALLOW_LOCAL_EXECUTION=true` is also set; refuse otherwise. Never the default.
- Rate limit: 30 run/submit requests per IP per minute (in-memory token bucket), 429 beyond.
- Input caps from the starter stay: 30k code chars, 20 tests, 4k chars per input/output.

## Frontend pages/components

- `/` Problems: search box, pattern/difficulty/status filters, sort, progress bar per problem.
- `/problem/:id` Workspace (the core): three resizable panels —
  1. Problem description (+ tabs: Description | Submissions | Notes).
  2. Monaco editor (Java, dark/light, font-size +/-, reset code, keyboard shortcuts e.g. Ctrl+Enter to run).
  3. Test cases + results + console (Run → sample/custom tests; Submit → hidden tests; verdict banners).
  AI toolbar above the editor: `Understand This Question`, `🧠 Explain with an Analogy`, `Get a Hint`, `Explain My Code`, `Analyze Complexity`. AI output renders in a dedicated panel that preserves editor state.
  Prev/next question navigation, related problems.
- `/dashboard` Stats, streak, pattern-wise progress bars, revision queue.
- `/login` Register/login.
- Responsive: panels stack on mobile. Loading states and clear error messages everywhere.
- Dev proxy: Vite proxies `/api` → `http://localhost:8080`.

## Quality bar (applies to every piece)

- Real functionality only. No mock buttons, no simulated execution, no hardcoded AI answers.
- Backend: JUnit tests for harness generation, serialization, verdicts, auth, and the question-bank
  loader (all 360 questions validate against the schema; every hidden test has non-empty input/expected).
- Every file this repo ships must be produced by these rules; AI explanations are generated live
  through the configured LLM from the actual problem data — never templated per-question text.
