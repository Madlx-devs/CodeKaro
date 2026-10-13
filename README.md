# DSA Practice Platform

A self-hosted, LeetCode-style platform for learning Data Structures & Algorithms in Java:
Monaco-based coding workspace, Docker-sandboxed Java 17 execution with auto-generated
test harnesses, a 360-question bank across 18 patterns, an AI learning assistant,
complexity analysis, accounts with progress tracking, streaks and gamification.

## Repo layout

- `backend/` — Java 17 + Spring Boot 3.4 REST API (also serves the frontend from
  `src/main/resources/static/` in the single-jar deployment).
- `frontend/` — React + TypeScript + Vite + Monaco Editor. `npm run build` outputs to
  `frontend/dist/`, copied into `backend/src/main/resources/static/`.
- `questions/` — the question bank: one JSON file per pattern (`questions/<pattern>.json`),
  each a JSON array of 20 question objects (see CONTRACT.md for the schema). The Maven
  build copies them into the backend classpath; they are validated at startup and the
  app fails fast if any file is invalid.

## Quick start (local dev)

Requirements: Java 17+, Maven 3.9+, Docker running, and (for AI features) an
OpenAI-compatible API key.

```bash
# 1. Pull the sandbox image once
docker pull eclipse-temurin:17-jdk

# 2. Run (dev profile: file-based H2 at ./data/dsa, Docker sandbox runner)
cd backend
mvn spring-boot:run
```

Open http://localhost:8080. The dev profile needs no database setup.

To run without Docker (dev machines only):

```bash
JAVA_RUNNER_MODE=local ALLOW_LOCAL_EXECUTION=true mvn spring-boot:run
```

Both variables are required; any other combination makes the app refuse to start
rather than silently executing untrusted code on your host.

## Production (Docker Compose)

```bash
cp .env.example .env   # fill in DB_PASSWORD and OPENAI_API_KEY
docker compose up --build
```

This starts PostgreSQL and the app (`SPRING_PROFILES_ACTIVE=prod`). The app container
mounts `/var/run/docker.sock` so it can launch the hardened sandbox containers; the
runner image (`JAVA_RUNNER_IMAGE`, default `eclipse-temurin:17-jdk`) must be pullable.
Pointing at a remote Docker host instead? Set `DOCKER_HOST` in the app container's
environment and drop the socket mount.

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `SPRING_PROFILES_ACTIVE` | `dev` | `dev` = H2 file DB; `prod` = PostgreSQL via `DB_URL`/`DB_USER`/`DB_PASSWORD` |
| `DB_URL` / `DB_USER` / `DB_PASSWORD` | `jdbc:postgresql://localhost:5432/dsa` / `dsa` / `changeme` | Prod database |
| `JAVA_RUNNER_IMAGE` | `eclipse-temurin:17-jdk` | Image for sandbox compile/run containers |
| `JAVA_RUNNER_MODE` | `docker` | `docker` (production) or `local` (dev only) |
| `ALLOW_LOCAL_EXECUTION` | `false` | Must be `true` together with `JAVA_RUNNER_MODE=local`, else the app refuses to start |
| `OPENAI_API_KEY` | — | Enables `/api/ai/*`; without it they return 503 |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | OpenAI-compatible chat-completions endpoint |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model for AI features |

## API summary (base path `/api`, JSON everywhere)

**Problems**
- `GET /api/problems?pattern=&difficulty=&search=&status=&sort=` — list; `status` is
  `solved|attempted|unsolved|bookmarked` (auth optional; flags false when anonymous)
- `GET /api/problems/{id}` — full question **without** `hiddenTests`

**Execution** (rate-limited: 30 req/min/IP, 429 + `Retry-After` beyond)
- `POST /api/run` `{problemId?, mode: "method"|"program", code, tests: [{input, expected}], signature?}` —
  per-test `{verdict, timeMs, actual, expected, passed, error}`; verdicts: Accepted, Wrong Answer,
  Runtime Error, Time Limit Exceeded, Memory Limit Exceeded. Never runs hidden tests.
- `POST /api/submit` `{problemId, code}` — runs hidden tests server-side;
  `{compiled, compileOutput, verdict, passedCount, totalCount, failedTest?, timeMs}`;
  verdicts add Compilation Error. Records the submission when authed.
- `POST /api/complexity` `{code}` — `{time, space, confidence, signals[], explanation, caveat}`
  (heuristic, labeled as such)

**AI** (503 `{error:"AI not configured"}` without a key; key never leaves the server)
- `POST /api/ai/understand` `{problemId, level?}` · `POST /api/ai/analogy` `{problemId, level?}` —
  the 🧠 Explain-with-an-Analogy 7-step format
- `POST /api/ai/hint` `{problemId, code?, hintLevel?: 1|2|3}` — progressive, never the full solution
- `POST /api/ai/explain-code` `{problemId?, code, level?}` · `POST /api/ai/dry-run` `{problemId?, code, input?}`

**Auth & progress** (`Authorization: Bearer <token>`)
- `POST /api/auth/register` / `POST /api/auth/login` `{username, password}` → `{token}`
- `GET /api/me/progress` — `{solved, attempted, streakDays, byPattern, byDifficulty, recentSubmissions}`
- `POST /api/problems/{id}/bookmark` `{bookmarked}` · `POST /api/problems/{id}/note` `{note}`
- `GET /api/submissions?problemId=`

## Harness I/O contract (method mode)

The backend wraps the user's `Solution` in a generated `Main` that reads all stdin
lines, parses line *i* as parameter *i*, calls the method, and prints the canonical
serialization. Supported types: `int long double boolean char String`, 1-D/2-D arrays,
`ListNode`, `TreeNode` (level-order, `null` for missing), `List<Integer>`,
`List<String>`, `List<List<Integer>>`, `void`. `char[]` serializes as `[a, b, c]`,
`TreeNode` as level-order with trailing nulls trimmed. Comparison trims trailing
whitespace and normalizes CRLF. Full details in `CONTRACT.md`.

## Security notes

- Untrusted code runs **only** in fresh Docker containers: `--network none`, 128 MB RAM,
  0.5 CPU, 64 pids, read-only root fs, `no-new-privileges`, `cap-drop ALL`; 12 s compile
  / 3 s run timeouts; 64 MB JVM heap (exit 137 or `OutOfMemoryError` → Memory Limit Exceeded).
- Host execution exists only as an explicit dev opt-in (`JAVA_RUNNER_MODE=local` **and**
  `ALLOW_LOCAL_EXECUTION=true`); anything else refuses to boot.
- Input caps: 30k code chars, 20 tests, 4k chars per input/output; 30 run/submit req/min/IP.
- Passwords are BCrypt-hashed; sessions are opaque 256-bit bearer tokens (30-day expiry).
- `hiddenTests` are never serialized to the client; the AI key lives only in server env.
- Docker is a strong isolation layer but not a complete security guarantee for a public
  judge: for public deployment use a dedicated worker host/VM, tighter syscall filters,
  and monitoring. Do not expose the Docker socket to untrusted users on a shared host.

## Tests

```bash
cd backend && mvn test
```

Covers: harness generation + real javac/java round-trips for every supported type
(skipped when no JDK is on PATH), verdict mapping incl. TLE/MLE, question-bank schema
validation, auth register→login→authed request, and rate-limiter behavior.
