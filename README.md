# Codekaro — DSA Practice Platform

![Java 17](https://img.shields.io/badge/Java-17-ED8B00?logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.4-6DB33F?logo=springboot&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-sandboxed-2496ED?logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)

A self-hosted, LeetCode-style platform for grinding Data Structures & Algorithms in
**Java**. Monaco-powered coding workspace, Docker-sandboxed Java 17 execution with
auto-generated test harnesses, **360 questions across 18 patterns**, an AI learning
assistant, complexity analysis, accounts with progress tracking, streaks and
gamification. One command takes it live on a VPS.

## Deploy it (VPS, one command)

```bash
curl -L -o dsa-deploy.zip https://raw.githubusercontent.com/Madlx-devs/Codekaro/main/dsa-deploy.zip \
  && unzip -o dsa-deploy.zip \
  && cd deploy \
  && sudo bash deploy.sh
```

That's it. `deploy.sh` installs Docker, pulls the sandbox image, starts the app +
PostgreSQL, and puts Caddy in front on port 80. Takes ~5 minutes on a fresh Ubuntu
22.04/24.04 box (works on a 1 GB RAM VPS). Re-run the same commands any time to
update — your database is untouched.

Set `OPENAI_API_KEY` in `deploy/.env` afterwards if you want the AI tutor features.

## What's inside

- **Real judge, not a toy** — every submission runs in a fresh Docker container:
  no network, 128 MB RAM, 0.5 CPU, read-only filesystem, 12 s compile / 3 s run
  timeouts. Verdicts: Accepted, Wrong Answer, Compilation Error, Runtime Error,
  Time Limit Exceeded, Memory Limit Exceeded.
- **Two problem modes** — LeetCode-style *method mode* (we generate the `Main`
  harness and parse your return value for all 24 supported types: primitives,
  1-D/2-D arrays, `ListNode`, `TreeNode`, collections, `void`) and classic
  *program mode* (stdin → stdout).
- **360 questions, 18 patterns** — two pointers, sliding window, trees, graphs, DP,
  heaps, tries… machine-verified expected outputs, hidden tests that never leak to
  the client.
- **Workspace that doesn't fight you** — dark-first "Ink & Amber" theme, real Java
  autocomplete in Monaco (keywords, snippets like `fori`/`sout`/`psvm`, ~90
  standard-library member completions), per-problem drafts that survive refreshes.
- **AI learning assistant** — hints that don't spoil, explain-with-an-analogy,
  dry-runs, code explanations (needs `OPENAI_API_KEY`; clean 503 without it).
- **Progress that sticks** — accounts, per-pattern stats, streaks, notes and
  bookmarks per problem, submission history.

## Run it locally (dev)

Requirements: Java 17+, Maven 3.9+, Docker running.

```bash
# 1. Pull the sandbox image once
docker pull eclipse-temurin:17-jdk

# 2. Run (dev profile: file-based H2 at ./data/dsa, Docker sandbox runner)
cd backend
mvn spring-boot:run
```

Open http://localhost:8080. No database setup needed.

No Docker on your dev machine? (Dev only — never for real judging.)

```bash
JAVA_RUNNER_MODE=local ALLOW_LOCAL_EXECUTION=true mvn spring-boot:run
```

Both variables are required; any other combination makes the app refuse to start
rather than silently executing untrusted code on your host.

## Production (Docker Compose, manual)

```bash
cp .env.example .env   # fill in DB_PASSWORD and OPENAI_API_KEY
docker compose up --build
```

Starts PostgreSQL and the app (`SPRING_PROFILES_ACTIVE=prod`). The app container
mounts `/var/run/docker.sock` so it can launch the hardened sandbox containers; the
runner image (`JAVA_RUNNER_IMAGE`, default `eclipse-temurin:17-jdk`) must be pullable.

## Repo layout

- `backend/` — Java 17 + Spring Boot 3.4 REST API (also serves the frontend from
  `src/main/resources/static/` in the single-jar deployment).
- `frontend/` — React + TypeScript + Vite + Monaco Editor. `npm run build` outputs to
  `frontend/dist/`, copied into `backend/src/main/resources/static/`.
- `questions/` — the question bank: one JSON file per pattern, 20 questions each
  (schema in `CONTRACT.md`). Validated at startup; the app fails fast on any invalid file.
- `dsa-deploy.zip` — the ready-to-download VPS package (backend + questions + compose +
  Caddyfile + install script). Rebuilt from a release commit; grab it with the curl
  command at the top.

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
- `POST /api/ai/understand` `{problemId, level?}` · `POST /api/ai/analogy` `{problemId, level?}`
- `POST /api/ai/hint` `{problemId, code?, hintLevel?: 1|2|3}` — progressive, never the full solution
- `POST /api/ai/explain-code` `{problemId?, code, level?}` · `POST /api/ai/dry-run` `{problemId?, code, input?}`

**Auth & progress** (`Authorization: Bearer <token>`)
- `POST /api/auth/register` / `POST /api/auth/login` `{username, password}` → `{token}`
- `GET /api/me/progress` — `{solved, attempted, streakDays, byPattern, byDifficulty, recentSubmissions}`
- `POST /api/problems/{id}/bookmark` `{bookmarked}` · `POST /api/problems/{id}/note` `{note}`
- `GET /api/submissions?problemId=`

## Harness I/O contract (method mode)

The backend wraps your `Solution` in a generated `Main` that reads all stdin lines,
parses line *i* as parameter *i*, calls the method, and prints the canonical
serialization. Supported types: `int long double boolean char String`, 1-D/2-D arrays,
`ListNode`, `TreeNode` (level-order, `null` for missing), `List<Integer>`,
`List<String>`, `List<List<Integer>>`, `void`. `char[]` serializes as `[a, b, c]`,
`TreeNode` as level-order with trailing nulls trimmed. Comparison trims trailing
whitespace and normalizes CRLF. Full details in `CONTRACT.md`.

## Security notes

- Untrusted code runs **only** in fresh Docker containers: `--network none`, 128 MB RAM,
  0.5 CPU, 64 pids, read-only root fs, `no-new-privileges`, `cap-drop ALL`; 64 MB JVM
  heap (exit 137 or `OutOfMemoryError` → Memory Limit Exceeded).
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
