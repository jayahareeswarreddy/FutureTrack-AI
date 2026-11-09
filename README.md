# FutureTrack AI

[![CI](https://github.com/jayahareeswarreddy/FutureTrack-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/jayahareeswarreddy/FutureTrack-AI/actions/workflows/ci.yml)
[![Deploy](https://github.com/jayahareeswarreddy/FutureTrack-AI/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/jayahareeswarreddy/FutureTrack-AI/actions/workflows/deploy-pages.yml)

A career recommender that scores your skills against 24 tech career paths,
explains each match, and points you at free material to close the gaps.

**Live demo → [jayahareeswarreddy.github.io/FutureTrack-AI](https://jayahareeswarreddy.github.io/FutureTrack-AI/)**

---

## What is actually AI, and what is not

Worth stating plainly, because the name invites the wrong assumption.

| Part | How it works |
| --- | --- |
| **Match score and ranking** | Deterministic Python. Weighted overlap between your skills and each career's required and preferred skills. Never touches a model. |
| **Career catalogue, salaries, base roadmaps** | A fixed dataset in `backend/server.py`. |
| **Skill-gap arithmetic** | Set difference between what you have and what a role requires. |
| **Match explanations** | LLM, when a key is configured. Otherwise rule-based templates. |
| **Roadmap detail** | LLM expands the base steps into durations and resources. Otherwise the base steps are returned unchanged. |
| **Skill-gap summary and learning order** | LLM. The numbers above it are never overwritten by the model. |

The service runs with **no API key at all** and stays fully functional — every
AI path has a deterministic fallback, and `GET /health` tells you which one is
live. That is the point of the design, not a limitation: a recruiter opening
the demo gets a working app whether or not a key is funded.

## The validation layer

The interesting problem here is not calling an LLM, it is trusting what comes
back. `backend/ai_client.py` wraps every generation:

```
prompt ──► model ──► JSON parse ──► JSON Schema check ──► caller
                          │              │
                          └── failure ───┘
                                 │
                       retry, with the validation
                       error fed back to the model
                                 │
                       exhausted ──► rule-based fallback
```

- Responses are requested as `json_object` and validated against the schemas in
  `backend/schemas.py` with `jsonschema`.
- A malformed response is not discarded silently — the validation error is
  appended to the next prompt so the model can correct itself.
- Retries use exponential backoff with jitter, capped by `AI_MAX_RETRIES`.
- The SDK call is synchronous, so it runs in a worker thread and never blocks
  the event loop.
- `GET /health` exposes retry counts, schema rejections and fallback counts.

## Providers

Groq and OpenAI both speak the OpenAI chat-completions protocol, so the
provider is configuration rather than a code path.

| Provider | Default model | Key | Cost |
| --- | --- | --- | --- |
| `groq` (default) | `llama-3.3-70b-versatile` | `GROQ_API_KEY` | Free tier, no card |
| `openai` | `gpt-4o-mini` | `OPENAI_API_KEY` | Paid |

Get a free Groq key at [console.groq.com/keys](https://console.groq.com/keys).

## API

Fourteen endpoints. Interactive docs at `/docs` once the server is running.

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | Service banner |
| `GET` | `/health` | Readiness, dependency state, AI retry metrics |
| `GET` | `/careers` | Full catalogue |
| `GET` | `/careers/search?q=` | Search by title, description, category, skill |
| `GET` | `/careers/{id}` | One career |
| `GET` | `/careers/{id}/roadmap` | Ordered learning path |
| `GET` | `/careers/{id}/resources` | Curated free material, grouped by skill |
| `GET` | `/categories` | Categories with counts |
| `GET` | `/skills?limit=` | Skill catalogue ranked by demand |
| `GET` | `/resources?skill=` | Resources for one skill |
| `POST` | `/recommendations` | Scored, explained career matches |
| `POST` | `/skill-gap` | Covered vs. missing skills for a target role |
| `POST` | `/profiles` | Persist a profile, returns an id |
| `GET` | `/profiles/{id}` | Saved profile with fresh recommendations |

Search escapes its input before it reaches MongoDB's `$regex`, so queries like
`C++` or `((` return results instead of a 500.

## Learning resources

`backend/resources.py` is a hand-curated catalogue keyed by skill. Editorial
rules it follows:

- Documentation, books and courses are exact URLs to canonical homes — official
  docs, or books the author publishes free online.
- Video entries are **YouTube search URLs, not pinned video IDs**. A chosen
  video ID dies when the uploader removes it; a search for the same topic keeps
  working and surfaces what is well-rated today.
- Everything listed is free to access without an account.
- Unknown skills fall back to a generated search bundle, so the panel is never
  empty.

## Running it

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env          # optional: add GROQ_API_KEY
uvicorn server:app --reload --port 8010
```

MongoDB is optional. With it running the catalogue is seeded into
`career_path_db` and saved profiles persist; without it everything falls back
to the in-memory catalogue and a per-process profile store.

### Frontend

```bash
cd frontend
npm install --legacy-peer-deps
npm start                     # http://localhost:3000
```

Point the UI at a different API with `REACT_APP_API_URL`.

### Tests

```bash
cd backend
pip install pytest anyio httpx
pytest test_api.py -q
```

29 tests, run with no MongoDB and no API key — deliberately, because that is
the configuration where the fallbacks have to hold.

## Stack

FastAPI · Pydantic · Motor/MongoDB · jsonschema · React 18 · React Router ·
Tailwind CSS · lucide-react · GitHub Actions

Design tokens live in `frontend/src/index.css` and are mapped to semantic
Tailwind names in `tailwind.config.js`, so no component holds a raw hex and
dark mode is a single class on `<html>`.

## Notes for anyone extending this

- `frontend/craco.config.js` sets `postcss.mode: 'file'`. CRA 5 pins its own
  PostCSS options inline, which stops `postcss.config.js` being discovered — so
  without that line the Tailwind directives pass through as literal text and
  every utility class silently does nothing. CI asserts the compiled CSS
  contains real utilities, to stop that regressing.
- `/recommendations` returns `career_id` alongside the title. Do not derive an
  id by slugifying the title: `Full-Stack Developer` is `fullstack-developer`,
  not `full-stack-developer`.
