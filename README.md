# Distributed LLM Evaluation Platform

A learning-first project for building reliable infrastructure that runs and compares model evaluations.

The first milestone is intentionally small: one containerized API server with one health endpoint. PostgreSQL, the job queue, workers, model adapters, and evaluators will be added only after this foundation is understood and verified.

## Run the API

```bash
docker compose up --build
```

In another terminal:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{ "status": "ok" }
```

FastAPI's generated API documentation is available at <http://localhost:8000/docs>.

## Current structure

```text
.
├── app/
│   └── main.py       # FastAPI application and health route
├── compose.yaml      # Runs the API container
├── Dockerfile        # Builds the API image
└── requirements.txt  # Python runtime dependencies
```

## Understand before extending

Be able to explain:

1. Why Uvicorn listens on `0.0.0.0` inside the container.
2. How port `8000` on the host reaches port `8000` in the container.
3. What Docker image layers are created by the Dockerfile.
4. Why dependencies are copied and installed before application code.

## Next milestone

Add a `POST /runs` endpoint and persistence only after the health endpoint works from Docker Compose.
