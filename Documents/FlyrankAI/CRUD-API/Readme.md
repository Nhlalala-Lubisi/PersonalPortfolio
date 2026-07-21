# Task API

A small in-memory CRUD API for managing a to-do list, built with **Python + FastAPI**
for the FlyRank Internship Backend Track, Week 2, Assignment A1.

Data lives only in memory (a Python list) and it resets whenever the server restarts.
That's intentional at this stage; a real database comes in Week 3.

## How to install & run

Requires Python 3.10+.

**macOS / Linux (bash):**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```
> If `Activate.ps1` is blocked by execution policy, run this once:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
>
> Always confirm the venv is active (prompt shows `(.venv)`) before installing
> packages land in your global/user site-packages and `uvicorn` won't be on PATH.

The server starts on **http://localhost:8000**. Interactive Swagger docs are automatically
available at **http://localhost:8000/docs** (FastAPI generates these for free, no extra setup).

## Endpoints

| Method | Path          | Meaning                          | Success | Errors           |
|--------|---------------|-----------------------------------|---------|------------------|
| GET    | `/`           | API description                   | 200     | —                |
| GET    | `/health`     | Health check                      | 200     | —                |
| GET    | `/tasks`      | List all tasks (supports `?done=`, `?search=`, `?limit=`, `?offset=`) | 200 | — |
| GET    | `/tasks/{id}` | Get one task                      | 200     | 404 unknown id   |
| POST   | `/tasks`      | Create a task (`{"title": "..."}`)| 201     | 400 missing/empty title |
| PUT    | `/tasks/{id}` | Update a task's `title` and/or `done` | 200 | 404 unknown id, 400 empty/invalid body |
| DELETE | `/tasks/{id}` | Delete a task                     | 204     | 404 unknown id   |
| GET    | `/stats`      | Extra: totals `{total, done, open}` | 200   | —                |
| POST   | `/reset`      | Extra: restore the 3 example tasks | 200    | —                |

Every error response is a JSON object shaped like `{"error": "..."}` or `{"detail": "..."}`
explaining what went wrong.

## Example: full CRUD cycle via curl

Create a task:

```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk"}'
```

```
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

List tasks:

```bash
curl -i http://localhost:8000/tasks
```

Get a single task / 404 for an unknown one:

```bash
curl -i http://localhost:8000/tasks/1        # 200
curl -i http://localhost:8000/tasks/99       # 404 {"detail":"Task 99 not found"}
```

Update a task:

```bash
curl -i -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done":true}'
```

Delete a task:

```bash
curl -i -X DELETE http://localhost:8000/tasks/1   # 204, empty body
```

Posting an empty body returns 400:

```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{}'
```

```
HTTP/1.1 400 Bad Request
content-type: application/json

{"detail":"Field 'title' is required and cannot be empty"}
```

## Swagger UI

Open http://localhost:8000/docs after starting the server, then use **Try it out** to run
the full CRUD cycle (create → list → get → update → delete) without curl.

> **TODO:** paste your Swagger UI screenshot here once you run it locally, e.g.
> `![Swagger UI](docs/swagger-screenshot.png)`

## The mortality experiment (optional extra)

Create a few tasks, restart the server, then `GET /tasks` again.

> **TODO:** write 2 sentences here about what you observed and why (this is the exact
> observation that motivates Week 3's database lesson, and everything in memory disappears
> the moment the process stops).

## Stage 7: AI vs me (bonus, optional)

> **TODO if you attempt Stage 7:** put your own hand-written prompt here, generate the
> AI's version into `ai-version/`, run your Stage 4 checkpoint curls against it, diff the
> two implementations, and answer:
> 1. What did the AI do better?
> 2. What did it get wrong or quietly ignore?
> 3. What did your prompt forget to specify, and what did the AI silently decide for you?
