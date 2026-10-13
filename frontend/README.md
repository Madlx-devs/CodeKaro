# DSA Practice Platform — Frontend

React + TypeScript + Vite + Monaco Editor. Consumes the Spring Boot API exactly
as specified in `../CONTRACT.md`.

## Run

```bash
npm install
npm run dev        # Vite dev server; /api is proxied to http://localhost:8080
```

The backend must be running on `http://localhost:8080` (or any port — only the
dev proxy target in `vite.config.ts` needs to match).

## Build

```bash
npm run build      # type-checks (tsc) and outputs to frontend/dist/
```

`dist/` is copied into `backend/src/main/resources/static/` for the single-jar
deployment.

## Pages

- `/` — problem list: search, pattern/difficulty/status filters, client-side sort, per-pattern progress chips
- `/problem/:id` — workspace: problem description (Description | Submissions | Notes tabs),
  Monaco Java editor (dark/light, font size, reset, Ctrl/⌘+Enter to run), AI toolbar,
  test cases (sample + custom) with per-test results, console, and submit-against-hidden-tests verdicts
- `/dashboard` — solved/attempted/streak cards, pattern progress, difficulty breakdown, revision queue
- `/login` — register + login (token stored in `localStorage`)

## Notes

- Auth token goes in `localStorage` under `dsa_token` and is sent as
  `Authorization: Bearer <token>`.
- Code drafts are auto-saved per problem in `localStorage` (`dsa_code_<id>`);
  official submissions are recorded server-side on submit.
- AI features require the backend to have `OPENAI_API_KEY` set; a 503 from the
  API surfaces a friendly "AI not configured" notice instead of an error.
